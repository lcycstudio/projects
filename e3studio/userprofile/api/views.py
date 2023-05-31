from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    CreateAPIView,
    DestroyAPIView,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from userprofile.models import Avatar, Profile
from .serializers import ProfileSerializer, CourseCheckSerializer
from courses.models import Subject


class ProfileListView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        profileset = [item for item in Profile.objects.all()]
        serializer = ProfileSerializer(profileset, many=True)
        serializer_data = serializer.data
        for item in serializer_data:
            for index in range(len(item["subject"])):
                item["subject"][index] = Subject.objects.get(
                    id=item["subject"][index]).subject
        return Response(serializer.data)


class ProfileDetailView(RetrieveAPIView):
    def get(self, request, token, format=None):
        tokenset = Token.objects.all()
        token = get_object_or_404(tokenset, key=token)
        user = token.user
        username = user.username
        profileset = Profile.objects.all()
        profile = get_object_or_404(profileset, user=user)
        serializer = ProfileSerializer(profile)
        serializer_data = serializer.data
        serializer_data["province"] = profile.province
        for index in range(len(serializer_data["subject"])):
            serializer_data["subject"][index] = Subject.objects.get(
                id=serializer_data["subject"][index]).subject
        return Response(serializer_data)


class CourseCheckView(UpdateAPIView):
    serializer_class = CourseCheckSerializer

    def put(self, request, format=None):
        tokenset = Token.objects.all()
        token = get_object_or_404(tokenset, key=request.data["token"])
        user = token.user
        profileset = Profile.objects.all()
        profile = get_object_or_404(profileset, user=user)
        temp_dict = {}
        # if profile
        if len(profile.subject.all()) != 0:
            for item in profile.subject.all():
                if item.subject == request.data["subject"]:
                    temp_dict["detail"] = item.subject
                    break
                else:
                    temp_dict["detail"] = "Not found."
        else:
            temp_dict["detail"] = "Not found."
        return Response(temp_dict)


# class ItemCategoryCreateView(CreateAPIView):
#     queryset = ItemCategory.objects.all()
#     serializer_class = ItemCategorySerializer
#     permission_classes = (permissions.IsAuthenticated, )

#     def post(self, request, format=None):
#         category = request.data['category']
#         image = request.data['image']
#         obj, created = ItemCategory.objects.get_or_create(
#             category=category, image=image)
#         obj.save()
#         return Response('ok')


# class ChapterDetailView(RetrieveAPIView):
#     def get(self, request, subject, chapter, format=None):
#         subject_obj = Subject.objects.get(subject=subject)
#         chapterset = Chapter.objects.filter(subject=subject_obj)
#         chapter = get_object_or_404(chapterset, chapter=chapter)
#         serializer = ProfileSerializer(chapter)
#         serializer_data = serializer.data
#         serializer_data["sections"] = []
#         sectionset = Section.objects.filter(chapter=chapter)
#         for item in sectionset:
#             serializer_data["sections"].append(item.section)
#         return Response(serializer_data)
    # serializer2 = ItemPlatformSerializer(platformset)
    # serializer_data.append({'platform': 'ok'})

    # print(serializer2.data)
    # for item in serializer2.data:
    #     print(item)
    # serializer_data["platforms"] = item["platform"]
    # print(serializer_data)
    # print(obj['platform']=serializer2.data)


# class SectionDetailView(RetrieveAPIView):
#     permission_classes = (permissions.AllowAny, )

#     def get(self, request, subject, chapter, section, format=None):
#         subject_obj = Subject.objects.get(subject=subject)
#         chapterset = Chapter.objects.filter(subject=subject_obj)
#         chapter = get_object_or_404(chapterset, chapter=chapter)
#         sectionset = Section.objects.filter(chapter=chapter)
#         section = get_object_or_404(sectionset, section=section)
#         serializer = SectionSerializer(section)
#         serializer_data = serializer.data
#         return Response(serializer_data)
    # for item in sectionset:
    #     serializer_data["sections"].append(item.section)
    #     serializer_data["section_images"].append(str(item.image))


# class ItemPlatformListView(ListAPIView):
#     queryset = ItemPlatform.objects.all()
#     serializer_class = ItemPlatformSerializer
#     permission_classes = (permissions.AllowAny, )


# class ItemPlatformDetailView(RetrieveAPIView):
#     def get(self, request, platformTitle, format=None):
#         platformset = ItemPlatform.objects.all()
#         platform = get_object_or_404(platformset, platform=platformTitle)
#         serializer = ItemPlatformSerializer(platform)
#         serializer_data = serializer.data
#         serializer_data["category"] = platform.category.category
#         serializer_data["items"] = []
#         serializer_data["item_iuid"] = []
#         serializer_data["item_seller"] = []
#         serializer_data["item_cover"] = []
#         itemset = ItemInstance.objects.filter(platform=platform)
#         for item in itemset:
#             serializer_data["items"].append(item.title.title)
#             serializer_data["item_iuid"].append(item.iuid.hex)
#             serializer_data["item_seller"].append(item.user.username)
#             serializer_data["item_cover"].append(str(item.cover_image))
#         return Response(serializer_data)


# class ItemPlatformCreateView(CreateAPIView):
#     queryset = ItemPlatform.objects.all()
#     serializer_class = ItemPlatformSerializer
#     permission_classes = (permissions.IsAuthenticated, )

#     def post(self, request, format=None):
#         platform = request.data['Platform']
#         image = request.data['image']
#         obj, created = ItemPlatform.objects.get_or_create(
#             platform=platform, image=image)
#         obj.save()
#         return Response('ok')


# class ItemInstanceUserList(RetrieveAPIView):
#     def get(self, request, itemUser, format=None):
#         userset = User.objects.all()
#         user = get_object_or_404(userset, username=itemUser)
#         itemset = ItemInstance.objects.filter(user=user)
#         serializer = ItemInstanceSerializer(itemset)
#         return Response(serializer.data)


# class ItemInstanceDetailView(RetrieveAPIView):
#     def get(self, request, itemUser, hexid, format=None):
#         userset = User.objects.all()
#         user = get_object_or_404(userset, username=itemUser)
#         itemset = ItemInstance.objects.filter(user=user)
#         for each in itemset:
#             if each.iuid.hex == hexid:
#                 item = each
#         # item = get_object_or_404(itemset, iuid=hex)
#         serializer = ItemInstanceSerializer(item)
#         serializer_data = serializer.data
#         serializer_data['title'] = item.title.title
#         serializer_data['user'] = item.user.username
#         serializer_data['category'] = item.category.category
#         serializer_data['platform'] = item.platform.platform
#         serializer_data['images'] = []
#         imageset = ItemImage.objects.filter(
#             user=item.user, title=item.title.id)
#         for each in imageset:
#             serializer_data['images'].append(str(each.image))
#         return Response(serializer_data)


# class ArticleDetailView(RetrieveAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer


# class ArticleCreateView(CreateAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer


# class ArticleUpdateView(UpdateAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer


# class TodolistDeleteView(DestroyAPIView):
#     queryset = Todolist.objects.all()
#     serializer_class = TodolistSerializer
#     permission_classes = (permissions.IsAuthenticated, )
#     def delete(self, request, pk, format=None):
#         todo_item = Todolist.objects.get(id=pk)
#         if todo_item.username == request.user:
#             todo_item.delete()
#             return Response('deleted')
#         else:
#             raise ValidationError({"message": "Cannot delete others' items."})
