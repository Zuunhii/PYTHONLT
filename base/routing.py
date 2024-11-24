# from django.urls import path
# from .consumers import *
#
# websocket_urlpatterns = [
#     path("ws/chatroom/<chatroom_name>", ChatroomConsumer.as_asgi()),
# ]
from django.urls import re_path
from .consumers import ChatroomConsumer

websocket_urlpatterns = [
    re_path(r'ws/chatroom/(?P<room_id>\w+)/$', ChatroomConsumer.as_asgi()),
]
