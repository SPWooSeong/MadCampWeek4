# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'chat_{self.room_name}'

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']
#         username = data['username']

#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'username': username,
#             }
#         )

#     async def chat_message(self, event):
#         message = event['message']
#         username = event['username']

#         await self.send(text_data=json.dumps({
#             'message': message,
#             'username': username,
#         }))

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room
from subjects.models import Element
import random

class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # 초기 큐 데이터 전송
        initial_queue = await self.get_initial_queue()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'initial_queue',
                'queue': initial_queue
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def get_initial_queue(self):
        room = Room.objects.get(room_id=12)
        subject_id = room.subject_id.subject_id
        print(subject_id)

        print("1")
        elements = list(Element.objects.filter(subject_id=subject_id))
        print(elements)
        print("2")
        random.shuffle(elements)
        elements_data = [{
            'element_id': element.element_id,
            'element_name': element.element_name,
            'element_image': element.element_image.url,
            'num_won': element.num_won
        } for element in elements]
        return elements_data

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'message':
            message = data['message']
            username = data['username']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                }
            )
        elif data['type'] == 'queue_update':
            queue = data['queue']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'queue_update',
                    'queue': queue
                }
            )
        elif data['type'] == 'initial_queue':
            queue = data['queue']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'initial_queue',
                    'queue': queue
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'username': event['username'],
        }))

    async def queue_update(self, event):
        print("queue_update")
        await self.send(text_data=json.dumps({
            'type': 'queue_update',
            'queue': event['queue']
        }))
    async def initial_queue(self, event):
        print("initial_queue")
        await self.send(text_data=json.dumps({
            'type': 'initial_queue',
            'queue': event['queue']
        }))
