import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OrderStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if self.user.is_authenticated:
            self.group_name = f"user_{self.user.id}"

            # Join group
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )

            await self.accept()

            # Optional: Send confirmation on connect
            await self.send(text_data=json.dumps({
                "message": "Connected!"
            }))
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    # Handler method for group message
    async def order_status(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))
