from django.urls import path
from django.conf.urls import url

from .views import (
    # MathInputView,
    AppsMathListView,
    AppsMathDetailView,
    CFInputView,
    IVPInputView,
)

urlpatterns = [
    # chapter
    # path('input/', MathInputView.as_view()),
    path('list/', AppsMathListView.as_view()),
    path('<app>/', AppsMathDetailView.as_view()),
    path('commonfunctions/put/', CFInputView.as_view()),
    path('initialvalueproblems/put/', IVPInputView.as_view()),

]
