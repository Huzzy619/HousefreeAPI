import os

import dj_database_url

from .settings import *

SECRET_KEY = os.environ.get("SECRET_KEY", config("SECRET_KEY", SECRET_KEY))

DEBUG = False

ALLOWED_HOSTS = ["rentrite.up.railway.app", "rentrite.herokuapp.com"]

CSRF_TRUSTED_ORIGINS = ["https://rentrite.up.railway.app", "https://rentrite.herokuapp.com"]

# DATABASES = {"default": dj_database_url.config()}
DATABASES = {
    'default': dj_database_url.parse(
        os.environ.get("ELEPHANT_SQL", config("ELEPHANT_SQL", "")),
        conn_max_age=600,
        conn_health_checks=True,
    )
}



DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.environ.get("CLOUD_NAME", config("CLOUD_NAME", "")),
    "API_KEY": os.environ.get("CLOUD_API_KEY", config("CLOUD_API_KEY", "")),
    "API_SECRET": os.environ.get("CLOUD_API_SECRET", config("CLOUD_API_SECRET", "")),
}


# Test mailtrap email account.... till mail_jet is fully configured
EMAIL_HOST = "smtp.mailtrap.io"
EMAIL_HOST_USER = "617e747e2afc2c"
EMAIL_HOST_PASSWORD = "e99890b04db43b"
EMAIL_PORT = "2525"


# CELERY_BROKER_URL = "redis://localhost:6379/1"



SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [('redis://default:TNaDnuIKgr4PjTCrPZwB@containers-us-west-47.railway.app:6965', 6379)]#[('redis-14998.c9.us-east-1-4.ec2.cloud.redislabs.com', 14998)],
            # 'password':'@Huzkid619'
        },
    },
}

