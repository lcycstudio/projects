from django.conf.urls import url, include, re_path
from django.conf.urls.static import static
from django.urls import path
from e3studio import settings
from . import views

urlpatterns = [
    path('api/', include('apps.api.urls')),
]
