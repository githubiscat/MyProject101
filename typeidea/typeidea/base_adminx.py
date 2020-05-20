from django.contrib.admin import ModelAdmin


class BaseOwnerAdmin(object):
    """
    1. 用来自动补充文章/分类/标签/侧边栏/友链/这些model的owner 字段
    2. 用来针对queryset过滤当前用户的数据
    """
    exclude = ('owner',)
    def get_list_queryset(self):
        request = self.request
        qs = super().get_list_queryset()
        return qs.filter(owner=request.user)


    def save_models(self):
        # self.new_obj 是xadmin在保存数据时创建的一个数据库对象
        self.new_obj.owner = self.request.user
        return super().save_models()



