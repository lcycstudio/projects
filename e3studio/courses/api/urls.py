# from marketplace.api.views import ItemCategoryViewSet
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'', ItemCategoryViewSet, basename='articles')  # path to api
# urlpatterns = router.urls

from django.urls import path
from django.conf.urls import url

from .views import (
    SubjectListView,
    MessageSendView,
)
#     ChapterDetailView,
#     SectionDetailView,
#     ContentDetailView,
#     ExerciseListView,
#     ChoiceDetailView,
#     ChoiceCheckView,
#     CodingInputView,
#     # ItemCategoryCreateView,
#     # ItemPlatformListView,
#     # ItemPlatformDetailView,
#     # ItemPlatformCreateView,
#     # ItemInstanceUserList,
#     # ItemInstanceDetailView,
# )

urlpatterns = [
    path('list/', SubjectListView.as_view()),
    path('message/', MessageSendView.as_view()),
]

#     path('<subject>/<chapter>/', ChapterDetailView.as_view()),
#     path('<subject>/<chapter>/<section>/', SectionDetailView.as_view()),
#     path('<subject>/<chapter>/<section>/exercises/', ExerciseListView.as_view()),
#     path('<subject>/<chapter>/<section>/content/', ContentDetailView.as_view()),
#     path('<subject>/<chapter>/<section>/get/<pk>/', ChoiceDetailView.as_view()),
#     path('<subject>/<chapter>/<section>/put/<pk>/', ChoiceCheckView.as_view()),
#     path('<subject>/<chapter>/<section>/coding/<pk>/', CodingInputView.as_view()),

#     # url(r'^category/(?P<category>[\w.@+-/]+)$/',
#     #     ItemCategoryDetailView.as_view()),
#     # path('category/create/', ItemCategoryCreateView.as_view()),


#     # item image

#     # item rating

#     # item comment

#     # path('<pk>/delete/', ItemCategoryDeleteView.as_view())
# ]


# # from django.urls import path

# # from .views import (
# #     ArticleListView,
# #     ArticleDetailView,
# #     ArticleCreateView,
# #     ArticleUpdateView,
# #     ArticleDeleteView,
# # )

# # urlpatterns = [
# #     path('', ArticleListView.as_view()),
# #     path('create', ArticleCreateView.as_view()),
# #     path('<pk>', ArticleDetailView.as_view()),
# #     path('<pk>/update', ArticleUpdateView.as_view()),
# #     path('<pk>/delete', ArticleDeleteView.as_view()),
# # ]
