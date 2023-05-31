from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.conf import settings
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
from apps_arithmetic.models import AppsArithmetic, Grade
from .serializers import InputSerializer, AppsArithmeticSerializer, OneAppSerializer, OneGradeSerializer
from .functions import additionFunc, subtractionFunc, multiplicationFunc, divisionFunc

# import os
import random
from fractions import Fraction
# import numpy as np
# import scipy as sp
# import pandas as pd
# import seaborn as sb
# from sympy import Symbol
# from sympy.solvers import solve
# from sympy.parsing.sympy_parser import parse_expr

# import base64
# import matplotlib.pyplot as plt
# from io import BytesIO
# from matplotlib.figure import Figure
# from apps_math.function import math_sf_find_y, get_yp, get_ypp, get_yppp, get_integral, RKF45, EulerSympletic


class AppsListView(ListAPIView):
    queryset = AppsArithmetic.objects.all()
    serializer_class = AppsArithmeticSerializer
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        appsarithmeticset = [item for item in AppsArithmetic.objects.all()]
        serializer = AppsArithmeticSerializer(appsarithmeticset, many=True)
        serializer_data = serializer.data
        for item in serializer_data:
            item["grades"] = []
            item["webs"] = []
            gradeset = Grade.objects.filter(
                appname=item["id"])
            if len(gradeset) != 0:
                for each in gradeset:
                    item["grades"].append(each.grade)
                    item["webs"].append(each.web)
        return Response(serializer_data)


class AppsDetailView(RetrieveAPIView):
    def get(self, request, appname, format=None):
        appset = AppsArithmetic.objects.all()
        app_obj = get_object_or_404(appset, appname=appname)
        serializer = OneAppSerializer(app_obj)
        serializer_data = serializer.data
        serializer_data["grades"] = []
        serializer_data["webs"] = []
        gradeset = Grade.objects.filter(appname=app_obj)
        for item in gradeset:
            serializer_data["grades"].append(item.grade)
            serializer_data["webs"].append(item.web)
        return Response(serializer_data)


class AdditionRetrieveView(RetrieveAPIView):
    queryset = AppsArithmetic.objects.all()
    serializer_class = OneGradeSerializer
    permission_classes = (permissions.AllowAny, )

    def get(self, request, grade, format=None):
        arithmeticset = AppsArithmetic.objects.all()
        arithmetic_obj = get_object_or_404(arithmeticset, appname='Addition')
        gradeset = Grade.objects.filter(appname=arithmetic_obj)
        grade_obj = get_object_or_404(gradeset, grade=grade)
        serializer = OneGradeSerializer(grade_obj)
        serializer_data = serializer.data
        serializer_data['appname'] = arithmetic_obj.appname
        serializer_data['appweb'] = arithmetic_obj.web
        list1 = []
        list2 = []
        list3 = []
        list_a = []
        list_b = []
        if 'Fractions' in grade:
            list1, list2, list_a, list_b = additionFunc(grade)
        else:
            list1, list2, list3 = additionFunc(grade)
        serializer_data['list'] = []
        serializer_data['listab'] = []
        if 'Fractions' in grade:
            for k in range(10):
                serializer_data['listab'].append(
                    '{0} + {1}'.format(list_a[k], list_b[k]))

        for k in range(10):
            serializer_data['list'].append(
                '{0} + {1}'.format(list1[k], list2[k]))
        if len(list3) != 0:
            serializer_data['list'] = []
            for k in range(10):
                serializer_data['list'].append(
                    '{0} + {1} + {2}'.format(list1[k], list2[k], list3[k]))

        for index in range(len(gradeset)):
            if grade_obj.id == gradeset[index].id:
                if grade_obj.id != 1 and index != 0:
                    serializer_data["previous"] = gradeset[index - 1].grade
                    serializer_data["prev_web"] = gradeset[index - 1].web
                else:
                    serializer_data["previous"] = "none"
                if index != len(gradeset) - 1:
                    serializer_data["next"] = gradeset[index + 1].grade
                    serializer_data["next_web"] = gradeset[index + 1].web
                else:
                    serializer_data["next"] = "none"
        return Response(serializer_data)


