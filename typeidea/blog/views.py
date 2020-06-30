from datetime import date

from django.core.cache import cache
from django.db.models import Q, F
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, render_to_response

# Create your views here.
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView, DetailView

from blog.models import Tag, Post, Category
from comment.forms import CommentForm, ReplyForm
from comment.models import Comment
from config.models import SideBar
from typeidea.settings.base import HOST_NAME

""" 类视图
类视图有着更好的封装, 解耦了http 的get post put delete patch 等请求, 对应不同的请求method
类视图对应相应的get() post()来处理不同的请求, 此外基于类View Django 还提供了 TemplateView
DetailView ListView 等CBV(class-based-view). 封装的程度更高只需要配置特定的参数和方法即
可实现类似function-view的逻辑. 虽然开发者的代码看起来更少了,但是后台django 有大量的代码去
解析开发者配置信息,并作出相应的处理. 
相应的配置参数作用在下面代码中会做出解释 
"""

def return404(request, exception):
    content = {
        'title':'404页面未找到',
        'sidebars': SideBar.get_all(),
        'tags': Tag.get_all(),
    }
    content.update(Category.get_navs())
    body = render_to_string('blog/404.html',context=content)
    return HttpResponseNotFound(body)



class CommonViewMixin:
    """ 获取通用的部分 侧边栏 热导航等  """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {'sidebars': SideBar.get_all(), }
        )
        context.update(Category.get_navs())
        context.update({'tags': Tag.get_all()})
        return context


class IndexView(CommonViewMixin, ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        top_posts = Post.get_top()
        context.update({
            'path_mark': 'index',
            'top_posts': top_posts,
            'req_path': HOST_NAME + self.request.get_full_path(),
        })
        return context
    # model = Post  # model 指定class based View要使用的数据库model
    queryset = Post.get_all()  # 指定cbv 要使用的查询集(过滤数据后), 与model二选一, 只用model时 django会进行普通all()查询
    paginate_by = 10  # 分页 每页显示的数量
    context_object_name = 'postlist'  # 传递到模板的上下文对象的名称 (默认到模板中是object_list)
    template_name = 'blog/index.html'  # 指定要渲染的模板


class CategoryView(IndexView):
    """根据category 分类过滤展示文章列"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
            'path_mark': 'category',

        })
        return context

    def get_queryset(self):
        """ 重写queryset,根据分类过滤 """
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)

    template_name = 'blog/list.html'

class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
            'path_mark': 'tag',
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)

    template_name = 'blog/list.html'


class PostDetailView(CommonViewMixin, DetailView):

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response

    queryset = Post.get_all()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            # 'comment_list': Comment.objects
            #     .filter(Q(status=Comment.STATUS_NORMAL) & Q(post_id=post_id))
            #     .order_by('created_time'),
            'comment_form': CommentForm,
            'reply_form': ReplyForm,
            'path_mark': 'post',
            'req_path': HOST_NAME + self.request.get_full_path(),
        })
        return context

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s' % (uid, self.request.path)
        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()),self.request.path)
        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24*60*60)

        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 60)

        if increase_pv and increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1,
                                                          uv=F('uv') + 1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)


class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'keyword': self.request.GET.get('keyword', ''),
            'path_mark': 'search',
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword', '')
        if not keyword:
            return queryset
        # Q(owner__username__icontains=keyword) 根据用户名做查询
        q = queryset.filter(Q(title__icontains=keyword)
                               | Q(desc__icontains=keyword)
                               | Q(content__icontains=keyword))
        if len(q):
            return q
        else:
            pass
        return queryset.filter(Q(title__icontains=keyword)
                               | Q(desc__icontains=keyword)
                               | Q(content__icontains=keyword))

    template_name = 'blog/list.html'


class AutherView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        auther_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=auther_id)

    template_name = 'blog/list.html'


class FeedbackView(CommonViewMixin, View):
    def get(self, request):
        return render(request, 'blog/feedback.html',)







