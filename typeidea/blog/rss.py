""" RSS 简易信息聚合, 提供订阅接口"""
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed

from blog.models import Post


class ExtendedRssFeed(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(ExtendedRssFeed, self).add_item_elements(handler, item)
        handler.addQuickElement('content:html', item['content_html'])



class LatestPostFeed(Feed):
    title = '满满屋'
    link = '/rss/'
    description = '欢迎来到满满屋,这里有我的分享'

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.desc

    def item_link(self, item):
        return reverse('post', kwargs={'post_id': item.pk})

    def item_extra_kwargs(self, item):
        print('aaaaa')
        print(self.item_content(item))
        return {'content_html': self.item_content(item)}

    def item_content(self, item):
        return item.content


