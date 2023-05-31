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
from .serializers import CodingSerializer
from apps_physics.models import AppsPhysics
from .serializers import AppsPhysicsSerializer, OneAppSerializer, PMFSerializer, BBSerializer, CFSerializer, ODESerializer

import os
import numpy as np
import scipy as sp
import pandas as pd
import seaborn as sb
# from sympy import Symbol
# from sympy.solvers import solve
# from sympy.parsing.sympy_parser import parse_expr

import base64
import matplotlib.pyplot as plt
from io import BytesIO
from matplotlib.figure import Figure
from apps_physics.function import particle, bounce  # , acc1, acc2, acc3


class AppsPhysicsListView(ListAPIView):
    queryset = AppsPhysics.objects.all()
    serializer_class = AppsPhysicsSerializer
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        appsPhysicsset = [item for item in AppsPhysics.objects.all()]
        serializer = AppsPhysicsSerializer(appsPhysicsset, many=True)
        serializer_data = serializer.data
        return Response(serializer_data)


class OneAppDetailView(RetrieveAPIView):

    def get(self, request, appname, format=None):
        appset = AppsPhysics.objects.all()
        app_obj = get_object_or_404(appset, appname=appname)
        serializer = OneAppSerializer(app_obj)
        serializer_data = serializer.data
        return Response(serializer_data)


# A Particle in Magnetic Field
class PMFInputView(UpdateAPIView):
    serializer_class = PMFSerializer

    def put(self, request, format=None):
        entryList = [9.1094e-31, 1.602e-19, 1e-12, 2, 'z']
        index = 0
        # print(request.data)
        for key in request.data:
            if request.data[key] != "":
                entryList[index] = request.data[key]
            index += 1
        mass = float(entryList[0])
        charge = float(entryList[1])
        magnet = float(entryList[2])
        speed = float(entryList[3])
        direction = entryList[4]
        w = charge * magnet / mass
        x, y, z = particle(w, speed, direction)
        serializer = PMFSerializer()
        serializer_data = serializer.data
        serializer_data['mass'] = entryList[0]
        serializer_data['charge'] = entryList[1]
        serializer_data['magnet'] = entryList[2]
        serializer_data['speed'] = entryList[3]
        serializer_data['direction'] = entryList[4]
        serializer_data['xdata'] = x
        serializer_data['ydata'] = y
        serializer_data['zdata'] = z
        return Response(serializer_data)


class BBInputView(UpdateAPIView):
    serializer_class = BBSerializer

    def put(self, request, format=None):
        entryList = [10, 0, 20, 9.8, 0, 0.75, 20, 0.1, 20, 'clockwise']
        index = 0
        for key in request.data:
            if request.data[key] != "":
                entryList[index] = request.data[key]
            index += 1
        h0 = entryList[0]
        vver = entryList[1]
        vhi = entryList[2]
        grav = entryList[3]
        airr = entryList[4]
        rho = entryList[5]
        w = entryList[6]
        r = entryList[7]
        af = entryList[8]
        ccw = entryList[9]
        D, H, W, T = bounce(h0, vver, vhi, grav, airr, rho, w, r, af, ccw)
        serializer = BBSerializer()
        serializer_data = serializer.data
        index = 0
        for item in serializer_data:
            serializer_data[item] = entryList[index]
            index += 1

        serializer_data['xdata'] = D
        serializer_data['ydata'] = H
        serializer_data['wdata'] = W
        serializer_data['tdata'] = T
        return Response(serializer_data)


# class AppsPhysicsDetailView(RetrieveAPIView):
#     queryset = AppsPhysics.objects.all()
#     serializer_class = OneAppMathSerializer
#     permission_classes = (permissions.AllowAny, )

#     def get(self, request, app, format=None):
#         appset = AppsPhysics.objects.all()
#         app_obj = get_object_or_404(appset, appname=app)
#         functionset = Function.objects.all()
#         parameterset = Parameter.objects.all()
#         initialfunctionset = InitialFunctionValue.objects.filter(
#             appname=app_obj)
#         initialderivativeset = InitialDerivativeValue.objects.filter(
#             appname=app_obj)
#         leftboundset = LeftBound.objects.all()
#         rightboundset = RightBound.objects.all()
#         titleset = Title.objects.all()
#         hlset = HorizontalLabel.objects.all()
#         vlset = VerticalLabel.objects.all()
#         function_obj = get_object_or_404(functionset, appname=app_obj)
#         parameter_obj = get_object_or_404(parameterset, appname=app_obj)
#         leftbound_obj = get_object_or_404(leftboundset, appname=app_obj)
#         rightbound_obj = get_object_or_404(rightboundset, appname=app_obj)
#         title_obj = get_object_or_404(titleset, appname=app_obj)
#         hl_obj = get_object_or_404(hlset, appname=app_obj)
#         vl_obj = get_object_or_404(vlset, appname=app_obj)
#         app_list = [function_obj, parameter_obj, leftbound_obj,
#                     rightbound_obj, title_obj, hl_obj, vl_obj]
#         if len(initialfunctionset) != 0:
#             initial_obj = get_object_or_404(
#                 initialfunctionset, appname=app_obj)
#             app_list = [function_obj, parameter_obj, initial_obj, leftbound_obj,
#                         rightbound_obj, title_obj, hl_obj, vl_obj]
#         if len(initialderivativeset) != 0:
#             initialder_obj = get_object_or_404(
#                 initialderivativeset, appname=app_obj)
#             app_list = [function_obj, parameter_obj, initial_obj, initialder_obj, leftbound_obj,
#                         rightbound_obj, title_obj, hl_obj, vl_obj]

