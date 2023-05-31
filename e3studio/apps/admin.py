from django.contrib import admin
from django.conf import settings
from django.utils.html import format_html

# Register your models here.

from apps.models import App


class AppAdmin(admin.ModelAdmin):
    list_display = ('appname', 'id')

    def image_tag_1(self, obj):
        return format_html('<img src="{img}" width="150px"/>'.format(img=obj.front_image.url))
    image_tag_1.short_description = 'Front Image'

    def image_tag_2(self, obj):
        return format_html('<img src="{img}" width="624px"/>'.format(img=obj.top_image.url))
    image_tag_2.short_description = 'Top Image'

    readonly_fields = ['image_tag_1', 'image_tag_2']


admin.site.register(App, AppAdmin)
