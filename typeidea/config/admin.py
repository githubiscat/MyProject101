from django.contrib import admin

# Register your models here.
from config.models import Link, SideBar


@admin.register(Link)
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

@admin.register(SideBar)
class SiteBar(admin.ModelAdmin):
    list_display = ('title', 'display_type', 'content',
                    'status', 'owner', 'created_time')

    fields = ('title', 'display_type', 'content',
              'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SiteBar, self).save_model(request, obj, form, change)
