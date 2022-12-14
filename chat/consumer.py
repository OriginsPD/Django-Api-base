import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from .models import (Room, Message)


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None

    @database_sync_to_async
    def _get_Room(self):
        return Room.objects.get(name=self.room_name)

    @database_sync_to_async
    def _save_message(self, message):
        return Message.objects.create(user=self.user,
                                      room=self.room,
                                      content=message)

    @async_to_sync
    def _get_online_user(self):
        return [user.username for user in self.room.online.all()]

    @async_to_sync
    def _add_user_add(self, user):
        return self.room.join(user)

    def _remove_user(self, user):
        return self.room.leave(user)

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.room = self._get_Room(self)
        self.user = self.scope['user']

        # connection has to be accepted
        await self.accept()

        # Join room group
        await self.channel_layer.group_add(self.room_group_name,
                                           self.channel_name)

        # send the user list to the newly joined user
        self.send(json.dumps({
            'type': 'user_list',
            'users': self._get_online_user(self),
        }))

        if self.user.is_authenticated:
            # send the join event to the room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_join',
                    'user': self.user.username,
                }
            )
            self._add_user_add(self, self.user)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name,
                                               self.channel_name)

        if self.user.is_authenticated:
            # send the leave event to the room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_leave',
                    'user': self.user.username,
                }
            )
            self._remove_user(self, self.user)
            return super().disconnect(close_code)

    # Receive message from WebSocket

    async def receive(self, text_data, **kwargs):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        if not self.user.is_authenticated:
            return

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user': self.user.username,
                'message': message,
            }
        )

        await self._save_message(self, message)
        return super().receive(text_data, **kwargs)

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    async def user_join(self, event):
        self.send(text_data=json.dumps(event))

    async def user_leave(self, event):
        self.send(text_data=json.dumps(event))
