import xadmin
from django.contrib import admin

# Register your models here.
from config.adminforms import SideBarForm
from config.models import Link, SideBar
from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site


@xadmin.sites.register(Link)
class LinkAdmin:
    list_display = ('title', 'status', 'weight', 'owner', 'created_time')
    search_fields = ('title', 'owner')

    form_layout = ('title',
              ('status','weight'),
              'href'
    )

    def save_models(self):
        request = self.reqeust
        self.new_obj.owner = request.user
        return super().save_models()

@xadmin.sites.register(SideBar)
class SideBarAdmin:
    form = SideBarForm
    list_display = ('title', 'display_type', 'content',
                    'status', 'owner', 'created_time', 'weight')

    form_layout = ('title', 'display_type', 'content',
              'status', 'weight')

    exclude = ('owner',)

    def get_queryset(self):
        request = self.request
        qs = super().get_queryset()
        return qs.filter(owner=request.user)

    def save_models(self):
        request = self.request
        self.new_obj.owner = request.user
        return super().save_models()
