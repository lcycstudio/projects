import os
import e3studio.settings as e3studio_settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.conf import settings
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import (
    GenericAPIView,
    # ListAPIView,
    # RetrieveAPIView,
    CreateAPIView,
    # UpdateAPIView,
    # DestroyAPIView,
)
# from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

# Login View
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_auth.models import TokenModel
from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

# Importing serializers from app_settings
from registration.app_settings import (
    create_token, register_permission_classes,
    UserTokenSerializer,
    UserLoginSerializer,
    UserRegisterSerializer,
    UserPasswordForgetSerializer,
    UserPasswordResetSerializer,
    UserPasswordChangeSerializer,
    UserTokenVerifySerializer,
)

# User Register and Email Resend
from rest_auth.app_settings import TokenSerializer  # , JWTSerializer, create_token
from django.views.generic.base import TemplateResponseMixin, TemplateView, View
from allauth.account.adapter import get_adapter
from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings
from django.http import Http404
from allauth.account.models import EmailAddress, EmailConfirmation, EmailConfirmationHMAC
from django.contrib.sites.models import Site
from registration.forms import GetEmailForm, ResetPasswordForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage, EmailMultiAlternatives
from .send import send_confirmation_mail

# from .app_settings import RegisterSerializer, register_permission_classes
from userprofile.models import Profile

# create order

# import datetime
# import base64
# from io import BytesIO


sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('password1', 'password2')
)


class TestEmailSend(GenericAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        return Response('hi')

    def post(self, request, format=None):
        try:
            user = User.objects.get(email=request.data['email'])
        except User.DoesNotExist:
            user = None
        else:
            try:
                email = EmailAddress.objects.get(email=user.email)
            except EmailAddress.DoesNotExist:
                # email = None
                raise ValidationError({'error': 'Email does not exist'})
            else:
                send_confirmation_mail(request, user, email)
            # send_confirmation_mail(request, user)
        # SignupSendEmail.send_confirmation_mail()
        return Response('hi')


class UserLoginView(GenericAPIView):
    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework
    Accept the following POST parameters: username, password
    Return the REST Framework Token Object's key.
    """
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    token_model = TokenModel

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(UserLoginView, self).dispatch(*args, **kwargs)

    def process_login(self):
        django_login(self.request, self.user)

    def login(self):
        self.user = self.serializer.validated_data['user']
        # REST_USE_JWT is irrelevant since I don't use it in settings
        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(self.user)
        else:
            self.token = create_token(self.token_model, self.user,
                                      self.serializer)
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            self.process_login()

    def get_mc(self):
        token, tk_created = Token.objects.get_or_create(user=self.user)
        try:
            clu = Profile.objects.get(user_id=self.user)
        except Profile.DoesNotExist:
            clu = None
        if clu is not None:
            content = {
                'token': token.key,
                'name': '{0} {1}'.format(clu.first_name, clu.last_name),
                'talored': clu.tailored,
            }
        else:
            content = {
                'token': token.key,
                'name': 'E3Studio User',
                'tailored': None,
            }
        # getMnger, u_created = Profile.objects.get_or_create(
        #     user_id=self.user,
        #     defaults={
        #         'first_name': self.user.first_name if self.user.first_name else None,
        #         'last_name': self.user.last_name if self.user.last_name else None,
        #     }
        # )
        # content = {
        #     'token': token.key,
        #     'mnger': getMnger.is_mnger,
        #     'corpo': getCorpo.is_corpo,
        # }

        return Response(content)

    def get_response(self):

        serializer_class = UserTokenSerializer
        serializer = serializer_class(instance=self.get_mc().data,
                                      context={'request': self.request})
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request})
        self.serializer.is_valid(raise_exception=True)
        self.login()
        return self.get_response()


class UserLogoutView(APIView):
    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.
    Accepts/Returns nothing.
    """
    serializer_class = UserTokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data
        token = data['token'] if data['token'] else ""
        if token != "":
            try:
                Token.objects.get(key=token).delete()
            except (AttributeError, ObjectDoesNotExist):
                pass
        response = Response({"detail": _("Successfully logged out.")},
                            status=status.HTTP_200_OK)
        return response


class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = register_permission_classes()
    # token_model = TokenModel

    @ sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(UserRegisterView, self).dispatch(*args, **kwargs)

    def get_response_data(self, user):
        if allauth_settings.EMAIL_VERIFICATION == \
                allauth_settings.EmailVerificationMethod.MANDATORY:
            return {"detail": _("Verification e-mail sent.")}
        return TokenSerializer(user.auth_token).data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # perform creating user
        user = self.perform_create(serializer)
        user.is_active = False
        user.save()
        # headers = self.get_success_headers(serializer.data)

        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED)
        # headers=headers)

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        # if getattr(settings, 'REST_USE_JWT', False):
        #     self.token = jwt_encode(user)
        # else:
        # create_token(self.token_model, user, serializer)
        if allauth_settings.EMAIL_VERIFICATION == \
                allauth_settings.EmailVerificationMethod.MANDATORY:
            try:
                email = EmailAddress.objects.get(email=user.email)
            except EmailAddress.DoesNotExist:
                raise ValidationError({'error': 'Email does not exist'})
            else:
                send_confirmation_mail(self.request, user, email)
        else:
            complete_signup(self.request._request, user,
                            'optional',
                            None)
        return user


