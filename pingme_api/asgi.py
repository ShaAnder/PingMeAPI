"""
ASGI config for pingme_api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from messenger import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pingme_api.settings')

application = ProtocolTypeRouter({
  # standard http handling
  "http": get_asgi_application(),
  # WebSocket handling
  "websocket": AuthMiddlewareStack(
    URLRouter(
      # Add messenger app's WebSocket routing
      routing.websocket_urlpatterns
    )
  )
})
