from rest_framework import serializers

from apps.models import App


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ('id', 'appname', 'content',
                  'front_image', 'top_image', 'web')


# class MessageSerializer(serializers.Serializer):
#     name = serializers.CharField(
#         max_length=None, min_length=None, allow_blank=False,)
#     email = serializers.EmailField(
#         max_length=None, min_length=None, allow_blank=False)
#     message = serializers.CharField(max_length=1005, min_length=None, allow_blank=False, style={
#                                     'base_template': 'textarea.html'})
