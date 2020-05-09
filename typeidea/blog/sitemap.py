"""sitemap, 提供给搜索引擎的spider, 收录我们的网站内容"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import Post


class PostSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)

    def lastmod(self, obj):
        return obj.created_time

    def location(self, obj):
        return reverse('post', kwargs={'post_id': obj.pk})
