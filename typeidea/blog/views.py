from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from blog.models import Tag, Post, Category
from config.models import SideBar


def post_list(request, category_id=None, tag_id=None):
    mask = ''  #用于显示分类的一个标志位
    tag = None
    category = None
    if tag_id:
        postlist, tag = Post.get_by_tag(tag_id)
    elif category_id:
        postlist, category = Post.get_by_category(category_id)
    else:
        postlist = Post.objects.filter(status=Post.STATUS_NORMAL)
    sidebars = SideBar.get_all()
    tags = Tag.get_all()
    data = {
        'postlist': postlist,
        'mask': mask,
        'tag': tag,
        'tags': tags,
        'category': category,
        'sidebars': sidebars,
    }
    data.update(Category.get_navs())
    return render(request, template_name='blog/list.html', context=data)


def post_detail(request, post_id=None):
    context = 'post_id is {}'.format(post_id)
    if post_id:
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            post = None
    else:
        post = None
    data = {
        'post': post,
        'tags': Tag.get_all(),
        'sidebars': SideBar.get_all(),
    }
    data.update(Category.get_navs())

    return render(request, template_name='blog/detail.html', context=data)



