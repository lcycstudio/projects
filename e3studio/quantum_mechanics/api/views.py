import os
import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd
import scipy as sp
import numpy as np
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from quantum_mechanics.models import Chapter, Section, Paragraph, Image, Exercise, Choice, Answer
from .serializers import ChapterSerializer, SectionSerializer, ChoiceSerializer, AnswerSerializer


class ChapterListView(ListAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        chapterset = [item for item in Chapter.objects.all()]
        serializer = ChapterSerializer(chapterset, many=True)
        serializer_data = serializer.data
        for item in serializer_data:
            item["sections"] = []
            sectionset = Section.objects.filter(
                chapter=item["id"])
            if len(sectionset) != 0:
                for section in sectionset:
                    item["sections"].append(section.section)
        return Response(serializer_data)


class ChapterDetailView(RetrieveAPIView):
    def get(self, request, chapter, format=None):
        chapterset = Chapter.objects.all()
        chapter_obj = get_object_or_404(chapterset, chapter=chapter)
        serializer = ChapterSerializer(chapter_obj)
        serializer_data = serializer.data
        serializer_data["sections"] = []
        sectionset = Section.objects.filter(chapter=chapter_obj)
        for item in sectionset:
            serializer_data["sections"].append(item.section)
        return Response(serializer_data)
        # serializer2 = ItemPlatformSerializer(platformset)
        # serializer_data.append({'platform': 'ok'})

        # print(serializer2.data)
        # for item in serializer2.data:
        #     print(item)
        # serializer_data["platforms"] = item["platform"]
        # print(serializer_data)
        # print(obj['platform']=serializer2.data)


class SectionDetailView(RetrieveAPIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, chapter, section, format=None):
        chapterset = Chapter.objects.all()
        chapter = get_object_or_404(chapterset, chapter=chapter)
        sectionset = Section.objects.filter(chapter=chapter)
        section = get_object_or_404(sectionset, section=section)
        serializer = SectionSerializer(section)
        serializer_data = serializer.data
        return Response(serializer_data)
        # serializer_data["paragraphs"] = []
        # serializer_data["equations"] = []
        # serializer_data["images"] = []
        # paragraphset = Paragraph.objects.filter(
        #     chapter=chapter, section=section)
        # equationset = Equation.objects.filter(
        #     chapter=chapter, section=section)
        # imageset = Image.objects.filter(
        #     chapter=chapter, section=section)
        # for item in paragraphset:
        #     serializer_data["paragraphs"].append(item.paragraph)
        # for item in equationset:
        #     serializer_data["equations"].append(item.equation)
        # for item in imageset:
        #     serializer_data["images"].append(item.image)


class ContentDetailView(RetrieveAPIView):
    def get(self, request, chapter, section, format=None):
        chapterset = Chapter.objects.all()
        chapter_obj = get_object_or_404(chapterset, chapter=chapter)
        sectionset = Section.objects.filter(chapter=chapter_obj)
        section_obj = get_object_or_404(sectionset, section=section)
        serializer = SectionSerializer(section_obj)
        serializer_data = serializer.data
        serializer_data["chapter"] = chapter_obj.chapter
        serializer_data["chapterID"] = chapter_obj.id
        for index in range(len(sectionset)):
            if section_obj.id == sectionset[index].id:
                if section_obj.id != 1:  # and index != 0:
                    serializer_data["previous"] = sectionset[index - 1].section
                else:
                    serializer_data["previous"] = "none"
                if index != len(sectionset) - 1:
                    serializer_data["next"] = sectionset[index + 1].section
                else:
                    serializer_data["next"] = "none"
        serializer_data["paragraphs"] = []
        serializer_data["images"] = []
        serializer_data["imageIndex"] = []
        serializer_data["captions"] = []
        serializer_data["plots"] = []
        serializer_data["values"] = []
        paragraphset = Paragraph.objects.filter(
            chapter=chapter_obj, section=section_obj)
        imageset = Image.objects.filter(
            chapter=chapter_obj, section=section_obj)
        for item in paragraphset:
            serializer_data["paragraphs"].append(item.paragraph)
        for item in imageset:
            if str(item.section_image) != "":
                serializer_data["images"].append(item.section_image.url)
            else:
                serializer_data["images"].append(str(item.section_image))
            serializer_data["captions"].append(item.caption)
        if len(imageset) != 0:
            a = 1
            for item in imageset:
                if str(item.section_image) != "":
                    serializer_data["imageIndex"].append(str(a))
                    a += 1
                else:
                    serializer_data["imageIndex"].append("")
        return Response(serializer_data)


class ExerciseListView(RetrieveAPIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, chapter, section, format=None):
        chapterset = Chapter.objects.all()
        chapter_obj = get_object_or_404(chapterset, chapter=chapter)
        sectionset = Section.objects.filter(chapter=chapter_obj)
        section_obj = get_object_or_404(sectionset, section=section)
        serializer = SectionSerializer(section_obj)
        serializer_data = serializer.data
        serializer_data["chapter"] = chapter_obj.chapter
        serializer_data["chapterID"] = chapter_obj.id
        serializer_data["section"] = section_obj.section
        for index in range(len(sectionset)):
            if section_obj.id == sectionset[index].id:
                if section_obj.id != 1:
                    serializer_data["previous"] = sectionset[index - 1].section
                else:
                    serializer_data["previous"] = "none"
                if index != len(sectionset) - 1:
                    serializer_data["next"] = sectionset[index + 1].section
                else:
                    serializer_data["next"] = "none"
        serializer_data["exercises"] = []
        serializer_data["choices"] = []
        choice_list = []
        exerciseset = Exercise.objects.filter(
            chapter=chapter_obj)
        choiceset = Choice.objects.filter(
            chapter=chapter_obj)
        for item in exerciseset:
            serializer_data["exercises"].append(item.exercise)
        for item in choiceset:
            choice_list.append(item.choice_1)
            choice_list.append(item.choice_2)
            choice_list.append(item.choice_3)
            serializer_data["choices"].append(choice_list)
            choice_list = []
        return Response(serializer_data)


class ChoiceDetailView(RetrieveAPIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, chapter, section, pk, format=None):
        chapterset = Chapter.objects.all()
        chapter_obj = get_object_or_404(chapterset, chapter=chapter)
        sectionset = Section.objects.filter(chapter=chapter_obj)
        section_obj = get_object_or_404(sectionset, section=section)
        exerciseset = Exercise.objects.filter(section=section_obj)
        exercise_obj = get_object_or_404(exerciseset, id=pk)
        choiceset = Choice.objects.filter(
            chapter=chapter_obj, section=section_obj, exercise=exercise_obj)
        choice_obj = get_object_or_404(choiceset, exercise=exercise_obj)
        serializer = ChoiceSerializer(choice_obj)
        serializer_data = serializer.data
        return Response(serializer_data)


class ChoiceCheckView(UpdateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (permissions.AllowAny, )

    def put(self, request, chapter, section, pk, format=None):
        chapterset = Chapter.objects.all()
        chapter_obj = get_object_or_404(chapterset, chapter=chapter)
        sectionset = Section.objects.filter(chapter=chapter_obj)
        section_obj = get_object_or_404(sectionset, section=section)
        exerciseset = Exercise.objects.filter(section=section_obj)
        exercise_obj = get_object_or_404(exerciseset, id=pk)
        choiceset = Choice.objects.filter(
            chapter=chapter_obj, section=section_obj, exercise=exercise_obj)
        choice_obj = get_object_or_404(choiceset, exercise=exercise_obj)
        serializer = ChoiceSerializer(choice_obj)
        serializer_data = serializer.data
        answer = request.data['answer']
        if serializer_data["answer"] == answer:
            if serializer_data["comment_1"] == "" and serializer_data["equation_1"] == "" and serializer_data["comment_2"] == "" and serializer_data["equation_2"] == "":
                return Response("The choice is correct. Well done!")
            else:
                return Response(serializer_data)
        else:
            return Response("The choice is incorrect. Please try again.")


# class CodingInputView(UpdateAPIView):
#     serializer_class = CodingSerializer

#     def put(self, request, chapter, section, pk, format=None):
#         chapterset = Chapter.objects.all()
#         chapter_obj = get_object_or_404(chapterset, chapter=chapter)
#         sectionset = Section.objects.filter(chapter=chapter_obj)
#         section_obj = get_object_or_404(sectionset, section=section)
#         data_list = request.data["code"].split("\n")
#         temp_dict = {}
#         if len(data_list) == 1:
#             index = 0
#             pass
#         else:
#             for index in range(len(data_list) - 1, -1, -1):
#                 if data_list[index] != "":
#                     break
#         if "plt." in request.data["code"]:
#             local_path = '{0}/coding/{1}/{2}'.format(
#                 settings.MLEARN_ROOT, chapter, section)
#             if os.path.isdir(local_path) is False:
#                 os.makedirs(local_path)
#             if "plt.show()" in data_list:
#                 temp_dict["plot"] = request.data["code"].replace(
#                     "plt.show()", "")
#             else:
#                 temp_dict["plot"] = request.data["code"]
#             fig = plt.figure()
#             try:
#                 exec(temp_dict["plot"])
#                 if len(os.listdir(local_path)) != 0:
#                     os.remove('{0}/plot_{1}.png'.format(local_path, pk))
#                 fig.savefig(
#                     local_path + '/plot_{0}.png'.format(pk), format='png')
#                 temp_dict["plot"] = 'probability/coding/{0}/{1}/plot_{2}.png'.format(
#                     chapter, section, pk)
#                 obj, created = CodeText.objects.update_or_create(
#                     chapter=chapter_obj, section=section_obj,
#                     id=pk, defaults={'codetext': request.data["code"], 'plot': temp_dict["plot"], 'value': ""})
#             except Exception as inst:
#                 temp_dict['value'] = "{0}: {1}".format(type(inst), inst)
#                 obj, created = CodeText.objects.update_or_create(
#                     chapter=chapter_obj, section=section_obj,
#                     id=pk, defaults={'codetext': request.data["code"], 'plot': "", 'value': "{0}: {1}".format(type(inst), inst)})
#             return Response(temp_dict)
#         if "plt." not in data_list and "=" not in data_list[index]:
#             try:
#                 exec(request.data["code"])
#                 exec("temp_dict['value'] =" + data_list[index])
#                 if type(temp_dict['value']) == type:
#                     temp_dict['value'] = "<class '{0}'>".format(
#                         temp_dict['value'].__name__)
#                 obj, created = CodeText.objects.update_or_create(
#                     chapter=chapter_obj, section=section_obj,
#                     id=pk, defaults={'codetext': request.data["code"], 'plot': "", 'value': str(temp_dict["value"])})
#             except Exception as inst:
#                 temp_dict['value'] = "{0}: {1}".format(type(inst), inst)
#                 obj, created = CodeText.objects.update_or_create(
#                     chapter=chapter_obj, section=section_obj,
#                     id=pk, defaults={'codetext': request.data["code"], 'plot': "", 'value': temp_dict["value"]})
#             return Response(temp_dict)


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
