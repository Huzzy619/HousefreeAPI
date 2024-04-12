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


# ? Application definition

INSTALLED_APPS = [
    "channels",
    # "daphne",
    "jazzmin",
    # ? Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # ? Third Party
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "debug_toolbar",
    "django.contrib.sites",
    "cloudinary",
    "cloudinary_storage",
    "corsheaders",
    "phonenumber_field",
    "django_filters",
    "hitcount",
    "django_extensions",
    "data_browser",
    # ? Local
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
    "core.middleware.RequestIDMiddleware",
    "core.middleware.ExceptionHandlerMiddleware",
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

# ? Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": BASE_DIR / "db.sqlite3",
    # },
    # # The Multiple database system is not implemented yet
    # # "info_db": {
    # #     "ENGINE": "django.db.backends.sqlite3",
    # #     "NAME": BASE_DIR / "infodb.sqlite3",
    # # },
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "rentrite",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "localhost",
    }
}


# DATABASE_ROUTERS = ['routers.db_routers.InfoRouter']

# ? Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
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


# ? Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

# TIME_ZONE = "UTC"
TIME_ZONE = "Africa/Lagos"

USE_I18N = True

USE_TZ = True


# ? Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]


MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ? Debug Toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]

# ? Documentation Settings
SPECTACULAR_SETTINGS = {
    "TITLE": "RentRite API",
    "DESCRIPTION": "A better Home makes a better Family",
    "VERSION": "1.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # "SWAGGER_UI_DIST": "SIDECAR",  # shorthand to use the sidecar instead
    # "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    # "REDOC_DIST": "SIDECAR",
    # "ENUM_NAME_OVERRIDES" :{"Category57aEnum": "CategoryEnum"}
    # OTHER SETTINGS
    "DISABLE_ERRORS_AND_WARNINGS": True,
    "SCHEMA_COERCE_PATH_PK_SUFFIX": True,
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
}


# ? Authentication Settings

AUTH_USER_MODEL = "core.User"
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "core.exception_handlers.custom_exception_handler",
    "NON_FIELD_ERRORS_KEY": "error",
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
}


SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=5),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}


SITE_ID = config("SITE_ID", 1, cast=int)
CORS_ALLOW_ALL_ORIGINS = True


MJ_API_KEY = config("MJ_API_KEY", "")
MJ_API_SECRET = config("MJ_API_SECRET", "")
REDIS_URL = config("REDIS_URL", "redis://localhost:6379/1")
FLUTTERWAVE_KEY = config("FLUTTERWAVE_KEY", "")
FLW_SECRET_KEY = config("FLW_SECRET_KEY", default="")
RAVE_PUBLIC_KEY = config("RAVE_PUBLIC_KEY", default="")
RAVE_SECRET_KEY = config("RAVE_SECRET_KEY", default="")
PAYSTACK_SECRET_KEY = config("PAYSTACK_SECRET_KEY", default="")


# ? HITCOUNT SETTINGS
# Limit the number of active Hits from a single IP address. 0 means that it is unlimited.
HITCOUNT_HITS_PER_IP_LIMIT = 1

# This is the number of days, weeks, months, hours, etc (using a timedelta keyword argument), that an Hit is kept active.
# If a Hit is active a repeat viewing will not be counted.
# After the active period ends, however, a new Hit will be recorded.
# You can decide how long you want this period to last and it is probably a matter of preference
HITCOUNT_KEEP_HIT_ACTIVE = {"days": 1}


CELERY_BROKER_URL = REDIS_URL

# ? localhost email settings
EMAIL_PORT = 2525
EMAIL_HOST = "localhost"
SEND_EMAIL = config("SEND_EMAIL", default=False, cast=bool)

# ? Development Gmail settings

# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_HOST_USER = "blazingkrane@gmail.com"
# EMAIL_HOST_PASSWORD = "kohk xdnl nalp cleo"
# EMAIL_PORT = 465
# EMAIL_USE_SSL = True
# EMAIL_USE_TSL = False

TEST_RUNNER = "utils.test.PytestTestRunner"
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://localhost:6379/2",
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
            "handlers": ["console"],
            "propagate": True,
        },
    },
    "formatters": {
        "verbose": {
            "format": (
                "{asctime} ({levelname}) -  {module} {name} {process:d} {thread:d}"
                " {message}"
            ),
            "style": "{",
        },
        "simple": {
            "format": "{asctime} ({levelname}) -  {message}",
            "style": "{",
        },
    },
}

# ? JAZZMIN_SETTINGS

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
