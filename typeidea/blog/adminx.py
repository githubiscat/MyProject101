import uuid

import xadmin
from django.contrib import admin

# Register your models here.
from django.contrib.admin.models import LogEntry
from django.urls import reverse
from django.utils.html import format_html
from xadmin.filters import RelatedFieldListFilter, manager
from xadmin.layout import Fieldset, Row, Container

from blog.adminforms import PostAdminForm
from blog.models import Category, Tag, Post
from blog.tools import find_HTML_mediafile_src
from blog.tools.clean_junk_file import CleanJunkFile
from typeidea.base_adminx import BaseOwnerAdmin
from typeidea.custom_site import custom_site


class PostInline:
    # fields = ('title', 'desc')
    form_layout = (
        Container(
            Row('title', 'desc')
        )
    )
    extra = 1
    model = Post


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline, ]
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time', 'owner')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


class CategoryOwnerFilter(RelatedFieldListFilter):
    """ 自定义过滤器只展示当前用户的分类(让一个admin用户只显示自己的信息)"""

    # title = '分类过滤器'  # 展示的标题
    # parameter_name = 'owner_category'  # 查询时URL的参数名 /?owner_category=1

    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.lookup_choices = Category.objects.filter(
            owner=request.user).values_list('id', 'name')


manager.register(CategoryOwnerFilter, take_priority=True)


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm  # 个性化定制form表单
    # admin 表中显示的字段
    list_display = ['title', 'category', 'status',
                    'owner', 'created_time', 'operator', 'pv', 'uv']
    # 那些字段可以作为链接, 点击可以进入编辑页面
    list_display_links = []

    list_filter = ['category']  # 用于侧边过滤栏的字段
    search_fields = ['title', 'category__name', 'owner__username']  # 用于搜索的字段

    actions_on_top = True  # admin 动作类操作按钮在上面
    actions_on_bottom = True  # admin 动作类操作按钮在最下面

    save_on_top = True  # 保存类按钮在最上方
    # filter_vertical = ('tag',)  # 设置多对多字段的前端样式
    filter_horizontal = ('tag',)
    style_fields = {'tag': 'm2m_transfer', }
    form_layout = (
        Fieldset(
            '基础信息',
            Row('title', ),
            Row('status', 'category'),
            Row('tag',)

        ),
        Fieldset(
            '内容信息',
            'desc',
            'content',
        ),
    )

    #  在list_display定义了一个字段operator , 并给这个字段的数据做处理
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'  # 字段的别名 展示在admin

    # def post_response(self, *args, **kwargs):
    #     定义POST 请求的响应
    #     print(self.request.method)
    #     response = super().post_response(*args, **kwargs)
    #     return response

    def get_response(self, *args, **kwargs):
        """
        get_response() 处理get 请求的响应信息
        因为post admin 涉及到可视化编辑器ajax异步上传文件
        上传的文件和POST 数据库关联性较弱, 容易产生垃圾文件
        所以需要设置一个cookie id 用于关联文件和POST文章的关系
        """
        response = super().get_response(*args, **kwargs)

        if response and self.request.method == 'GET':
            uuid_str = str(uuid.uuid4())
            response.set_cookie('post_stamp', uuid_str,
                                path=str(self.request.path))
            response.set_cookie('post_stamp_ckfile', uuid_str,
                                path='/ckeditor/')
        return response

    def save_models(self):
        # 获取cookie中的post_stamp 编辑标记
        post_stamp = self.request.COOKIES.get('post_stamp')

        # 获取form 中的content 字段内容
        post_content = self.new_obj.content
        src_list = find_HTML_mediafile_src.find_all(post_content)
        old_src_list = []
        if self.new_obj.id and self.new_obj.attached_file:
            old_src_list = eval(self.new_obj.attached_file)
        self.new_obj.attached_file = str(src_list)
        self.new_obj.owner = self.request.user
        ret = super().save_models()  # 保存数据

        # new_obj 是xadmin创建或更改内容是创建的数据库对象
        obj = self.new_obj

        cleaner = CleanJunkFile(cookie_stamp=post_stamp,
                                src_list=src_list,
                                old_src_list=old_src_list,
                                post_id=obj.id)
        cleaner.clean_file()
        return ret

    # def save_related(self):
    #     obj = self.new_obj
    #     print('操作的数据对象',obj.id)

    # @property
    # def media(self):
    #     media = super().media
    #     media.add_js(['https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js'])
    #     media.add_css(['https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css'])
    #     return media
