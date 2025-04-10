# messenger/routing.py

from django.urls import re_path
from . import consumers  # Import consumers where our WebSocket logic lives

# Define WebSocket URL patterns specific to messenger (chat) app
websocket_urlpatterns = [
    re_path(r'ws/messenger/(?P<other_user_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]