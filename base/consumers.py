from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from .models import *
import json

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room = get_object_or_404(Room, id=self.room_id)

        async_to_sync(self.channel_layer.group_add)(
            self.room_id, self.channel_name
        )

        self.accept()
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_id, self.channel_name
        )
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']

        message = Message.objects.create(
            body = body,
            user = self.user,
            room = self.room
        )

        event = {
            'type': 'message_handler',
            'message_id': message.id
        }
        async_to_sync(self.channel_layer.group_send)(
            self.room_id, event
        )

    def message_handler(self, event):
        message_id = event["message_id"]
        message = Message.objects.get(id=message_id)
        html = render_to_string('partials/message_p.html', {'message': message, 'user': self.user})
        self.send(text_data=html)