class AdditionInputView(UpdateAPIView):
    queryset = AppsArithmetic.objects.all()
    serializer_class = InputSerializer
    permission_classes = (permissions.AllowAny, )

    def put(self, request, grade, format=None):
        arithmeticset = AppsArithmetic.objects.all()
        arithmetic_obj = get_object_or_404(arithmeticset, appname='Addition')
        gradeset = Grade.objects.filter(appname=arithmetic_obj)
        grade_obj = get_object_or_404(gradeset, grade=grade)
        serializer = OneGradeSerializer(grade_obj)
        new_dict = {}
        new_dict['id'] = grade_obj.id
        new_dict['appname'] = arithmetic_obj.appname
        new_dict['grade'] = grade_obj.grade
        new_dict['list'] = []
        new_dict['input'] = []
        new_dict['answer'] = []
        new_dict['check'] = []
        data_list = request.data
        for key in data_list:
            if len(data_list[key]) != 0:
                equal_i = data_list[key].index('=') - 1
                equal_j = data_list[key].index('=') + 2
                new_dict['list'].append(str(data_list[key])[:equal_i])
                new_dict['input'].append(str(data_list[key])[equal_j:])
            else:
                new_dict['list'].append('')
                new_dict['input'].append('')
        for k in range(len(new_dict['list'])):
            if new_dict['list'][k] != '':
                if 'Decimals' in grade:
                    new_dict['answer'].append(
                        round(eval(new_dict['list'][k]), 3))
                elif 'Fractions' in grade:
                    new_dict['answer'].append(
                        str(Fraction(eval(new_dict['list'][k])).limit_denominator()))
                else:
                    new_dict['answer'].append(eval(new_dict['list'][k]))
            else:
                new_dict['answer'].append(new_dict['list'][k])
        a = 0
        for k in range(len(new_dict['answer'])):
            if 'Decimals' in grade:
                if new_dict['answer'][k] == round(eval(new_dict['input'][k]), 3):
                    new_dict['check'].append('check')
                    a = a + 1
                else:
                    new_dict['check'].append('close')
            if 'Fractions' in grade:
                if 'Grade 5' in grade:
                    if new_dict['answer'][k] == new_dict['input'][k]:
                        new_dict['check'].append('check')
                        a = a + 1
                    else:
                        new_dict['check'].append('close')
                else:
                    if eval(new_dict['answer'][k]) == eval(new_dict['input'][k]):
                        new_dict['check'].append('check')
                        a = a + 1
                    else:
                        new_dict['check'].append('close')
            else:
                if new_dict['answer'][k] == eval(new_dict['input'][k]):
                    new_dict['check'].append('check')
                    a = a + 1
                else:
                    new_dict['check'].append('close')
        new_dict['score'] = a
        return Response(new_dict)


class SubtractionRetrieveView(RetrieveAPIView):
    queryset = AppsArithmetic.objects.all()
    serializer_class = OneGradeSerializer
    permission_classes = (permissions.AllowAny, )

    def get(self, request, grade, format=None):
        arithmeticset = AppsArithmetic.objects.all()
        arithmetic_obj = get_object_or_404(
            arithmeticset, appname='Subtraction')
        gradeset = Grade.objects.filter(appname=arithmetic_obj)
        grade_obj = get_object_or_404(gradeset, grade=grade)
        serializer = OneGradeSerializer(grade_obj)
        serializer_data = serializer.data
        serializer_data['appname'] = arithmetic_obj.appname
        serializer_data['appweb'] = arithmetic_obj.web
        list1 = []
        list2 = []
        list3 = []
        list_a = []
        list_b = []
        if 'Fractions' in grade:
            list1, list2, list_a, list_b = subtractionFunc(grade)
        else:
            list1, list2, list3 = subtractionFunc(grade)
        serializer_data['list'] = []
        serializer_data['listab'] = []
        if 'Fractions' in grade:
            for k in range(10):
                serializer_data['listab'].append(
                    '{0} - {1}'.format(list_a[k], list_b[k]))
        for k in range(10):
            serializer_data['list'].append(
                '{0} - {1}'.format(list1[k], list2[k]))
        if len(list3) != 0:
            serializer_data['list'] = []
            for k in range(10):
                serializer_data['list'].append(
                    '{0} - {1} - {2}'.format(list1[k], list2[k], list3[k]))

        for index in range(len(gradeset)):
            if grade_obj.id == gradeset[index].id:
                if grade_obj.id != 1 and index != 0:
                    serializer_data["previous"] = gradeset[index - 1].grade
                    serializer_data["prev_web"] = gradeset[index - 1].web
                else:
                    serializer_data["previous"] = "none"
                if index != len(gradeset) - 1:
                    serializer_data["next"] = gradeset[index + 1].grade
                    serializer_data["next_web"] = gradeset[index + 1].web
                else:
                    serializer_data["next"] = "none"
        return Response(serializer_data)


