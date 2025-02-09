import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message, ChatRoom

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.product_id = self.scope["url_route"]["kwargs"]["product_id"]
        self.buyer_id = self.scope["url_route"]["kwargs"]["buyer_id"]
        self.room_group_name = f"chat_{self.product_id}_{self.buyer_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = text_data.strip()
        sender = self.scope["user"]

        chat = await ChatRoom.objects.aget(product_id=self.product_id, buyer_id=self.buyer_id)
        msg = await Message.objects.acreate(room=chat, sender=sender, content=data)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": f"<b>{sender.username}:</b> {msg.content}",
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))