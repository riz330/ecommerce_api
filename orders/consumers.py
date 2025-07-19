# from channels.generic.websocket import AsyncWebsocketConsumer
# import json
# from django.contrib.auth import get_user_model
# from channels.layers import get_channel_layer

# User = get_user_model()

# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         if self.scope['user'].is_anonymous:
#             await self.close()
#         else:
#             self.user = self.scope['user']
#             self.group_name = f'user_{self.user.id}'

#             # Join user group
#             await self.channel_layer.group_add(
#                 self.group_name,
#                 self.channel_name
#             )
#             await self.accept()

#     async def disconnect(self, close_code):
#         if not self.scope['user'].is_anonymous:
#             await self.channel_layer.group_discard(
#                 self.group_name,
#                 self.channel_name
#             )

#     async def notify(self, event):
#         """Receive notification from group and send it to WebSocket"""
#         await self.send(text_data=json.dumps(event['data']))


# # ✅ Call this function from your views or business logic using: await send_notification(user_id, data)
# async def send_notification(user_id, data):
#     channel_layer = get_channel_layer()
#     await channel_layer.group_send(
#         f'user_{user_id}',
#         {
#             'type': 'notify',
#             'data': data
#         }
#     )


from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.group_name = f'user_{self.scope["user"].id}'
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message')
            
            if message:
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'notification.message',
                        'message': message
                    }
                )
        except json.JSONDecodeError:
            pass

    async def notification_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))