class SubtractionInputView(UpdateAPIView):
    queryset = AppsArithmetic.objects.all()
    serializer_class = InputSerializer
    permission_classes = (permissions.AllowAny, )

    def put(self, request, grade, format=None):
        arithmeticset = AppsArithmetic.objects.all()
        arithmetic_obj = get_object_or_404(
            arithmeticset, appname='Subtraction')
        gradeset = Grade.objects.filter(appname=arithmetic_obj)
        grade_obj = get_object_or_404(gradeset, grade=grade)
        serializer = OneGradeSerializer(grade_obj)
        new_dict = {}
        new_dict['id'] = grade_obj.id
        new_dict['appname'] = arithmetic_obj.appname
        new_dict['grade'] = grade_obj.grade
        new_dict['list'] = []
        new_dict['input'] = []
        new_dict['answer'] = []
        new_dict['check'] = []
        data_list = request.data
        for key in data_list:
            if len(data_list[key]) != 0:
                equal_i = data_list[key].index('=') - 1
                equal_j = data_list[key].index('=') + 2
                new_dict['list'].append(str(data_list[key])[:equal_i])
                new_dict['input'].append(str(data_list[key])[equal_j:])
            else:
                new_dict['list'].append('')
                new_dict['input'].append('')
        for k in range(len(new_dict['list'])):
            if new_dict['list'][k] != '':
                if 'Decimals' in grade:
                    new_dict['answer'].append(
                        round(eval(new_dict['list'][k]), 3))
                elif 'Fractions' in grade:
                    new_dict['answer'].append(
                        str(Fraction(eval(new_dict['list'][k])).limit_denominator()))
                else:
                    new_dict['answer'].append(eval(new_dict['list'][k]))
            else:
                new_dict['answer'].append(new_dict['list'][k])
        a = 0
        for k in range(len(new_dict['answer'])):
            if 'Decimals' in grade:
                if new_dict['answer'][k] == round(eval(new_dict['input'][k]), 3):
                    new_dict['check'].append('check')
                    a = a + 1
                else:
                    new_dict['check'].append('close')
            if 'Fractions' in grade:
                if eval(new_dict['answer'][k]) == eval(new_dict['input'][k]):
                    new_dict['check'].append('check')
                    a = a + 1
                else:
                    new_dict['check'].append('close')
            else:
                if new_dict['answer'][k] == eval(new_dict['input'][k]):
                    new_dict['check'].append('check')
                    a = a + 1
                else:
                    new_dict['check'].append('close')
        new_dict['score'] = a
        return Response(new_dict)


