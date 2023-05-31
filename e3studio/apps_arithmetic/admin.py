from django.contrib import admin
from django.conf import settings
from django.utils.html import format_html

# Register your models here.

from apps_arithmetic.models import AppsArithmetic, Grade


class AppsArithmeticAdmin(admin.ModelAdmin):
    list_display = ('appname', 'id')

    def image_tag_1(self, obj):
        return format_html('<img src="{img}" width="200px"/>'.format(img=obj.front_image.url))
    image_tag_1.short_description = 'Front Image'

    def image_tag_2(self, obj):
        return format_html('<img src="{img}" width="200px"/>'.format(img=obj.top_image.url))
    image_tag_2.short_description = 'Top Image'

    def image_tag_3(self, obj):
        return format_html('<img src="{img}" width="200px"/>'.format(img=obj.right_image.url))
    image_tag_3.short_description = 'Right Image'

    readonly_fields = ['image_tag_1', 'image_tag_2', 'image_tag_3']


class GradeAdmin(admin.ModelAdmin):
    list_display = ('grade', 'appname', 'id')
    list_filter = ('appname',)


admin.site.register(AppsArithmetic, AppsArithmeticAdmin)
admin.site.register(Grade, GradeAdmin)
