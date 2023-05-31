from rest_framework import serializers

from userprofile.models import Avatar, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'first_name', 'last_name', 'subject', 'city', 'province',
                  'birth_date', 'gender', 'bio')


# from courses.models import Chapter, Section, Choice, Answer


class CourseCheckSerializer(serializers.Serializer):
    subject = serializers.CharField(required=False, allow_blank=True)
    token = serializers.CharField(required=False, allow_blank=True)


# class SectionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Section
#         fields = ('id', 'chapter', 'section')


# class ItemInstanceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ItemInstance
#         fields = ('title', 'user', 'category', 'platform', 'brand',
#                   'condition', 'reg_price', 'sale_price', 'sale', 'rating',
#                   'quantity', 'description', 'post_date', 'cover_image')