class MultiplicationRetrieveView(RetrieveAPIView):
    queryset = AppsArithmetic.objects.all()
    serializer_class = OneGradeSerializer
    permission_classes = (permissions.AllowAny, )

    def get(self, request, grade, format=None):
        arithmeticset = AppsArithmetic.objects.all()
        arithmetic_obj = get_object_or_404(
            arithmeticset, appname='Multiplication')
        gradeset = Grade.objects.filter(appname=arithmetic_obj)
        grade_obj = get_object_or_404(gradeset, grade=grade)
        serializer = OneGradeSerializer(grade_obj)
        serializer_data = serializer.data
        serializer_data['appname'] = arithmetic_obj.appname
        serializer_data['appweb'] = arithmetic_obj.web
        list1 = []
        list2 = []
        list_a = []
        list_b = []
        if 'Fractions' in grade:
            list1, list2, list_a, list_b = subtractionFunc(grade)
        else:
            list1, list2 = multiplicationFunc(grade)
        serializer_data['list'] = []
        serializer_data['listab'] = []
        if 'Fractions' in grade:
            for k in range(10):
                serializer_data['listab'].append(
                    '{0} x {1}'.format(list_a[k], list_b[k]))
        for k in range(10):
            serializer_data['list'].append(
                '{0} \\times {1}'.format(list1[k], list2[k]))
        for index in range(len(gradeset)):
            if grade_obj.id == gradeset[index].id:
                if grade_obj.id != 1 and index != 0:
                    serializer_data["previous"] = gradeset[index - 1].grade
                    serializer_data["prev_web"] = gradeset[index - 1].web
                else:
                    serializer_data["previous"] = "none"
                if index != len(gradeset) - 1:
                    serializer_data["next"] = gradeset[index + 1].grade
                    serializer_data["next_web"] = gradeset[index + 1].web
                else:
                    serializer_data["next"] = "none"
        return Response(serializer_data)


class MultiplicationInputView(UpdateAPIView):
    queryset = AppsArithmetic.objects.all()
    serializer_class = InputSerializer
    permission_classes = (permissions.AllowAny, )

    def put(self, request, grade, format=None):
        arithmeticset = AppsArithmetic.objects.all()
        arithmetic_obj = get_object_or_404(
            arithmeticset, appname='Multiplication')
        gradeset = Grade.objects.filter(appname=arithmetic_obj)
        grade_obj = get_object_or_404(gradeset, grade=grade)
        serializer = OneGradeSerializer(grade_obj)
        new_dict = {}
        new_dict['id'] = grade_obj.id
        new_dict['appname'] = arithmetic_obj.appname
        new_dict['grade'] = grade_obj.grade
        new_dict['list'] = []
        new_dict['input'] = []
        new_dict['answer'] = []
        new_dict['check'] = []
        data_list = request.data
        for key in data_list:
            if len(data_list[key]) != 0:
                equal_i = data_list[key].index('=') - 1
                equal_j = data_list[key].index('=') + 2
                new_dict['list'].append(str(data_list[key])[:equal_i])
                new_dict['input'].append(str(data_list[key])[equal_j:])
            else:
                new_dict['list'].append('')
                new_dict['input'].append('')
        for i in range(len(new_dict['list'])):
            new_dict['list'][i] = new_dict['list'][i].replace('\\times', '*')
        for k in range(len(new_dict['list'])):
            if new_dict['list'][k] != '':
                if 'Decimals' in grade:
                    new_dict['answer'].append(
                        round(eval(new_dict['list'][k]), 3))
                elif 'Fractions' in grade:
                    new_dict['answer'].append(
                        str(Fraction(eval(new_dict['list'][k])).limit_denominator()))
                else:
                    new_dict['answer'].append(eval(new_dict['list'][k]))
            else:
                new_dict['answer'].append(new_dict['list'][k])
        a = 0
        for k in range(len(new_dict['answer'])):
            if 'Decimals' in grade:
                if new_dict['answer'][k] == round(eval(new_dict['input'][k]), 3):
                    new_dict['check'].append('check')
                    a = a + 1
                else:
                    new_dict['check'].append('close')
            if 'Fractions' in grade:
                if eval(new_dict['answer'][k]) == eval(new_dict['input'][k]):
                    new_dict['check'].append('check')
                    a = a + 1
                else:
                    new_dict['check'].append('close')
            else:
                if new_dict['answer'][k] == eval(new_dict['input'][k]):
                    new_dict['check'].append('check')
                    a = a + 1
                else:
                    new_dict['check'].append('close')
        new_dict['score'] = a
        return Response(new_dict)


