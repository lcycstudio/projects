from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.urls import static
from rest_framework.exceptions import ValidationError
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from . import settings
import registration.urls

import courses.urls
# import coding.urls
import quantum_mechanics.urls
import probability.urls

import apps.urls
import apps_math.urls
import apps_arithmetic.urls
import apps_physics.urls
import userprofile.urls
from rest_auth.views import PasswordResetView
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # path('accounts/', include('allauth.urls')),

    # url(r'^rest-auth/password/reset/$', PasswordResetView.as_view(),
    # name='rest_password_reset'),
    # path('rest-auth/', include('rest_auth.urls')),
    # path('rest-auth/registration/', include('rest_auth.registration.urls')),



    path('courses/', include(courses.urls)),  # courses


    path('quantummechanics/', include(quantum_mechanics.urls)),  # physics 11

    path('probability/',
         include(probability.urls)),  # machine learning app



    path('apps/', include(apps.urls)),  # apps

    path('apps_math/', include(apps_math.urls)),  # app_math

    path('apps_arithmetic/', include(apps_arithmetic.urls)),  # app_arithmetic

    path('apps_physics/', include(apps_physics.urls)),  # app_physics


    path('system/registration/', include(registration.urls)),  # django user
    path('userprofile/', include(userprofile.urls)),  # userprofile app
    # index html
    re_path(r'^.*', TemplateView.as_view(template_name='index.html')),
]

# urlpatterns += staticfiles_urlpatterns()
