"""
ASGI config for RentRite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RentRite.settings")

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM or models.

django_asgi = get_asgi_application()

from utils.auth.AuthMiddleware import JWTAuthMiddleWareStack  # noqa
import chat.routing  # noqa


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            JWTAuthMiddleWareStack(URLRouter(chat.routing.websocket_urlpatterns))
        ),
    }
)
