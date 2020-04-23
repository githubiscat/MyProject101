from django.contrib import admin

# Register your models here.
from django.contrib.admin.models import LogEntry
from django.urls import reverse
from django.utils.html import format_html

from blog.adminforms import PostAdminForm
from blog.models import Category, Tag, Post
from typeidea.custom_site import custom_site


class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [PostInline]
    list_display = ('name', 'status', 'is_nav','created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'



@admin.register(Tag, site=custom_site)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    """ 自定义过滤器只展示当前用户的分类(让一个admin用户只显示自己的信息)"""

    title = '分类过滤器'  # 展示的标题
    parameter_name = 'owner_category'  # 查询时URL的参数名 /?owner_category=1

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        print(category_id)
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset

@admin.register(Post, site=custom_site)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    # admin 表中显示的字段
    list_display = ['title', 'category', 'status',
                    'owner', 'created_time', 'operator']
    # 那些字段可以作为链接, 点击可以进入编辑页面
    list_display_links = []

    list_filter = [CategoryOwnerFilter, 'status']  # 用于侧边过滤栏的字段
    search_fields = ['title', 'category__name']  #用于搜索的字段

    actions_on_top = True  # admin 动作类操作按钮在上面
    actions_on_bottom = True  # admin 动作类操作按钮在最下面

    save_on_top = True  # 保存类按钮在最上方

    # form 表中需要填写的字段, 需要填写特殊值的字段可以在save_model()中定义
    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )
    fieldsets = (
        ('基础配置:', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status'
            )
        }),
        ('内容', {
            'fields': (
                'desc',
                'content'
            )
        }),
        ('其他', {
            'classes': ('collapse',),
            'fields': ('tag',)
        })
    )
    # filter_vertical = ('tag',)  # 设置多对多字段的前端样式
    filter_horizontal = ('tag',)

    #  在list_display定义了一个字段operator , 并给这个字段的数据做处理
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'  # 字段的别名 展示在admin

    def save_model(self, request, obj, form, change):
        obj.owner = request.user  # 不能随便的更改作者,所以作者都做为固定值去保存
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        """过滤文章, 用户只能查看自己的文章
        对Queryset继承并再次添加一个过滤条件 owner=当前 user
        """
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

@admin.register(LogEntry)
class  LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag',
                    'user', 'change_message']