#         serializer = OneAppMathSerializer(app_list, many=True)
#         serializer_data = serializer.data
#         index = 0
#         for item in serializer_data:
#             item["appname"] = app_list[index].appname.appname
#             index = index + 1
#         return Response(serializer_data)


class CFInputView(UpdateAPIView):
    serializer_class = CFSerializer

    # fig, ax = plt.subplots()

    def put(self, request, format=None):
        entryList = ['', 'x', '-10', '10', '', 'x', 'y', '0', '', '']
        index = 0
        # print(request.data)
        for key in request.data:
            if request.data[key] != "":
                entryList[index] = request.data[key]
            index += 1
        # print(entryList)
        # Getting values
        left_bound = float(eval(entryList[2]))
        right_bound = float(eval(entryList[3]))
        # Grids, function and parameter
        N = 1001  # number of data points
        h = (right_bound - left_bound) / (N - 1)  # grid size
        x = np.arange(left_bound, right_bound + h, h)
        function = entryList[0]
        parameter = entryList[1]
        function = function.replace(parameter, "x", function.count(parameter))
        esIndex = function.index("=")  # equal sign index
        # Start Plotting Simple Function
        fig = Figure()
        ax = fig.subplots()
        if 'x' in function:
            function_array = eval(function[esIndex + 1:len(function)])
        else:
            function_array = np.ones(
                1001) * float(function[esIndex + 1:len(function)])
        # print(entryList[7])
        if entryList[7] == '0':
            ax.plot(x, function_array, label=r"$y$")
        if entryList[7] == '1':
            yp = get_yp(N, x, h, function_array)
            ax.plot(x, function_array, label=r"$y$")
            ax.plot(x, yp, label=r"$y^{\prime}$")
        if entryList[7] == '2':
            ypp = get_ypp(N, x, h, function_array)
            ax.plot(x, function_array, label=r"$y$")
            ax.plot(x, ypp, label=r"$y^{\prime \prime}$")
        if entryList[7] == '3':
            yp = get_yp(N, x, h, function_array)
            ypp = get_ypp(N, x, h, function_array)
            ax.plot(x, yp, label=r"$y^{\prime}$")
            ax.plot(x, ypp, label=r"$y^{\prime \prime}$")
        if entryList[7] == '4':
            yp = get_yp(N, x, h, function_array)
            ypp = get_ypp(N, x, h, function_array)
            ax.plot(x, function_array, label=r"$y$")
            ax.plot(x, yp, label=r"$y^{\prime}$")
            ax.plot(x, ypp, label=r"$y^{\prime \prime}$")

        findyvalue = ""
        if entryList[7] == '5':
            x_array = x
            x = float(entryList[8])
            findyvalue = round(eval(function[esIndex + 1:len(function)]), 4)
            ax.plot(x_array, function_array, label=r"$y$")

        findxvalue = ""
        if entryList[7] == '6':
            x_array = x
            y = float(entryList[9])
            findxvalue = str(math_sf_find_y(function, function_array, x, y))
            # x = Symbol('x')
            # function = function[esIndex + 1:len(function)] + '-' + str(y)
            # if "np." in function:
            #     function = function.replace("np.", "")
            #     f = parse_expr(function)
            #     result = solve(f, x)
            # else:
            #     result = solve(eval(function), x)
            # print(result)
            # findxvalue = ""
            # if len(result) > 1:
            #     for item in result:
            #         findxvalue = findxvalue + str(round(item, 4)) + ', '
            #     findxvalue = findxvalue[:-2]
            # else:
            #     findxvalue = str(round(float(result[0]), 4))
            ax.plot(x_array, function_array, label=r"$y$")

        ax.set(title=r'${0}$'.format(
            entryList[4]), xlabel=entryList[5], ylabel=entryList[6])
        ax.grid()
        ax.legend()
        # Save it to a temporary buffer.
        buf = BytesIO()
        fig.savefig(buf, format='png')
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        serializer = CFSerializer()
        serializer_data = serializer.data
        serializer_data['function'] = ""
        serializer_data['parameter'] = entryList[1]
        serializer_data['left_bound'] = entryList[2]
        serializer_data['right_bound'] = entryList[3]
        serializer_data['title'] = entryList[4]
        serializer_data['hlabel'] = entryList[5]
        serializer_data['vlabel'] = entryList[6]
        serializer_data['forxvalue'] = findyvalue
        serializer_data['foryvalue'] = findxvalue
        serializer_data['figure'] = f"data:img/png;base64,{data}"
        return Response(serializer_data)


