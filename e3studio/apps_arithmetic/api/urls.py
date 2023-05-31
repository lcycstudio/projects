from django.urls import path
from django.conf.urls import url

from .views import (
    AppsListView,
    AppsDetailView,
    AdditionRetrieveView,
    AdditionInputView,
    SubtractionRetrieveView,
    SubtractionInputView,
    MultiplicationRetrieveView,
    MultiplicationInputView,
    DivisionRetrieveView,
    DivisionInputView,
)

urlpatterns = [
    # chapter
    # path('input/', MathInputView.as_view()),
    path('list/', AppsListView.as_view()),
    path('<appname>/', AppsDetailView.as_view()),
    path('addition/<grade>/get/', AdditionRetrieveView.as_view()),
    path('addition/<grade>/put/', AdditionInputView.as_view()),
    path('subtraction/<grade>/get/', SubtractionRetrieveView.as_view()),
    path('subtraction/<grade>/put/', SubtractionInputView.as_view()),
    path('multiplication/<grade>/get/', MultiplicationRetrieveView.as_view()),
    path('multiplication/<grade>/put/', MultiplicationInputView.as_view()),
    path('division/<grade>/get/', DivisionRetrieveView.as_view()),
    path('division/<grade>/put/', DivisionInputView.as_view()),
]
