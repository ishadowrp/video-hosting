import json
import datetime

from django.core.exceptions import ObjectDoesNotExist

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from comments_and_chats.models import Message, PrivatChat, Comment
from media_storage.models import Media
from accounts.models import ProfileData, Notification


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        type_chat = text_data_json['type_chat']
        created = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'username': str(self.scope["user"]),
                'userID': str(self.scope["user"].pk),
                'created': created,
                'message': message
            }
        )
        if type_chat == 'chat':
            await self.create_message(message)
        else:
            await self.create_comment(message)

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def profile_photo(self):
        try:
            profile = ProfileData.objects.get(owner__pk=self.scope["user"].pk).avatar
        except ObjectDoesNotExist:
            profile = 'none'
        return profile

    @database_sync_to_async
    def create_message(self, message):
        try:
            chat = PrivatChat.objects.get(id=int(self.room_name))
            Message.objects.create(chat=chat, author=self.scope["user"], content=message)
        except ObjectDoesNotExist:
            print('chat not found')

    @database_sync_to_async
    def create_comment(self, message):
        try:
            chat = Media.objects.get(id=int(self.room_name))
            Comment.objects.create(media=chat, author=self.scope["user"], content=message)
        except ObjectDoesNotExist:
            print('chat not found')


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'notification_%s' % self.room_name

        # Join notifications group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave notifications group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        notification_id = text_data_json['notification_id']
        status = text_data_json['status']
        # Send message to room group
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'username': str(self.scope["user"]),
        #         'userID': str(self.scope["user"].pk),
        #         'created': created,
        #         'message': {
        #             'notification_id': notification_id,
        #             'message': message,
        #             'status': status
        #         },
        #     }
        # )

        await self.change_status(notification_id, status)

    async def send_notification(self, notification):
        self.room_name = self.scope['url_route']['kwargs'][str(notification.user)]
        self.room_group_name = 'notification_%s' % self.room_name
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'notification_id': str(notification.pk),
                'username': str(notification.user),
                'userID': str(notification.user.pk),
                'created': notification.created,
                'message': notification.message,
                'status': notification.status_read
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def change_status(self, notification_id, status):
        if status:
            try:
                notification = Notification.objects.get(id=int(notification_id))
                notification.status_read = True
                notification.save()
            except ObjectDoesNotExist:
                print('notification not found')
