from django.urls import path
from django.conf.urls import url

from .views import (
    AppListView,
    AppDetailView,
    # MessageSendView,
)

urlpatterns = [
    path('list/', AppListView.as_view()),
    path('<appname>/', AppDetailView.as_view()),
    # path('message/', MessageSendView.as_view()),
]
