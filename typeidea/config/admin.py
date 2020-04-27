from django.contrib import admin

# Register your models here.
from config.models import Link, SideBar
from typeidea.custom_site import custom_site


@admin.register(Link, site=custom_site)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'weight', 'owner', 'created_time')
    search_fields = ('title', 'owner')

    fields = ('title',
              ('status','weight'),
              'href'
    )

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin, self).save_model(request, obj, form, change)

@admin.register(SideBar, site=custom_site)
class SiteBar(admin.ModelAdmin):
    list_display = ('title', 'display_type', 'content',
                    'status', 'owner', 'created_time', 'weight')

    fields = ('title', 'display_type', 'content',
              'status', 'weight')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SiteBar, self).save_model(request, obj, form, change)
