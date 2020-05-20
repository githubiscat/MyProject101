"""
DJango_autocomplete-light插件的原理比较简单, 首先峰组昂好一个接口, 用来查询你要处理的数据,
然后提供一个前端组件, 其中包含HTML css js . 等用户输入数据时, 实时接口查询(ajax)
拿到数据后展示到页面上, 供用户选择
"""
from dal import autocomplete

from blog.models import Category, Tag


class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Category.objects.none()

        qs = Category.objects.filter(owner=self.request.user)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Tag.objects.none()
        qs = Tag.objects.filter(owner=self.request.user)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
    # def get_queryset(self):
    #     if not self.request.user.is_authenticated:
    #         return Tag.objects.none()
    #
    #     qs = Tag.objects.filter(owner=self.request.user)
    #     if self.q:
    #         qs = qs.filter(name__istartswith=self.q)
    #     return qs

