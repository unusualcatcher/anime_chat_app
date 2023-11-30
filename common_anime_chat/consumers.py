# from channels.generic.websocket import AsyncWebsocketConsumer
# import json
# from django.contrib.auth.models import User
# from channels.db import database_sync_to_async
# from .models import ChatRoom, Message, Profile
# from channels.db import database_sync_to_async

# @database_sync_to_async
# def save_message_to_database(chatroom_name, username, message):
#     try:
#         chatroom = ChatRoom.objects.get(name=chatroom_name)
#         user = User.objects.get(username=username)
#         user_profile = Profile.objects.get(user=user)

#         new_message = Message.objects.create(chat_room=chatroom, sender=user_profile, content=message)
#         print("Message saved to DB:", new_message)

#     except ChatRoom.DoesNotExist:
#         print(f"Chatroom with name '{chatroom_name}' does not exist.")
    
#     except Profile.DoesNotExist:
#         print(f"User profile with username '{username}' does not exist.")

#     except Exception as e:
#         print(f"Error occurred while saving the message: {e}")

# @database_sync_to_async
# def get_chatroom_by_name(name):
#     try:
#         return ChatRoom.objects.get(name=name)
#     except ChatRoom.DoesNotExist:
#         return None

# @database_sync_to_async
# def get_messages_for_chatroom(chatroom):
#     return Message.objects.filter(chat_room=chatroom).order_by('timestamp')

# class ChatRoomConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.load_previous_messages()

#         await self.accept()
#     @database_sync_to_async
#     def load_previous_messages(self):
#         chatroom = ChatRoom.objects.get(name=self.room_name)
#         messages = Message.objects.filter(chat_room=chatroom).order_by('timestamp')
#         print("MESSAGES INSIDE LOAD FUNCTION:", messages)
#         return messages

#     async def process_messages(self, messages):
#         for message in messages:
#             print("PROCESSING MESSAGE")
#             await self.send_message_to_client(message)

#     async def send_message_to_client(self, message):
#         user_id = message.sender.profile.user_id
#         username = User.objects.get(id=user_id)
#         print("SENDING MESSAGES TO CLIENT")

#         await self.send(text_data=json.dumps({
#             'message': message.content,
#             'username': username,
#             'user_pfp': message.sender.profile_picture.url,
#             'room_name': self.room_name,
#         }))
    
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         username = text_data_json['username']
#         user_pfp = text_data_json['user_pfp']
#         room_name = text_data_json['room_name']

#         await save_message_to_database(chatroom_name=room_name, username=username, message=message)

#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chatroom_message',
#                 'message': message,
#                 'username': username,
#                 'user_pfp': user_pfp,
#                 'room_name': room_name,
#                 'tester_message': 'tester message in receive function'
#             }
#         )

#     async def chatroom_message(self, event):
#         message = event['message']
#         username = event['username']
#         user_pfp = event['user_pfp']

#         await self.send(text_data=json.dumps({
#             'message': message,
#             'username': username,
#             'user_pfp': user_pfp,
#             'tester_message': 'tester message in chatroom message'
#         }))

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.contrib.auth.models import User
# from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from .models import ChatRoom, Message, Profile
from asyncer import asyncify
from django.urls import reverse

@sync_to_async
def save_message_to_database(chatroom_name, username, message):
    try:
        chatroom = ChatRoom.objects.get(name=chatroom_name)
        user = User.objects.get(username=username)
        user_profile = Profile.objects.get(user=user)

        new_message = Message.objects.create(chat_room=chatroom, sender=user_profile, content=message)
        print("Message saved to DB:", new_message)

    except ChatRoom.DoesNotExist:
        print(f"Chatroom with name '{chatroom_name}' does not exist.")
    
    except Profile.DoesNotExist:
        print(f"User profile with username '{username}' does not exist.")

    except Exception as e:
        print(f"Error occurred while saving the message: {e}")
@sync_to_async
def get_chatroom_by_name(name):
    try:
        return ChatRoom.objects.get(name=name)
    except ChatRoom.DoesNotExist:
        return None
@sync_to_async
def get_messages_for_chatroom(chatroom):
    return list(Message.objects.filter(chat_room=chatroom).order_by('timestamp'))

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        print("Before getting chatroom")
        chatroom = await get_chatroom_by_name(self.room_name)
       
        print("chatroom:",chatroom)
    
        print("Chatroom:",chatroom)
        messages = await get_messages_for_chatroom(chatroom.id)
        for message in messages:
            print("SENDING MESSAGE TO FUNCTION")
            await self.send_message_to_client(message)
        


    async def send_message_to_client(self, message):
        user_id = await sync_to_async(lambda: message.sender.user_id)()
        user = await sync_to_async(lambda: User.objects.get(id=user_id))()
        print("SENDING MESSAGES TO THE FRONTEND")
        user_profile_url = reverse('view-profile', kwargs={'user_id': user_id})
        await self.send(text_data=json.dumps({
            'message': message.content,
            'username': user.username,
            'user_pfp': message.sender.profile_picture.url,
            'room_name': self.room_name,
            'tester_message':'tester message in send_message_to_client function',
            'user_profile_url':user_profile_url
        }))
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        user_pfp = text_data_json['user_pfp']
        room_name = text_data_json['room_name']


        await save_message_to_database(chatroom_name=room_name, username=username, message=message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'username': username,
                'user_pfp': user_pfp,
                'room_name': room_name,
                'tester_message': 'tester message in receive function',
            }
        )

    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']
        user_pfp = event['user_pfp']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'user_pfp': user_pfp,
            'tester_message': 'tester message in chatroom message',
            
        }))
