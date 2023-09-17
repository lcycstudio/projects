import os, sys
from socket import gethostname, gethostbyname
from django.core.exceptions import ImproperlyConfigured
from .awsenv import load_env_from_aws_if_configured
from pathlib import Path

load_env_from_aws_if_configured()


def get_required_var(var):
    try:
        return os.environ[var]
    except KeyError:
        error_message = f"{var} environment variable not set."
        raise ImproperlyConfigured(error_message)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-)fz%d!_jvpma(h@(n%^%dm-3wuyn!h5og5^@mz#cqarazn3gv6'
SECRET_KEY = get_required_var("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG_ENV = os.environ.get("DEBUG", False)
DEBUG = DEBUG_ENV and not DEBUG_ENV.lower() == "false"

ALLOWED_HOSTS = [
    gethostname(),
    gethostbyname(gethostname()),
    "127.0.0.1",
    "localhost",
]

CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://leadexchange.com",
    "https://lexstaging.com",
]

CORS_ORIGIN_REGEX_WHITELIST = [
    r"https://.*\.leadexchange\.com$",
    r"https://.*\.lexstaging\.com$",
]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",  # new
    "rest_framework.authtoken",  # new
    "corsheaders",  # new
    "django_ses",  # new
    "storages",  # new
]

MIDDLEWARE = [
    "server.middleware.HealthCheckMiddleware",  # new
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "server.urls"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",  # added for /openapi/
    ),
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "static")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ASGI_APPLICATION = 'server.routing.application'
ASGI_APPLICATION = "server.asgi.application"

# WSGI_APPLICATION = 'server.wsgi.application'


# AWS settings
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

# SES settings
EMAIL_BACKEND = "django_ses.SESBackend"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")

# Storages
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_DEFAULT_ACL = "public-read"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}

# Stripe
STRIPE_SK = os.environ.get("STRIPE_SK")
STRIPE_PK = os.environ.get("STRIPE_PK")

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
MGDB_NAME = os.environ.get("MGDB_NAME")
MGDB_USER = os.environ.get("MGDB_USER")
MGDB_PSWD = os.environ.get("MGDB_PSWD")
MGDB_CLST = os.environ.get("MGDB_CLST")
DATABASES = {
    "default": {
        "ENGINE": "djongo",
        "NAME": MGDB_USER,
        "ENFORCE_SCHEMA": False,
        "CLIENT": {
            "host": f"mongodb+srv://{MGDB_USER}:{MGDB_PSWD}@{MGDB_CLST}/{MGDB_NAME}?retryWrites=true&w=majority"
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, "public/media/")
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(BASE_DIR, "public/static/")
STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

RECAPTCHA_THRESHOLD = float(os.environ.get("RECAPTCHA_THRESHOLD", 0.7))
RECAPTCHA_SECRET = os.environ.get("RECAPTCHA_SECRET")
