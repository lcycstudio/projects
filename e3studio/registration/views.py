from rest_auth.serializers import PasswordResetConfirmSerializer
from allauth.account.models import EmailAddress, EmailConfirmation, EmailConfirmationHMAC
from allauth.account.utils import (perform_login, url_str_to_user_pk)
from allauth.account.adapter import get_adapter
from django.shortcuts import redirect
from django.contrib import messages
from django.http import Http404
from django.views.generic.base import TemplateResponseMixin, TemplateView, View
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# LoginView, RegisterView
from django.conf import settings
from django.contrib.auth import login as django_login
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny  # IsAuthenticated
from rest_auth.registration.app_settings import RegisterSerializer, register_permission_classes
from rest_auth.models import TokenModel
from rest_auth.app_settings import (
    TokenSerializer, JWTSerializer, create_token)
from rest_auth.utils import jwt_encode
from allauth.account import app_settings as allauth_settings
from allauth.account.utils import complete_signup
from .app_settings import (LoginSerializer)


# user_signup and email_resend
from .forms import GetEmailForm, ResetPasswordForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from rest_framework.exceptions import ValidationError
import e3studio.settings as e3studio_settings
from django.contrib.sites.models import Site
import os


@api_view()
def null_view(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view()
def complete_view(request):
    return Response("Email account is activated")


@api_view(['POST'])
def username_check(request):
    user_data = request.data
    username_exist = User.objects.filter(
        username__contains=user_data["username"].lower()).exists()
    if username_exist:
        raise ValidationError(
            {"message": "A user with that username already exists."})
    else:
        return Response({"Username is ok."})


@api_view(['POST'])
def email_check(request):
    user_data = request.data
    email_exist = User.objects.filter(
        email__contains=user_data["email"].lower()).exists()
    if email_exist:
        raise ValidationError(
            {"message": "A user is already registered with this e-mail address."})
    else:
        return Response({"Email is ok."})


@api_view(['POST'])
def email_username_check(request):
    user_data = request.data

    email_exist = User.objects.filter(
        email__contains=user_data["email"].lower()).exists()
    username_exist = User.objects.filter(
        username__contains=user_data["username"].lower()).exists()
    if email_exist and username_exist:
        raise ValidationError(
            {"message": "Both the e-mail address and the user exist."})
    elif email_exist:
        raise ValidationError(
            {"message": "A user is already registered with this e-mail address."})
    elif username_exist:
        raise ValidationError(
            {"message": "A user with that username already exists."})
    else:
        return Response({"username": user_data["username"], "email": user_data["email"]})


sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('password1', 'password2')
)


class LoginView(GenericAPIView):
    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework
    Accept the following POST parameters: username, password
    Return the REST Framework Token Object's key.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = TokenModel

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def process_login(self):
        django_login(self.request, self.user)

    def get_response_serializer(self):
        if getattr(settings, 'REST_USE_JWT', False):
            response_serializer = JWTSerializer
        else:
            response_serializer = TokenSerializer
        return response_serializer

    def login(self):

        self.user = self.serializer.validated_data['user']

        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(self.user)
        else:
            self.token = create_token(self.token_model, self.user,
                                      self.serializer)

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            self.process_login()

    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': self.user,
                'token': self.token
            }
            serializer = serializer_class(instance=data,
                                          context={'request': self.request})
        else:
            serializer = serializer_class(instance=self.token,
                                          context={'request': self.request})

        response = Response(serializer.data, status=status.HTTP_200_OK)
        if getattr(settings, 'REST_USE_JWT', False):
            from rest_framework_jwt.settings import api_settings as jwt_settings
            if jwt_settings.JWT_AUTH_COOKIE:
                from datetime import datetime
                expiration = (datetime.utcnow() +
                              jwt_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(jwt_settings.JWT_AUTH_COOKIE,
                                    self.token,
                                    expires=expiration,
                                    httponly=True)
        print("response ", response)
        return response

    def post(self, request, *args, **kwargs):
        self.request = request

        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request})

        print("request ", request)
        self.serializer.is_valid(raise_exception=True)
        self.login()
        return self.get_response()


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = register_permission_classes()
    token_model = TokenModel

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(RegisterView, self).dispatch(*args, **kwargs)

    def get_response_data(self, user):
        if allauth_settings.EMAIL_VERIFICATION == \
                allauth_settings.EmailVerificationMethod.MANDATORY:
            return {"detail": _("Verification e-mail sent.")}

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': user,
                'token': self.token
            }
            return JWTSerializer(data).data
        else:
            return TokenSerializer(user.auth_token).data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        user.is_active = False
        user.save()
        headers = self.get_success_headers(serializer.data)

        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(user)
        else:
            create_token(self.token_model, user, serializer)

        complete_signup(self.request._request, user,
                        allauth_settings.EMAIL_VERIFICATION,
                        None)
        return user


