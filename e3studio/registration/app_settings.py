from rest_auth.registration.serializers import (
    RegisterSerializer as DefaultRegisterSerializer)
from rest_framework.permissions import AllowAny
from django.conf import settings

from rest_auth.utils import import_callable, default_create_token

from registration.api_reg.serializers import (
    UserTokenSerializer as DefaultUserTokenSerializer,
    UserLoginSerializer as DefaultUserLoginSerializer,
    UserRegisterSerializer as DefaultUserRegisterSerializer,
    UserPasswordForgetSerializer as DefaultUserPasswordForgetSerializer,
    UserPasswordResetSerializer as DefaultUserPasswordResetSerializer,
    UserPasswordChangeSerializer as DefaultUserPasswordChangeSerializer,
    UserPasswordChangeSerializer as DefaultUserPasswordChangeSerializer,
    UserTokenVerifySerializer as DefaultUserTokenVerifySerializer,
)

# from user.api.serializers import (
#     IDUpdateSerializer as DefaultIDUpdateSerializer,
#     ChargeAccountUpdateSerializer as DefaultChargeAccountUpdateSerializer,

# )
#  ADMINISTRATION SERIALIZERS
# Login
create_token = import_callable(
    getattr(settings, 'REST_AUTH_TOKEN_CREATOR', default_create_token))


def register_permission_classes():
    permission_classes = [AllowAny, ]
    for klass in getattr(settings, 'REST_AUTH_REGISTER_PERMISSION_CLASSES', tuple()):
        permission_classes.append(import_callable(klass))
    return tuple(permission_classes)


serializers = getattr(settings, 'REST_AUTH_SERIALIZERS', {})


# USER REGISTRATION SERIALIZERS
UserTokenSerializer = import_callable(
    serializers.get('USER_TOKEN_SERIALIZER', DefaultUserTokenSerializer))

UserLoginSerializer = import_callable(
    serializers.get('USER_LOGIN_SERIALIZER', DefaultUserLoginSerializer))

UserRegisterSerializer = import_callable(
    serializers.get('USER_REGISTER_SERIALIZER', DefaultUserRegisterSerializer))

UserPasswordForgetSerializer = import_callable(serializers.get(
    'USER_PASSWORD_FORGET_SERIALIZER', DefaultUserPasswordForgetSerializer))

UserPasswordResetSerializer = import_callable(serializers.get(
    'USER_PASSWORD_RESET_SERIALIZER', DefaultUserPasswordResetSerializer))


UserPasswordChangeSerializer = import_callable(serializers.get(
    'USER_PASSWORD_CHANGE_SERIALIZER', DefaultUserPasswordChangeSerializer))


UserTokenVerifySerializer = import_callable(serializers.get(
    'USER_TOKEN_VERIFY_SERIALIZER', DefaultUserTokenVerifySerializer))


# API Tools
# IDUpdateSerializer = import_callable(serializers.get(
#     'ID_UPDATE_SERIALIZER', DefaultIDUpdateSerializer))

# ChargeAccountUpdateSerializer = import_callable(serializers.get(
#     'CHARGE_ACCOUNT_UPDATE_SERIALIZER', DefaultChargeAccountUpdateSerializer))
