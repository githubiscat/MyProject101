"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from blog.views import IndexView, CategoryView, TagView, PostDetailView, \
    SearchView, AutherView
from comment.views import CommentView, reply_comment
from config.views import LinkListView
from typeidea.custom_site import custom_site

urlpatterns = [
    # class view
    re_path(r'^$', IndexView.as_view()),
    re_path(r'^auther/(?P<owner_id>\d+)/$', AutherView.as_view(), name='auther'),
    re_path(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category'),
    re_path(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag'),
    re_path(r'^post/(?P<post_id>\d+).html$', PostDetailView.as_view(), name='post'),
    re_path(r'^search/$', SearchView.as_view(), name='search'),
    re_path(r'^links/$', LinkListView.as_view(), name='link'),
    re_path(r'^comment/$', CommentView, name='comment'),
    re_path(r'^reply/$', reply_comment, name='reply'),
    # func view
    # re_path(r'^$', post_list),
    # re_path(r'^category/(?P<category_id>\d+)/$', post_list, name='category'),
    # re_path(r'^tag/(?P<tag_id>\d+)/$', post_list, name='tag'),
    # re_path(r'^post/(?P<post_id>\d+).html$', post_detail, name='post'),
    # re_path(r'^links/$', links),

    re_path(r'^superadmin/', admin.site.urls),
    re_path(r'^admin/', custom_site.urls)
    # path(r'admin/', custom_site.urls)
]
