from django.conf.urls import url, include, re_path
from django.urls import path

urlpatterns = [
    path('api/', include('registration.api_reg.urls')),
]


# from django.conf.urls import url, include, re_path
# from django.urls import path
# # from allauth.account.views import ConfirmEmailView
# from .views import LoginView, RegisterView, ConfirmEmailView, CompleteEmailView
# from . import views
# from django.contrib.auth import views as auth_views

# urlpatterns = [
#     # Override urls
#     # url(r'^registration/account-email-check-exist/', views.email_check_exist),
#     # url(r'^registration/account-username-check-exist/', views.username_check_exist),
#     url(r'^registration/account-email-username-check/', views.email_username_check),
#     url(r'^registration/account-username-check/', views.username_check),
#     url(r'^registration/account-email-check/', views.email_check),
#     url(r'^registration/login/', LoginView.as_view(), name='rest_login'),
#     url(r'^registration/signup/', RegisterView.as_view(), name='rest_register'),
#     re_path('registration/confirm-email/(?P<key>[-:\w]+)/', ConfirmEmailView.as_view(),
#             name='account_confirm_email'),
#     url(r'^registration/complete-email/(?P<key>[-:\w]+)/', CompleteEmailView.as_view(),
#         name="account_email_complete"),
#     url(r'^registration/resend-email/',
#         views.email_resend, name="account_email_resend"),
#     url(r'^registration/activate-email/(?P<uidb64>[-:\w]+)/(?P<keydb64>[-:\w]+)/',
#         views.email_activate, name="account_email_activate"),

#     path('registration/', include('django.contrib.auth.urls')),