# # I use this class to make modification for the email_confirm template


class UserEmailConfirmView(TemplateResponseMixin, View):

    # + allauth_settings.TEMPLATE_EXTENSION
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


class UserEmailCompleteView(TemplateResponseMixin, View):
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


def email_resend(request):
    form = GetEmailForm()
    context = {'form': form,
               'text_message': "Please enter the email address to issue a new e-mail confirmation request."}
    if request.method == "POST":
        form = GetEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email_field')
            user = User.objects.filter(email=email)
            if len(user) == 0:
                pass
            else:
                # current_site = get_current_site(request)
                current_site = Site.objects.get(id=1)
                email_subject = 'Activate Your Account'
                message = render_to_string('account/email/email_resend_message.txt', {
                    'user': user[0],
                    'domain': current_site.domain,
                    'domain_name': current_site.name,
                    'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                    'key': urlsafe_base64_encode(force_bytes(Token.objects.get(user=user[0]))),
                })
                to_email = form.cleaned_data.get('email_field')
                email = EmailMessage(email_subject, message, to=[to_email])
                email.send()
                context = {
                    'sent_message': "We have sent you an email."}
                return render(request, "account/email_resend.html", context=context)
        else:
            form = GetEmailForm()
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
        return render(request, "account/email_resend.html", {'activate_message': "Your account has been activated successfully.", "active": "true"})
    else:
        return render(request, "account/email_resend.html", {'invalid_message': "Activation link is invalid."})


# class UserEmailSentView(TemplateView):
#     # + app_settings.TEMPLATE_EXTENSION
#     template_name = "account/verification_sent.html"


class UserPasswordForgetView(GenericAPIView):
    """
    Calls Django Auth PasswordResetForm save method.
    Accepts the following POST parameters: email
    Returns the success/fail message.
    """
    serializer_class = UserPasswordForgetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"detail": _("Your secured password reset e-mail has been sent.")},
            status=status.HTTP_200_OK
        )


class UserPasswordResetView(GenericAPIView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.
    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = UserPasswordResetSerializer
    permission_classes = (AllowAny,)

    @ sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(UserPasswordResetView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("Your password has been reset.")})


class UserPasswordChangeView(GenericAPIView):
    """
    Calls Django Auth SetPasswordForm save method.
    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = UserPasswordChangeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @ sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(UserPasswordChangeView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("Your password has been changed.")})


class UserTokenVerifyView(GenericAPIView):
    serializer_class = UserTokenVerifySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        data = request.data
        try:
            user = Token.objects.get(key=data['token']).user
            authUser = authenticate(
                username=user.username, password=data['current_password'])
            if authUser is None:
                msg = _(
                    'Critical error: user does not exist with provided password.')
                raise ValidationError({'error': msg})
            else:
                return Response({'match': True})
        except Exception as e:
            msg = _('Current user and password do not match.')
            raise ValidationError({'error': msg})
        # if user:
        #     authUser = authenticate(
        #         username=user.username, password=data['current_password'])
        # else:
        #     msg = _('Crtical error has occured: user or password do not exist.')
        #     raise exceptions.ValidationError({'error':msg})
        # if authUser is not None:
        #     return Response({'match': True})
        # else:
        #     raise exceptions.ValidationError({'error':msg})
