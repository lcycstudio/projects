from django.urls import path
from django.conf.urls import url, re_path
# from django.contrib.auth import views as auth_views
from . import views

from .views import (
    UserLoginView,
    UserLogoutView,
    UserRegisterView,
    UserEmailConfirmView,
    UserEmailCompleteView,
    UserEmailSentView,
    UserPasswordForgetView,
    UserPasswordResetView,
    UserPasswordChangeView,
    UserTokenVerifyView,
)


from django.views.generic import TemplateView

from rest_auth.views import (
    PasswordChangeView,
)

urlpatterns = [
    # login
    path('registration/login/', UserLoginView.as_view()),
    # logout
    path('registration/logout/', UserLogoutView.as_view()),
    # signup
    path('registration/signup/',
         UserRegisterView.as_view(), name='rest_register'),
    # email verification sent (not useful but must include this)
    path("registration/confirm-email/",
         UserEmailSentView.as_view(), name="account_email_verification_sent"),

    # confirm email link from email box
    re_path('registration/confirm-email/(?P<key>[-:\w]+)/', UserEmailConfirmView.as_view(),
            name='account_confirm_email'),
    # complete email registration after clicking "Confirm" on confirm email page
    url(r'^registration/complete-email/(?P<key>[-:\w]+)/', UserEmailCompleteView.as_view(),
        name="account_email_complete"),
    # resend email if the activation link expires
    url(r'^registration/resend-email/',
        views.email_resend, name="account_email_resend"),
    # activate email upon requesting resending another email
    url(r'^registration/activate-email/(?P<uidb64>[-:\w]+)/(?P<keydb64>[-:\w]+)/',
        views.email_activate, name="account_email_activate"),

    # Forget Password Mechanism:
    # 1. Build frontend forget password page to link to UserPasswordForgetView
    # 2. Make custom password_reset_email.html in templates/registration
    # 3. Use custom frontend url with uid and token redirect
    # 4. Build frontend forget password reset page to obtain uid and token
    # 5. Upon entering new passwords, this page will link with UserPasswordResetView
    # 6. Complete the forget password with detail sent back as res.data
    # api for forget password and entering email
    url(r'^registration/password/forget/$', UserPasswordForgetView.as_view(),
        name='rest_password_reset'),
    # password reset form from forgot password link sent to email
    url(r'^registration/password/confirm/$', UserPasswordResetView.as_view(),
        name='rest_password_forget_confirm'),

    # Reset Password Mechanism:
    # 1. UserPasswordChangeView requires permissions.IsAuthenticated (know password to change)
    # 2. react axios.post(ur, data, {headers: {'Authentication': `Token ${props.token}`}})
    # 3. For security reasons, I ask users to enter password to authenticate themselves
    # 4. UserTokenVerifyView authenticate username and password by feeding props.token
    # 5. Once it is done, the change password form can be called and submitted
    url(r'^registration/password/change/$', UserPasswordChangeView.as_view(),
        name='rest_password_change'),
    url(r'^registration/password/tokenverify/$',
        UserTokenVerifyView.as_view())

]
