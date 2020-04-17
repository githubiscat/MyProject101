from django.contrib import admin

# Register your models here.
from django.urls import reverse
from django.utils.html import format_html

from blog.models import Category, Tag, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav','created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # admin 表中显示的字段
    list_display = ['title', 'category', 'status', 'created_time', 'operator']
    # 那些字段可以作为链接, 点击可以进入编辑页面
    list_display_links = []

    list_filter = ('category__name', 'status')  # 用于侧边过滤栏的字段
    search_fields = ['title', 'category__name']  #用于搜索的字段

    actions_on_top = True  # admin 动作类操作按钮在上面
    actions_on_bottom = True  # admin 动作类操作按钮在最下面

    save_on_top = True  # 保存类按钮在最上方

    # form 表中需要填写的字段, 需要填写特殊值的字段可以在save_model()中定义
    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
    )

    #  在list_display定义了一个字段operator , 并给这个字段的数据做处理
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作' # 字段的别名 展示在admin

    def save_model(self, request, obj, form, change):
        obj.owner = request.user  # 不能随便的更改作者,所以作者都做为固定值去保存
        return super(PostAdmin, self).save_model(request, obj, form, change)