class DivisionRetrieveView(RetrieveAPIView):
    queryset = AppsArithmetic.objects.all()
    serializer_class = OneGradeSerializer
    permission_classes = (permissions.AllowAny, )

    def get(self, request, grade, format=None):
        arithmeticset = AppsArithmetic.objects.all()
        arithmetic_obj = get_object_or_404(
            arithmeticset, appname='Division')
        gradeset = Grade.objects.filter(appname=arithmetic_obj)
        grade_obj = get_object_or_404(gradeset, grade=grade)
        serializer = OneGradeSerializer(grade_obj)
        serializer_data = serializer.data
        serializer_data['appname'] = arithmetic_obj.appname
        serializer_data['appweb'] = arithmetic_obj.web
        list1 = []
        list2 = []
        list1, list2 = divisionFunc(grade)
        # if 'Fractions' in grade:
        #     list1, list2, list_a, list_b = divisionFunc(grade)
        # else:

        serializer_data['list'] = []
        # serializer_data['listab'] = []
        # if 'Fractions' in grade:
        #     for k in range(10):
        #         serializer_data['listab'].append(
        #             '{0} \\div {1}'.format(list_a[k], list_b[k]))
        for k in range(10):
            serializer_data['list'].append(
                '{0} \\div {1}'.format(list1[k], list2[k]))
        for index in range(len(gradeset)):
            if grade_obj.id == gradeset[index].id:
                if grade_obj.id != 1 and index != 0:
                    serializer_data["previous"] = gradeset[index - 1].grade
                    serializer_data["prev_web"] = gradeset[index - 1].web
                else:
                    serializer_data["previous"] = "none"
                if index != len(gradeset) - 1:
                    serializer_data["next"] = gradeset[index + 1].grade
                    serializer_data["next_web"] = gradeset[index + 1].web
                else:
                    serializer_data["next"] = "none"
        return Response(serializer_data)


class DivisionInputView(UpdateAPIView):
    queryset = AppsArithmetic.objects.all()
    serializer_class = InputSerializer
    permission_classes = (permissions.AllowAny, )

    def put(self, request, grade, format=None):
        arithmeticset = AppsArithmetic.objects.all()
        arithmetic_obj = get_object_or_404(
            arithmeticset, appname='Division')
        gradeset = Grade.objects.filter(appname=arithmetic_obj)
        grade_obj = get_object_or_404(gradeset, grade=grade)
        serializer = OneGradeSerializer(grade_obj)
        new_dict = {}
        new_dict['id'] = grade_obj.id
        new_dict['appname'] = arithmetic_obj.appname
        new_dict['grade'] = grade_obj.grade
        new_dict['list'] = []
        new_dict['list_r'] = []
        new_dict['input'] = []
        new_dict['answer'] = []
        new_dict['answer_r'] = []
        new_dict['check'] = []
        data_list = request.data
        for key in data_list:
            if len(data_list[key]) != 0:
                equal_i = data_list[key].index('=') - 1
                equal_j = data_list[key].index('=') + 2
                new_dict['list'].append(str(data_list[key])[:equal_i])
                new_dict['input'].append(str(data_list[key])[equal_j:])
            else:
                new_dict['list'].append('')
                new_dict['input'].append('')
        for i in range(len(new_dict['list'])):
            new_dict['list'][i] = new_dict['list'][i].replace('\\div', '//')

        if 'Remainder' in grade:
            for i in range(len(new_dict['list'])):
                new_dict['list_r'].append(
                    new_dict['list'][i].replace('//', '%'))

        for k in range(len(new_dict['list'])):
            if new_dict['list'][k] != '':
                new_dict['answer'].append(str(eval(new_dict['list'][k])))
                if 'Remainder' in grade:
                    new_dict['answer_r'].append(
                        str(eval(new_dict['list_r'][k])))
            else:
                new_dict['answer'].append(new_dict['list'][k])
        if 'Remainder' in grade:
            for k in range(len(new_dict['answer'])):
                new_dict['answer'][k] = new_dict['answer'][k] + \
                    'R' + new_dict['answer_r'][k]
        a = 0
        for k in range(len(new_dict['answer'])):
            if 'Remainder' in grade:
                if '0' in new_dict['answer'][k]:
                    if new_dict['answer'][k].replace('R0', '') == new_dict['input'][k].upper().replace('R0', ''):
                        new_dict['check'].append('check')
                        a = a + 1
                    else:
                        new_dict['check'].append('close')
                else:
                    if new_dict['answer'][k] == new_dict['input'][k].upper():
                        new_dict['check'].append('check')
                        a = a + 1
                    else:
                        new_dict['check'].append('close')
            else:
                if eval(new_dict['answer'][k]) == eval(new_dict['input'][k]):
                    new_dict['check'].append('check')
                    a = a + 1
                else:
                    new_dict['check'].append('close')
        new_dict['score'] = a
        return Response(new_dict)