class IVPInputView(UpdateAPIView):
    serializer_class = ODESerializer

    def put(self, request, format=None):
        entryList = ['', 't', '', '', '0', '10', '', 't', 'y', '0', '', '']
        index = 0
        for key in request.data:
            if request.data[key] != "":
                entryList[index] = request.data[key]
            index += 1
        # print(entryList)
        # Getting values
        left_bound = float(eval(entryList[4]))
        right_bound = float(eval(entryList[5]))
        # Grids, function and parameter
        # N = 1001  # number of data points
        # h = (right_bound - left_bound) / (N - 1)  # grid size
        # x = np.arange(left_bound, right_bound + h, h)
        function = entryList[0][0]
        parameter = entryList[1]
        function = function.replace(parameter, "t", function.count(parameter))
        esIndex = function.index("=")  # equal sign index
        # function = form_data[0]
        # parameter = form_data[14]
        # function = function.replace(parameter,"t",function.count(parameter))
        # esIndex = function.index("=") # equal sign index
        fun = function[esIndex + 1:]
        if entryList[0][1] == '1':
            t, y, v, ypp, h = RKF45(
                fun, eval(entryList[2]), left_bound, right_bound, 1e-12)
        elif entryList[0][1] == '2':
            t, y, v, h = EulerSympletic(fun, eval(entryList[2]), eval(
                entryList[3]), left_bound, right_bound, 1000)
        # Start Plotting Simple Function
        fig = Figure()
        ax = fig.subplots()
        if entryList[9] == '0':
            ax.plot(t, y, label=r"$y$")
        if entryList[9] == '1':
            ax.plot(t, y, label=r"$y$")
            ax.plot(t, v, label=r"$y^{\prime}$")
        if entryList[9] == '2':
            if entryList[0][1] == '2':
                ypp = get_ypp(len(t), t, h, y)
            ax.plot(t, y, label=r"$y$")
            ax.plot(t[3:], ypp[3:], label=r"$y^{\prime \prime}$")
        if entryList[9] == '3':
            if entryList[0][1] == '2':
                ypp = get_ypp(len(t), t, h, y)
            ax.plot(t, v, label=r"$y^{\prime}$")
            ax.plot(t[3:], ypp[3:], label=r"$y^{\prime \prime}$")
        if entryList[9] == '4':
            if entryList[0][1] == '2':
                ypp = get_ypp(len(t), t, h, y)
            ax.plot(t, y, label=r"$y$")
            ax.plot(t, v, label=r"$y^{\prime}$")
            ax.plot(t[3:], ypp[3:], label=r"$y^{\prime \prime}$")

        findyvalue = ""
        if entryList[9] == '5':
            new_t = []
            for i in t:
                new_t.append(np.abs(entryList[10] - i))
            findyvalue = round(y[new_t.index(min(new_t))], 4)
            ax.plot(t, y, label=r"$y$")

        findxvalue = ""
        if entryList[9] == '6':
            new_y = []
            for j in y:
                new_y.append(np.abs(entryList[11] - j))
            findxvalue = round(t[new_y.index(min(new_y))], 4)
            ax.plot(t, y, label=r"$y$")

        ax.set(title=r'${0}$'.format(
            entryList[6]), xlabel=entryList[7], ylabel=entryList[8])
        ax.grid()
        ax.legend()
        # Save it to a temporary buffer.
        buf = BytesIO()
        fig.savefig(buf, format='png')
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        serializer = ODESerializer()
        serializer_data = serializer.data
        serializer_data['equation'] = ""
        serializer_data['parameter'] = entryList[1]
        serializer_data['ifv'] = entryList[2]
        serializer_data['idv'] = entryList[3]
        serializer_data['left_bound'] = entryList[4]
        serializer_data['right_bound'] = entryList[5]
        serializer_data['title'] = entryList[6]
        serializer_data['hlabel'] = entryList[7]
        serializer_data['vlabel'] = entryList[8]
        # serializer_data['option'] = entryList[9]
        serializer_data['forxvalue'] = findyvalue
        serializer_data['foryvalue'] = findxvalue
        serializer_data['figure'] = f"data:img/png;base64,{data}"
        return Response(serializer_data)


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
