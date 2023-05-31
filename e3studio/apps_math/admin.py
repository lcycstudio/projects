from django.contrib import admin
from django.conf import settings
from django.utils.html import format_html

# Register your models here.

from apps_math.models import AppsMath, Function, InitialFunctionValue, InitialDerivativeValue, Parameter, LeftBound, RightBound, Title, HorizontalLabel, VerticalLabel


class AppsMathAdmin(admin.ModelAdmin):
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


class FunctionAdmin(admin.ModelAdmin):
    list_display = ('appname', 'note')
    readonly_fields = ['latex']


class InitialFunctionValueAdmin(admin.ModelAdmin):
    list_display = ('appname', 'note')
    readonly_fields = ['latex']


class InitialDerivativeValueAdmin(admin.ModelAdmin):
    list_display = ('appname', 'note')
    readonly_fields = ['latex']


class ParameterAdmin(admin.ModelAdmin):
    list_display = ('appname', 'note')
    readonly_fields = ['latex']


class LeftBoundAdmin(admin.ModelAdmin):
    list_display = ('appname', 'note')
    readonly_fields = ['latex']


class RightBoundAdmin(admin.ModelAdmin):
    list_display = ('appname', 'note')
    readonly_fields = ['latex']


class TitleAdmin(admin.ModelAdmin):
    list_display = ('appname', 'note')
    readonly_fields = ['latex']


class HorizontalLabelAdmin(admin.ModelAdmin):
    list_display = ('appname', 'note')
    readonly_fields = ['latex']


class VerticalLabelAdmin(admin.ModelAdmin):
    list_display = ('appname', 'note')
    readonly_fields = ['latex']


class Admin(admin.ModelAdmin):
    list_display = ('appname', 'note')
    readonly_fields = ['latex']


admin.site.register(AppsMath, AppsMathAdmin)
admin.site.register(Function, FunctionAdmin)
admin.site.register(InitialFunctionValue, InitialFunctionValueAdmin)
admin.site.register(InitialDerivativeValue, InitialDerivativeValueAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(LeftBound, LeftBoundAdmin)
admin.site.register(RightBound, RightBoundAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(HorizontalLabel, HorizontalLabelAdmin)
admin.site.register(VerticalLabel, VerticalLabelAdmin)
