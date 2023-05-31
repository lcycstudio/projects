from django.contrib import admin
from django.utils.html import format_html
from .models import Avatar, Profile
# Register your models here.


class AvatarAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'avatar')
    list_display_links = ('id', 'user')

    def image_tag(self, obj):
        return format_html('<img src="{img}" width="150px"/>'.format(img=obj.avatar.url))
    image_tag.short_description = 'Image'
    readonly_fields = ['image_tag', ]


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'gender', 'city', 'province', 'birth_date')


admin.site.register(Avatar, AvatarAdmin)
admin.site.register(Profile, ProfileAdmin)
