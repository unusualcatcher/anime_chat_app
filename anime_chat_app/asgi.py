"""
ASGI config for anime_chat_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import common_anime_chat.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anime_chat_app.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(
        common_anime_chat.routing.websocket_urlpatterns
    ),
})
