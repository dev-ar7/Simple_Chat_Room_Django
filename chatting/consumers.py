import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chatbox_%s' % self.room_name

        # JOIN ROOM GROUP
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.room_name
        )
        self.accept()

    def disconnect(self, code):
        # LEAVE ROOM GROUP
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # RECIVE MESSAGE FROM WEBSOCKET
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # SEND MESSAGE TO ROOM_GROUP
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        # RECIVE MESSAGE FROM ROOM_GROUP
        message = event['message']

        # SEND MESSAGE TO WEBSOCKET
        self.send(text_data=json.dumps({
            'message': message
        }))
