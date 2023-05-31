import os
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate  # get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.contrib.auth.tokens import default_token_generator
from rest_framework.exceptions import ValidationError
from registration.models import StudentUser

# Get the UserModel
UserModel = get_user_model()

# RegisterSerializer
try:
    from allauth.account import app_settings as allauth_settings
    from allauth.utils import (email_address_exists,
                               get_username_max_length)
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
except ImportError:
    raise ImportError("allauth needs to be added to INSTALLED_APPS.")


class UserTokenSerializer(serializers.Serializer):
    """
    Serializer for Token Manager Verification.
    """
    token = serializers.CharField(
        max_length=100, required=False, allow_blank=True)
    name = serializers.CharField(
        max_length=100, required=False, allow_blank=True)
    tailored = serializers.CharField(
        max_length=2000, required=False, allow_blank=True)

    def update(self, instance, validated_data):
        instance.token = validated_data.get(
            'token', instance.token)
        instance.name = validated_data.get(
            'name', instance.name)
        instance.tailored = validated_data.get(
            'tailored', instance.tailored)
        instance.save()
        return instance


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def _validate_email(self, email, password):
        user = None
        if email and password:
            # This is where things get complicated: username IS the email
            user = authenticate(
                username=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError({'error': msg})
        # if 'securigene' not in email.split("@")[1]:
        #     msg = _('Please enter a SecuriGene email.')
        #     raise exceptions.ValidationError({'error': msg})
        # else:
        return user

    def _validate_username(self, username, password):
        user = None
        if username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include "username" and "password".')
            raise exceptions.ValidationError({'error': msg})
        return user

    def _validate_username_email(self, username, email, password):
        user = None
        if email and password:
            user = self.authenticate(email=email, password=password)
        elif username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include either "username" or "email" and "password".')
            raise exceptions.ValidationError({'error': msg})
        return user

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        user = None
        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            # Authentication through email
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
                user = self._validate_email(email, password)
            # Authentication through username
            elif app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
                user = self._validate_username(username, password)
            # Authentication through either username or email
            else:
                user = self._validate_username_email(username, email, password)
        else:
            # Authentication without using allauth
            if email:
                try:
                    username = UserModel.objects.get(
                        email__iexact=email).get_username()
                except UserModel.DoesNotExist:
                    pass
            if username:
                user = self._validate_username_email(username, '', password)
        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is not yet activated.')
                raise exceptions.ValidationError({'error': msg})
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError({'error': msg})

        # If required, is the email verified?
        # if 'rest_auth.registration' in settings.INSTALLED_APPS:
        #     from allauth.account import app_settings
        #     if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
        #         email_address = user.emailaddress_set.get(email=user.email)
        #         if not email_address.verified:
        #             raise serializers.ValidationError(
        #                 _('E-mail is not verified.'))

        attrs['user'] = user
        return attrs


class UserRegisterSerializer(serializers.Serializer):
    # username = serializers.CharField(
    #     # style={'input_type': 'disable'}
    #     read_only=True,
    #     # max_length=get_username_max_length(),
    #     # min_length=allauth_settings.USERNAME_MIN_LENGTH,
    #     # required=allauth_settings.USERNAME_REQUIRED
    # )
    first_name = serializers.CharField(required=False)
    middle_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(
        write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    def validate_username(self, email):
        username = get_adapter().clean_username(email)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
            # elif 'securigene' not in email:
            #     raise serializers.ValidationError(
            #         _("Please register with your securigene email."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                _("The two password fields didn't match."))
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        # username = self.validated_data.get('email', '').split(
        #     '@')[0] if self.validated_data.get('email', '') != "" else ""
        return {
            'username': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        student, created = StudentUser.objects.get_or_create(
            user_id=user,
            defaults={
                'first_name': user.first_name if user.first_name else "",
                'last_name': user.last_name if user.last_name else "",
            }
        )
        return user


class UserPasswordForgetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    email = serializers.EmailField()

    password_reset_form_class = PasswordResetForm

    def get_email_options(self):
        """Override this method to change default e-mail options"""
        # from_email = SGTool.objects.get(id=1).info_email
        # email_template_name = os.path.join(
        #     settings.BASE_DIR, 'templates/registration/password_reset_email_user.html')
        return {}

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(
            data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': SGTool.objects.get(id=1).info_email,
            'request': request,
            'html_email_template_name': 'registration/password_reset_email_system.html',
        }
        opts.update(self.get_email_options())
        self.reset_form.save(**opts)


class UserPasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    uid = serializers.CharField()
    token = serializers.CharField()

    set_password_form_class = SetPasswordForm

    def custom_validation(self, attrs):
        pass

    def validate(self, attrs):
        self._errors = {}

        # Decode the uidb64 to uid to get User object
        try:
            uid = force_text(uid_decoder(attrs['uid']))
            self.user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})

        return attrs

    def save(self):
        return self.set_password_form.save()


class UserPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def __init__(self, *args, **kwargs):
        self.old_password_field_enabled = getattr(
            settings, 'OLD_PASSWORD_FIELD_ENABLED', False
        )
        self.logout_on_password_change = getattr(
            settings, 'LOGOUT_ON_PASSWORD_CHANGE', False
        )
        super(UserPasswordChangeSerializer, self).__init__(*args, **kwargs)

        if not self.old_password_field_enabled:
            self.fields.pop('old_password')

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password(value)
        )

        if all(invalid_password_conditions):
            err_msg = _(
                "Your old password was entered incorrectly. Please enter it again.")
            raise serializers.ValidationError(err_msg)
        return value

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()
        if not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(self.request, self.user)


class UserTokenVerifySerializer(serializers.Serializer):
    token = serializers.CharField(
        max_length=100, style={'input_type': 'password'})
    current_password = serializers.CharField(style={'input_type': 'password'})

    def update(self, instance, validated_data):
        instance.token = validated_data.get(
            'token', instance.token)
        instance.current_password = validated_data.get(
            'current_password', instance.current_password)
        instance.save()
        return instance
