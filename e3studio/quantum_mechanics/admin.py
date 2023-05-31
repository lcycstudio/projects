import os
from django.contrib import admin
from django.conf import settings
from django.utils.html import format_html

# Register your models here.

from quantum_mechanics.models import Chapter, Section, Paragraph, Image, Exercise, Choice


class ChapterAdmin(admin.ModelAdmin):
    list_display = ('chapter', 'id')

    def image_tag(self, obj):
        return format_html('<img src="{img}" width="150px"/>'.format(img=obj.image.url))
    image_tag.short_description = 'Image'
    readonly_fields = ['image_tag', ]


class SectionAdmin(admin.ModelAdmin):
    list_display = ('section', 'id', 'chapter')

    def image_tag(self, obj):
        return format_html('<img src="{img}" width="150px"/>'.format(img=obj.image.url))
    image_tag.short_description = 'Image'
    readonly_fields = ['image_tag', ]


class ParagraphAdmin(admin.ModelAdmin):
    list_display = ('section', 'id', 'chapter')

    def next_page(self, obj):
        if obj is not None:
            obj_set = Paragraph.objects.all()
            if len(obj_set) > int(str(obj.id)):
                go_id = int(str(obj.id)) + 1
                return format_html('<a href="http://{ch}/admin/quantum_mechanics/paragraph/{ok}/change/">Next</a>'.format(ch=settings.CURRENT_HOST, ok=go_id))
            else:
                return format_html('<p>None</p>')

    def prev_page(self, obj):
        if obj is not None:
            if int(str(obj.id)) > 1:
                go_id = int(str(obj.id)) - 1
                return format_html('<a href="http://{ch}/admin/quantum_mechanics/paragraph/{ok}/change/">Back</a>'.format(ch=settings.CURRENT_HOST, ok=go_id))
            else:
                return format_html('<p>None</p>')
    readonly_fields = ['next_page', 'prev_page']


# class EquationAdmin(admin.ModelAdmin):
#     list_display = ('section', 'id', 'chapter')

#     def next_page(self, obj):
#         if obj is not None:
#             obj_set = Equation.objects.all()
#             if len(obj_set) > int(str(obj.id)):
#                 go_id = int(str(obj.id)) + 1
#                 return format_html('<a href="http://{ch}/admin/quantum_mechanics/equation/{ok}/change/">Next</a>'.format(ch=settings.CURRENT_HOST, ok=go_id))
#             else:
#                 return format_html('<p>None</p>')

#     def prev_page(self, obj):
#         if obj is not None:
#             if int(str(obj.id)) > 1:
#                 go_id = int(str(obj.id)) - 1
#                 return format_html('<a href="http://{ch}/admin/quantum_mechanics/equation/{ok}/change/">Back</a>'.format(ch=settings.CURRENT_HOST, ok=go_id))
#             else:
#                 return format_html('<p>None</p>')
#     readonly_fields = ['next_page', 'prev_page']


class ImageAdmin(admin.ModelAdmin):
    list_display = ('section', 'id', 'chapter')

    def image_tag(self, obj):
        return format_html('<img src="{img}" width="150px"/>'.format(img=obj.section_image.url))
    image_tag.short_description = 'Image'

    def next_page(self, obj):
        if obj is not None:
            obj_set = Image.objects.all()
            if len(obj_set) > int(str(obj.id)):
                go_id = int(str(obj.id)) + 1
                return format_html('<a href="http://{ch}/admin/quantum_mechanics/image/{ok}/change/">Next</a>'.format(ch=settings.CURRENT_HOST, ok=go_id))
            else:
                return format_html('<p>None</p>')

    def prev_page(self, obj):
        if obj is not None:
            if int(str(obj.id)) > 1:
                go_id = int(str(obj.id)) - 1
                return format_html('<a href="http://{ch}/admin/quantum_mechanics/image/{ok}/change/">Back</a>'.format(ch=settings.CURRENT_HOST, ok=go_id))
            else:
                return format_html('<p>None</p>')
    # readonly_fields = ['next_page', 'prev_page']
    readonly_fields = ['image_tag', 'next_page', 'prev_page']


class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'id', 'chapter', 'section')


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('answer', 'id', 'chapter', 'section')


admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Paragraph, ParagraphAdmin)
# admin.site.register(Equation, EquationAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Choice, ChoiceAdmin)
# # admin.site.register(Plot, PlotAdmin)
