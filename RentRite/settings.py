"""
Django settings for RentRite project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-2j7na566q5h%1*j$mo@c+*7-z)r&#62j^4*-a8$g@a(%#5stjy"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "channels",
    # "daphne",
    "jazzmin",
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third Party
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "debug_toolbar",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "dj_rest_auth.registration",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "cloudinary",
    "cloudinary_storage",
    "corsheaders",
    "phonenumber_field",
    "django_filters",
    "hitcount",
    # Local
    "core",
    "apartments",
    "chat",
    "info",
    "blog",
    "payments",
    "notifications",
    # "playground",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "RentRite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
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

WSGI_APPLICATION = "RentRite.wsgi.application"
ASGI_APPLICATION = "RentRite.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
    # The Multiple database system is not implemented yet
    # "info_db": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": BASE_DIR / "infodb.sqlite3",
    # },
    # "default":{
    #     "ENGINE": "django.db.backends.postgresql",
    #     "NAME": "freehouse",
    #     "USER": "postgres",
    #     "PASSWORD": "0509",
    #     "HOST": "localhost"
    # }
}


# DATABASE_ROUTERS = ['routers.db_routers.InfoRouter']

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"


MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Debug Toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]

# Documentation Settings
SPECTACULAR_SETTINGS = {
    "TITLE": "RentRite API",
    "DESCRIPTION": "A better Home makes a better Family",
    "VERSION": "1.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",  # shorthand to use the sidecar instead
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    # "ENUM_NAME_OVERRIDES" :{"Category57aEnum": "CategoryEnum"}
    # OTHER SETTINGS
}


# Authentication Settings

AUTH_USER_MODEL = "core.User"
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ),
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "NON_FIELD_ERRORS_KEY": "error",
}
REST_AUTH_SERIALIZERS = {
    "LOGIN_SERIALIZER": "core.serializers.CustomLoginSerializer",
    "REGISTER_SERIALIZER": "core.serializers.CustomRegisterSerializer",
    # "PASSWORD_RESET_CONFIRM_SERIALIZER": ""
    # "PASSWORD_CHANGE_SERIALIZER":"core.serializers."
}
REST_USE_JWT = True

JWT_AUTH_COOKIE = "my-app-auth"
JWT_AUTH_REFRESH_COOKIE = "my-refresh-token"


SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=5),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}


ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
# OLD_PASSWORD_FIELD_ENABLED = True

# In order to verify an email address a key is mailed identifying the email address to be verified.
# In previous versions, a record was stored in the database for each ongoing email confirmation, keeping track of these keys.
# Current versions use HMAC based keys that do not require server side state.
# ACCOUNT_EMAIL_CONFIRMATION_HMAC = True

# Determines the e-mail verification method during signup – choose one of "mandatory", "optional", or "none".

# Setting this to “mandatory” requires ACCOUNT_EMAIL_REQUIRED to be True

# When set to “mandatory” the user is blocked from logging in until the email address is verified.
# Choose “optional” or “none” to allow logins with an unverified e-mail address.
# In case of “optional”, the e-mail verification mail is still sent, whereas in case of “none” no e-mail verification mails are sent.

ACCOUNT_EMAIL_VERIFICATION = config("ACCOUNT_EMAIL_VERIFICATION", "none")

SITE_ID = config("SITE_ID", 1, cast=int)
CORS_ALLOW_ALL_ORIGINS = True


# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        "APP": {
            "client_id": config("GOOGLE_CLIENT_ID", ""),
            "secret": config("GOOGLE_SECRET", ""),
            "key": "",
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    }
}

MJ_API_KEY = config("MJ_API_KEY", "")
MJ_API_SECRET = config("MJ_API_SECRET", "")
REDIS_URL = config("REDIS_URL", "redis://localhost:6379/1")
FLUTTERWAVE_KEY = config("FLUTTERWAVE_KEY", "")
FLW_SECRET_KEY = config("FLW_SECRET_KEY", default ="")
RAVE_PUBLIC_KEY = config("RAVE_PUBLIC_KEY", default ="")
RAVE_SECRET_KEY = config("RAVE_SECRET_KEY", default ="")
PAYSTACK_SECRET_KEY = config("PAYSTACK_SECRET_KEY", default ="")


# HITCOUNT SETTINGS
HITCOUNT_HITS_PER_IP_LIMIT = 1
HITCOUNT_KEEP_HIT_ACTIVE = { 'days': 2 }

CELERY_BROKER_URL = REDIS_URL

SEND_EMAIL = config("SEND_EMAIL", default=False, cast=bool)

# local email settings
EMAIL_PORT = 2525
EMAIL_HOST = "localhost"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://localhost:6379/2',
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "simple"},
        "file": {
            "class": "logging.FileHandler",
            "filename": "general.log",
            "formatter": "verbose",
            "level": config("DJANGO_LOG_LEVEL", "WARNING"),
        },
    },
    "loggers": {
        "": {  # The empty string indicates ~ All Apps including installed apps
            "handlers": ["file"],
            "propagate": True,
        },
    },
    "formatters": {
        "verbose": {
            "format": "{asctime} ({levelname}) -  {module} {name} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{asctime} ({levelname}) -  {message}",
            "style": "{",
        },
    },
}

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "RentRite Ltd",
    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "RENTRITE",
    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "RENTRITE",
    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "images/Logo3.png",
    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": "images/Logo2.png",
    # Logo to use for login form in dark themes (defaults to login_logo)
    # "login_logo_dark": "images/Logo4.png",
    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": "images/Logo3.png",
    # Welcome text on the login screen
    "welcome_sign": "Welcome to RentRite Admin Site",
    # Copyright on the footer
    "copyright": "RENTRITE",
    "show_ui_builder": True,

    "changeform_format": "collapsible",
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-purple",
    "accent": "accent-lightblue",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": True,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-purple",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "pulse",
    # "dark_mode_theme": "cyborg",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}
