from django.contrib import admin

# Register your models here.
from django.urls import reverse
from django.utils.html import format_html

from comment.models import Comment, Reply
from typeidea.custom_site import custom_site


@admin.register(Comment, site=custom_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'con', 'nickname',
                    'email', 'status', 'created_time', 'operator')
    list_display_links = ['con']
    fields = (
        'target',
        'content',
        ('email', 'website'),
        'status'
    )
    search_fields = ['target', 'contents', 'nickname']
    list_filter = ['status', 'created_time', 'website']

    actions_on_top = True
    save_on_top = True

    def operator(self, obj):
        return format_html('<a href="{}">编辑</a>',
                           reverse('cus_admin:comment_comment_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    def con(self, obj):
        c = obj.content
        return c[:20] + '...'
    con.short_description = '内容'

    def get_queryset(self, request):
        # 过滤数据 只显示当前登录用户写的文章的评论和回复
        qs = super(CommentAdmin, self).get_queryset(request)
        return qs.filter(target__owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.nickname = str(request.user)
        return super(CommentAdmin, self).save_model(request, obj, form, change)

@admin.register(Reply, site=custom_site)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('id','comment', 'reply_id', 'reply_type',
                    'from_name', 'from_email', 'from_website',
                    'to_name', 'from_content', 'created_time', 'status')
    # list_display_links = ['con']
    fields = (
        'reply_type',
        'from_website',
        'status'
    )
    # search_fields = ['target', 'contents', 'nickname']
    # list_filter = ['status', 'created_time', 'website']

    actions_on_top = True
    save_on_top = True

    # def operator(self, obj):
    #     return format_html('<a href="{}">编辑</a>',
    #                        reverse('cus_admin:comment_comment_change', args=(obj.id,))
    #     )
    # operator.short_description = '操作'

    def con(self, obj):
        c = obj.content
        return c[:20] + '...'
    con.short_description = '内容'

    def get_queryset(self, request):
        qs = super(ReplyAdmin, self).get_queryset(request)
        return qs.filter(comment__target__owner=request.user)



    # def save_model(self, request, obj, form, change):
    #     obj.nickname = str(request.user)
    #     return super(CommentAdmin, self).save_model(request, obj, form, change)