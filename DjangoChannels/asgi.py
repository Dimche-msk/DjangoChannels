"""
ASGI config for ChannelsWS project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoChannels.settings')
# Важно сделать в начале!!!

django_asgi_app = get_asgi_application()

from CustomUsers import routing as custom_users_routing

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": django_asgi_app,

    # WebSocket chat handler
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                custom_users_routing.websocket_urlpatterns # + custom_users_routing.websocket_urlpatterns_ДРУГОЕ приложение
            )
        )
    ),
})
