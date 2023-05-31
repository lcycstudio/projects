from django.contrib import admin
from django.conf import settings
from django.utils.html import format_html
from courses.models import Subject


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject', 'id')

    def image_tag_1(self, obj):
        return format_html('<img src="{img}" width="200px"/>'.format(img=obj.front_image.url))
    image_tag_1.short_description = 'Front Image'

    def image_tag_2(self, obj):
        return format_html('<img src="{img}" width="624px"/>'.format(img=obj.top_image.url))
    image_tag_1.short_description = 'Top Image'

    readonly_fields = ['image_tag_1', 'image_tag_2']


# class PublicAdmin(admin.ModelAdmin):
#     list_display = ('id', 'file')


# admin.site.register(Public, PublicAdmin)
admin.site.register(Subject, SubjectAdmin)