# I use this class to make modification for the email_confirm template

class ConfirmEmailView(TemplateResponseMixin, View):

    # + allauth_settings.TEMPLATE_EXTENSION
    print('e3studio_settings.BASE_DIR', e3studio_settings.BASE_DIR)

    template_name = os.path.join(
        e3studio_settings.BASE_DIR, "templates/account/email_confirm.html")

    def get(self, *args, **kwargs):
        try:
            self.object = self.get_object()
            if allauth_settings.CONFIRM_EMAIL_ON_GET:
                return self.post(*args, **kwargs)
        except Http404:
            self.object = None
        ctx = self.get_context_data()
        return self.render_to_response(ctx)

    def post(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        print(self.object)
        confirmation.confirm(self.request)
        get_adapter(self.request).add_message(
            self.request,
            messages.SUCCESS,
            'templates/account/messages/email_confirmed.txt',
            {'email': confirmation.email_address.email})
        if allauth_settings.LOGIN_ON_EMAIL_CONFIRMATION:
            resp = self.login_on_confirm(confirmation)
            if resp is not None:
                return resp
        # Don't -- allauth doesn't touch is_active so that sys admin can
        # use it to block users et al
        #
        # user = confirmation.email_address.user
        # user.is_active = True
        # user.save()
        redirect_url = self.get_redirect_url()
        if not redirect_url:
            ctx = self.get_context_data()
            return self.render_to_response(ctx)
        return redirect(redirect_url)

    def login_on_confirm(self, confirmation):
        """
        Simply logging in the user may become a security issue. If you
        do not take proper care (e.g. don't purge used email
        confirmations), a malicious person that got hold of the link
        will be able to login over and over again and the user is
        unable to do anything about it. Even restoring their own mailbox
        security will not help, as the links will still work. For
        password reset this is different, this mechanism works only as
        long as the attacker has access to the mailbox. If they no
        longer has access they cannot issue a password request and
        intercept it. Furthermore, all places where the links are
        listed (log files, but even Google Analytics) all of a sudden
        need to be secured. Purging the email confirmation once
        confirmed changes the behavior -- users will not be able to
        repeatedly confirm (in case they forgot that they already
        clicked the mail).
        All in all, opted for storing the user that is in the process
        of signing up in the session to avoid all of the above.  This
        may not 100% work in case the user closes the browser (and the
        session gets lost), but at least we're secure.
        """
        user_pk = None
        user_pk_str = get_adapter(self.request).unstash_user(self.request)
        if user_pk_str:
            user_pk = url_str_to_user_pk(user_pk_str)
        user = confirmation.email_address.user
        if user_pk == user.pk and self.request.user.is_anonymous:
            return perform_login(self.request,
                                 user,
                                 allauth_settings.EmailVerificationMethod.NONE,
                                 # passed as callable, as this method
                                 # depends on the authenticated state
                                 redirect_url=self.get_redirect_url)

        return None

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        emailconfirmation = EmailConfirmationHMAC.from_key(key)
        if not emailconfirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                emailconfirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                raise Http404()
        return emailconfirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs

    def get_context_data(self, **kwargs):
        ctx = kwargs
        ctx["confirmation"] = self.object
        # site = get_current_site(self.request)
        site = Site.objects.get(id=1)
        ctx.update({'site': site})
        return ctx

    def get_redirect_url(self):
        return get_adapter(self.request).get_email_confirmation_redirect_url(
            self.request)


confirm_email = ConfirmEmailView.as_view()


class CompleteEmailView(TemplateResponseMixin, View):
    # allauth_settings.TEMPLATE_EXTENSION
    template_name = os.path.join(
        e3studio_settings.BASE_DIR, "templates/account/email_complete.html")

    def get(self, *args, **kwargs):
        try:
            self.object = self.get_object()
            if allauth_settings.CONFIRM_EMAIL_ON_GET:
                return self.post(*args, **kwargs)
        except Http404:
            self.object = None
        ctx = self.get_context_data()
        return self.render_to_response(ctx)

    def post(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        user = confirmation.email_address.user
        user.is_active = True
        user.save()
        ctx = self.get_context_data()
        return self.render_to_response(ctx)

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        emailconfirmation = EmailConfirmationHMAC.from_key(key)
        if not emailconfirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                emailconfirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                raise Http404()
        return emailconfirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs

    def get_context_data(self, **kwargs):
        ctx = kwargs
        ctx["confirmation"] = self.object
        # site = get_current_site(self.request)
        site = Site.objects.get(id=1)
        ctx.update({'site': site})
        return ctx

    def get_redirect_url(self):
        return get_adapter(self.request).get_email_confirmation_redirect_url(
            self.request)


complete_email = CompleteEmailView.as_view()


def email_resend(request):
    form = GetEmailForm()
    context = {'form': form,
               'text_message': "Please enter the email address to issue a new e-mail confirmation request."}
    if request.method == "POST":
        form = GetEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email_field')
            user = User.objects.filter(email=email)
            print(user)
            if len(user) == 0:
                print('None')
            else:
                # current_site = get_current_site(request)
                current_site = Site.objects.get(id=1)
                email_subject = 'Activate Your Account'
                message = render_to_string('account/email/email_resend_message.txt', {
                    'user': user[0],
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                    'key': urlsafe_base64_encode(force_bytes(Token.objects.get(user=user[0]))),
                })
                to_email = form.cleaned_data.get('email_field')
                email = EmailMessage(email_subject, message, to=[to_email])
                email.send()
                context = {
                    'sent_message': "We have sent you an email. Please check your email box to complete registration. "}
                return render(request, "account/email_resend.html", context=context)
        else:
            form = GetEmailForm()
            print('bad request')
    return render(request, "account/email_resend.html", context=context)


def email_activate(request, uidb64, keydb64):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        key = urlsafe_base64_decode(keydb64).decode()
        user = User.objects.get(pk=uid)
        token = Token.objects.get(user=user)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and token.key == key:
        user.is_active = True
        user.save()
        return render(request, "account/email_resend.html", {'sent_message': "Your account has been activated successfully."})
    else:
        return render(request, "account/email_resend.html", {'invalid_message': "Activation link is invalid."})


# class PasswordResetConfirmView(GenericAPIView):
#     """
#     Password reset e-mail link is confirmed, therefore
#     this resets the user's password.
#     Accepts the following POST parameters: token, uid,
#         new_password1, new_password2
#     Returns the success/fail message.
#     """
#     serializer_class = PasswordResetConfirmSerializer
#     permission_classes = (AllowAny,)

#     @sensitive_post_parameters_m
#     def dispatch(self, *args, **kwargs):
#         return super(PasswordResetConfirmView, self).dispatch(*args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             {"detail": _("Password has been reset with the new password.")}
#         )


# def reset_password(request, uidb64, token):
#     uid = urlsafe_base64_decode(uidb64).decode()
#     exist_user = User.objects.get(pk=uid)
#     if exist_user.is_active is False:
#         exist_user.is_active = True
#         exist_user.save()
#     form = ResetPasswordForm()
#     context = {
#         "form": form,
#         "uidb64": uidb64,
#         "token": token
#     }
#     if request.method == 'POST':
#         form = ResetPasswordForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # update_session_auth_hash(request, user)  # Important!
#             # messages.success(
#             # request, 'Your password was successfully updated!')
#             # return redirect('reset_password_confirm', args=[uidb64, token])
#         # else:
#             # messages.error(request, 'Please correct the error below.')

#     return render(request, 'account/reset_password.html', context)
# Next work on javascript for email_resend

# class ResendEmailView(GenericAPIView):

#     template_name = os.path.join(
#         e3studio_settings.BASE_DIR, "templates/account/email_resend.html")

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context

#     def get_serializer_class(self):

#     def post(self, request, *args, **kwargs):

#         # self.email = self.serializer
#         # self.request = request

#         # self.serializer = self.get_serializer(data=self.request.data,
#         #   context={'request': request})

#         print("request ", self.get_serializer(data=request.data))
#         # self.serializer.is_valid(raise_exception=True)
#         # self.login()
#         # return self.get_response()

#         # print(self.request.data)
#         ctx = self.get_context_data()
#         return self.render_to_response(ctx)
    # try:
    #     self.object = self.get_object()
    #     if allauth_settings.CONFIRM_EMAIL_ON_GET:
    #         return self.post(*args, **kwargs)
    # except Http404:
    #     self.object = None
    # ctx = self.get_context_data()
    # return self.render_to_response(ctx)

    # def post(self, request, *args, **kwargs):
    #     self.request = request

    #     self.serializer = self.get_serializer(data=self.request.data,
    #                                           context={'request': request})

    #     print("request ", request)
    #     self.serializer.is_valid(raise_exception=True)
    #     self.login()
    #     return self.get_response()
    # self.object = confirmation = self.get_object()
    # confirmation.confirm(self.request)
    # get_adapter(self.request).add_message(
    #     self.request,
    #     messages.SUCCESS,
    #     'templates/account/messages/email_confirmed.txt',
    #     {'email': confirmation.email_address.email})
    # if allauth_settings.LOGIN_ON_EMAIL_CONFIRMATION:
    #     resp = self.login_on_confirm(confirmation)
    #     if resp is not None:
    #         return resp
    # Don't -- allauth doesn't touch is_active so that sys admin can
    # use it to block users et al
    #
    # user = confirmation.email_address.user
    # user.is_active = True
    # user.save()
    # redirect_url = self.get_redirect_url()
    # if not redirect_url:
    #     ctx = self.get_context_data()
    #     return self.render_to_response(ctx)
    # return redirect(redirect_url)


# resend_email = ResendEmailView.as_view()
# @api_view(['POST'])
# def username_check_exist(request):
#     user_data = request.data
#     if User.objects.filter(username__contains=user_data["username"].lower()).exists():
#         raise ValidationError({"Username already exists."})
#     else:
#         return Response({"username-ok"})


# @api_view(['POST'])
# def email_check_exist(request):
#     user_data = request.data
#     if User.objects.filter(email__contains=user_data["email"].lower()).exists():
#         raise ValidationError({"Email already exists."})
#     else:
#         return Response({"email-ok"})

# if User.objects.filter(email__contains=user_data["email"].lower()).exists() and
#     User.objects.filter(username__contains=user_data["username"].lower()).exists():
#     raise ValidationError("Username and Email already exist.")


# elif User.objects.filter(username__contains=user_data["username"].lower()).exists():
#     raise ValidationError("Username already exists.")

# user = User.objects.create_user(user_data['username'], user_data['email'], user_data['password2'])
# user = User.objects.get(email="lewischen856@gmail.com")
# user.is_active = False
# user.save()
# current_site = get_current_site(request)
# email_subject = 'Activate Your Account'
# message = render_to_string('./registration/activate_account.html', {
#     'user': user,
#     'domain': current_site.domain,
#     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#     # 'token': Token.objects.create(user=user)
# })
# to_email = user_data['email']
# email = EmailMessage(email_subject, message, to=[to_email])
# email.send()
# # for item, value in request.data:
# #     print(value)
# print(request.data)
# return Response({"We have sent you an email, please confirm your email address to complete registration."})


# def activate_account(request, uidb64, token):
#     try:
#         uid = force_bytes(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         # login(request, user)
#         return Response('Your account has been activate successfully')
#     else:
#         return Response('Activation link is invalid!')
