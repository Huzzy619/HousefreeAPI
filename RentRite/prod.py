import os

import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from corsheaders.defaults import default_headers
from .settings import *  # noqa
from decouple import config

SECRET_KEY = os.environ.get("SECRET_KEY", config("SECRET_KEY", SECRET_KEY))

# DEBUG = config("DEBUG", False, cast=bool)


LOCAL_ALLOWED_HOSTS = ["localhost", "127.0.0.1", "localhost:3000"]

# ALLOWED_HOSTS = [
#     "rentrite.herokuapp.com",
#     "rentrite.up.railway.app",
#     "rentrite-homes.up.railway.app",
#     "rentrite.cleverapps.io",
# ]


CSRF_TRUSTED_ORIGINS = (
    ["https://" + host for host in ALLOWED_HOSTS]
    + ["http://" + host for host in LOCAL_ALLOWED_HOSTS]
    + ["https://rentrite.up.railway.app", "https://rentrite-homes.up.railway.app"]
)


CORS_ALLOW_HEADERS = list(default_headers)

# DATABASES = {"default": dj_database_url.config()}
DATABASES = {
    "default": dj_database_url.parse(
        config("RAILWAY_DB_URL", ""),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

INSTALLED_APPS.append('treblle')

MIDDLEWARE.append('treblle.middleware.TreblleMiddleware')


STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config("CLOUD_NAME", ""),
    "API_KEY": config("CLOUD_API_KEY", ""),
    "API_SECRET": config("CLOUD_API_SECRET", ""),
}


# Test mailtrap email account.... till mail_jet is fully configured
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_SSL = False
EMAIL_USE_TSL = True


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis-13115.c261.us-east-1-4.ec2.cloud.redislabs.com", 13115)],
            "password": "",
            # "db": 0,
        },
    },
}


CELERY_BROKER_URL = REDIS_URL

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    }
}

sentry_sdk.init(
    dsn=config("SENTRY_LOGGER_URL", ""),
    integrations=[DjangoIntegration()],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # To set a uniform sample rate
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production,
    profiles_sample_rate=1.0,
)


TREBLLE_INFO = {
'api_key': config('TREBLLE_API_KEY'),
'project_id': config('TREBLLE_PROJECT_ID')
}