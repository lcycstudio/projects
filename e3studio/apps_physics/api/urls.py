from django.urls import path
from django.conf.urls import url

from .views import (
    # MathInputView,
    AppsPhysicsListView,
    OneAppDetailView,
    PMFInputView,
    BBInputView,
)

urlpatterns = [
    # chapter
    # path('input/', PhysicsInputView.as_view()),
    path('list/', AppsPhysicsListView.as_view()),
    path('<appname>/', OneAppDetailView.as_view()),
    path('aparticleinmagneticfield/put/', PMFInputView.as_view()),
    path('abouncingball/put/', BBInputView.as_view()),
    # path('Initial Value Problems/put/', IVPInputView.as_view()),

]
