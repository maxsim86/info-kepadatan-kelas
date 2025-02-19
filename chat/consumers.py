import json
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


from django.contrib.auth.models import User
from .models import Conversation, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # authentication (JWT)
        await self.authenticate()

        # join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # Get or create conversation
        self.conversation = await self.get_or_create_conversation()
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']
        # Send back to the same user
        await self.save_message(message_content)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'sender': self.scope['user'].username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']


        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
        
    @database_sync_to_async
    async def authenticate(self):
        try:
            auth_header =dict(self.scope['headers']).get(b'authorization',b'').decode()
            if auth_header.startswitch('Bearer '):
                
                jwt_token = auth_header.split(' ')
            else:
                await self.close()
            validated_token = JWTAuthentication().get_validated_token(jwt_token)
            user = JWTAuthentication().get_user(validated_token)

            if user is not None and user.is_authenticated:
                self.scope['user']=user
            else:
                await self.close()
        except Exception as e:
            print(f"Authentication error: {e}")
            await self.close() # now i can use await here

    @database_sync_to_async
    def get_or_create_conversation(self):
        participants = [self.scope['user'], User.objects.first()]
        conversation, created = Conversation.objects.get_or_create(
            participants__in=participants,
            participants__count= len(participants)
        )
        if created:
            conversation.participants.set(participants)
        return conversation
    @database_sync_to_async
    def save_message(self, message_content):
        Message.objects.create(
            conversation=self.conversation,
            sender = self.scope['user'],
            content = message_content
        )