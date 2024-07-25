import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from users.models import User
from .models import Room
from subjects.models import Element
import random
from urllib.parse import parse_qs

class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.current_vote = [0, 0]
        self.users_voted = {}

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        query_string = self.scope['query_string'].decode()
        # 유저의 구글 계정
        self.google_account = parse_qs(query_string).get('google-account')[0]
        print(self.google_account)
        new_user = await self.get_user_by_account(self.google_account)
        nickname = new_user.nickname
        profile_image_url = new_user.profile_image_url
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'member_enter',
                'google_account': self.google_account,
                'nickname': nickname,
                'profile_image_url': profile_image_url,
            }
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'member_exit',
                'google_account': self.google_account,
                'random': random.choice(['left', 'right'])
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    @database_sync_to_async
    def get_room(self):
        return Room.objects.get(room_id=int(self.room_name))

    @database_sync_to_async
    def get_initial_queue(self):
        room = Room.objects.get(room_id=int(self.room_name))
        subject_id = room.subject_id.subject_id
        elements = list(Element.objects.filter(subject_id=subject_id))
        random.shuffle(elements)
        elements_data = [{
            'element_id': element.element_id,
            'element_name': element.element_name,
            'element_image': element.element_image.url,
            'num_won': element.num_won
        } for element in elements]
        return elements_data
    
    @database_sync_to_async
    def get_user_by_account(self, google_account):
        return User.objects.get(google_account=google_account)
        
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
            initial_queue = await self.get_initial_queue()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'initial_queue',
                    'queue': initial_queue
                }
            )
        elif data['type'] == 'member_enter': 
            google_account = data['google_account']
            new_user = self.get_user_by_account(google_account)
            nickname = new_user.nickname
            profile_image_url = new_user.profile_image_url
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'member_enter',
                    'google_account': google_account,
                    'nickname': nickname,
                    'profile_image_url': profile_image_url,
                }
            )
        elif data['type'] == 'member_exit':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'member_exit',
                    'google_account': data['google_account'],
                    'random': data['random']
                }
            )
        elif data['type'] == 'vote':
            user = data['user']
            select = data['select']
            if not (user in self.users_voted):
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'vote',
                        'user': user,
                        'select': select,
                        'random': random.choice(['left', 'right'])
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
    async def member_enter(self, event):
        print("member_enter")
        await self.send(text_data=json.dumps({
            'type': 'member_enter',
            'google_account': event['google_account'],
            'nickname': event['nickname'],
            'profile_image_url': event['profile_image_url'],
        }))
    async def member_exit(self, event):
        print("member_exit")
        await self.send(text_data=json.dumps({
            'type': 'member_exit',
            'google_account': event['google_account'],
        }))
        user = event['google_account']
        if user in self.users_voted:
            index = self.users_voted[user]
            self.current_vote[index] -= 1
            del self.users_voted[user]
            await self.send(text_data=json.dumps({
                'type': 'vote',
                'left': self.current_vote[0],
                'right': self.current_vote[1],
            }))
        current_users_voted = sum(self.current_vote)
        try:
            room = await self.get_room()
            if (current_users_voted >= room.current_people):
                # vote end
                if self.current_vote[0] > self.current_vote[1]:
                    result = 'left'
                elif self.current_vote[0] < self.current_vote[1]:
                    result = 'right'
                else:
                    result = event['random']
                self.current_vote = [0, 0]
                self.users_voted = {}
                await self.send(text_data=json.dumps({
                    'type': 'vote_end',
                    'result': result,
                }))
        except:
            pass
            
    async def vote(self, event):
        print("vote")
        user = event['user']
        if user not in self.users_voted:
            index = 0 if event['select'] == 'left' else 1
            self.users_voted[user] = index
            self.current_vote[index] += 1
            await self.send(text_data=json.dumps({
                'type': 'vote',
                'left': self.current_vote[0],
                'right': self.current_vote[1],
            }))
            current_users_voted = sum(self.current_vote)
            room = await self.get_room()
            if (current_users_voted >= room.current_people):
                # vote end
                if self.current_vote[0] > self.current_vote[1]:
                    result = 'left'
                elif self.current_vote[0] < self.current_vote[1]:
                    result = 'right'
                else:
                    result = event['random']
                self.current_vote = [0, 0]
                self.users_voted = {}
                await self.send(text_data=json.dumps({
                    'type': 'vote_end',
                    'result': result,
                }))