# class CodingInputView(UpdateAPIView):
#     serializer_class = CodingSerializer

#     def put(self, request, format=None):
#         data_list = request.data["code"].split("\r\n")
#         temp_dict = {}

    # def get(self, request, app, format=None):
    #     appset = AppsMath.objects.all()
    #     app_obj = get_object_or_404(appset, appname=app)
    #     functionset = Function.objects.all()
    #     parameterset = Parameter.objects.all()
    #     initialfunctionset = InitialFunctionValue.objects.filter(
    #         appname=app_obj)
    #     initialderivativeset = InitialDerivativeValue.objects.filter(
    #         appname=app_obj)
    #     leftboundset = LeftBound.objects.all()
    #     rightboundset = RightBound.objects.all()
    #     titleset = Title.objects.all()
    #     hlset = HorizontalLabel.objects.all()
    #     vlset = VerticalLabel.objects.all()
    #     function_obj = get_object_or_404(functionset, appname=app_obj)
    #     parameter_obj = get_object_or_404(parameterset, appname=app_obj)
    #     leftbound_obj = get_object_or_404(leftboundset, appname=app_obj)
    #     rightbound_obj = get_object_or_404(rightboundset, appname=app_obj)
    #     title_obj = get_object_or_404(titleset, appname=app_obj)
    #     hl_obj = get_object_or_404(hlset, appname=app_obj)
    #     vl_obj = get_object_or_404(vlset, appname=app_obj)
    #     if len(initialfunctionset) != 0:
    #         initial_obj = get_object_or_404(
    #             initialfunctionset, appname=app_obj)
    #         app_list = [function_obj, parameter_obj, initial_obj, leftbound_obj,
    #                     rightbound_obj, title_obj, hl_obj, vl_obj]
    #         if len(initialderivativeset) != 0:
    #             initialder_obj = get_object_or_404(
    #                 initialderivativeset, appname=app_obj)
    #             app_list = [function_obj, parameter_obj, initial_obj, initialder_obj, leftbound_obj,
    #                         rightbound_obj, title_obj, hl_obj, vl_obj]
    #     else:
    #         app_list = [function_obj, parameter_obj, leftbound_obj,
    #                     rightbound_obj, title_obj, hl_obj, vl_obj]
    #     serializer = OneAppMathSerializer(app_list, many=True)
    #     serializer_data = serializer.data
    #     index = 0
    #     for item in serializer_data:
    #         item["appname"] = app_list[index].appname.appname
    #         index = index + 1
    #     return Response(serializer_data)


# class MathInputView(UpdateAPIView):
#     serializer_class = CodingSerializer

#     def put(self, request, format=None):
#         data_list = request.data["code"].split("\r\n")
#         temp_dict = {}
#         if len(data_list) == 1:
#             index = 0
#             pass
#         else:
#             for index in range(len(data_list) - 1, 0, -1):
#                 if data_list[index] != "":
#                     pass
#         if "plt." in request.data["code"]:
#             local_path = '{0}/python'.format(settings.CODING_ROOT)
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
#                 if len(os.listdir(local_path)) == 1:
#                     os.remove('{0}/{1}'.format(local_path,
#                                                os.listdir(local_path)[0]))
#                 fig.savefig(local_path + '/plot.png', format='png')
#                 temp_dict["plot"] = 'coding/mediafiles/coding/python/plot.png'
#             except Exception as inst:
#                 temp_dict['error'] = "{0}: {1}".format(type(inst), inst)
#             return Response(temp_dict)
#         if "plt." not in data_list and "=" not in data_list[index]:
#             # print(data_list)
#             try:
#                 exec(request.data["code"])
#                 exec("temp_dict['val'] =" + data_list[index])
#             except Exception as inst:
#                 temp_dict['error'] = "{0}: {1}".format(type(inst), inst)
#             return Response(temp_dict)
