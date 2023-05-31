# from marketplace.api.views import ItemCategoryViewSet
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'', ItemCategoryViewSet, basename='articles')  # path to api
# urlpatterns = router.urls

from django.urls import path
from django.conf.urls import url

from .views import (
    ProfileListView,
    ProfileDetailView,
    CourseCheckView,
    # SectionDetailView,
    # ItemCategoryCreateView,
    # ItemPlatformListView,
    # ItemPlatformDetailView,
    # ItemPlatformCreateView,
    # ItemInstanceUserList,
    # ItemInstanceDetailView,
)

urlpatterns = [
    # profiles
    path('profiles/', ProfileListView.as_view()),
    path('profiles/check/', CourseCheckView.as_view()),
    path('profiles/<token>/', ProfileDetailView.as_view()),

    # path('<subject>/<chapter>/<section>/', SectionDetailView.as_view()),
    # url(r'^category/(?P<category>[\w.@+-/]+)$/',
    #     ItemCategoryDetailView.as_view()),
    # path('category/create/', ItemCategoryCreateView.as_view()),

]
