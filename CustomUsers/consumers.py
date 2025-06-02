import asyncio
from datetime import datetime
from channels.consumer import AsyncConsumer, SyncConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer, JsonWebsocketConsumer
"""
Важно про AsyncConsumer, SyncConsumer

SyncConsumer (СИНХРОННЫЙ) запускается в отдельном Threed, (количество - ограничено, накладные расходы)

AsyncConsumer - запускается в event-loop Uvicorn-a. 

Вывод:
Тяжелые, вычислительные задачи лучше делать в синхронном варианте
Легкие, небольшие лучше делать в асинхронном
"""

class EchoConsumerText(AsyncConsumer):

    async def websocket_connect(self, event):
        print(f'Старт соединения, event={event}, юзер = {self.scope["user"]}')
        await self.send({
            "type": "websocket.accept",
        })


    async def websocket_receive(self, event):
        print(f'Received message {event} from user={self.scope["user"]}')
        await self.send({
            "type": "websocket.send",
            "text": event["text"],
        })
        await asyncio.sleep(10)
        await self.send({
            "type": "websocket.send",
            "message":"Not allowed"
        })
        await asyncio.sleep(1.0)
        await self.close(code=1000)

    async def websocket_disconnect(self, close_code):
        print(f'Соединение закрылось, код {close_code} user={self.scope["user"]}')

class EchoConsumerJSON(AsyncJsonWebsocketConsumer):
    async def websocket_connect(self, event):
        user = self.scope.get("user")
        if user and user.is_authenticated:
            await self.accept()
            # Пользователь аутентифицирован, можно продолжать
            print(f"User {user.username} connected.")
        else:
            # Пользователь не аутентифицирован или user не найден в scope
            print("Anonymous user or authentication failed. Closing connection.")
            await self.close(
                code=4003)  # 4003 - кастомный код "Permission Denied" или стандартный 1008 "Policy Violation"

        print(f'Старт JSON соединения, event={event}')
        await self.send_json({
            "type": "websocket.accept",
            "datetime":datetime.now().astimezone()
        })

    async def websocket_receive(self, event):
        print(f'Received JSON message {event} from user={self.scope["user"]}')
        await self.send_json({
            "type": "websocket.send",
            "text": event["text"],
        })
        await asyncio.sleep(10)
        await self.send_json({
            "type": "websocket.send",
            "message":"Not allowed"
        })
        await asyncio.sleep(1.0)
        await self.close(code=1000)

    async def websocket_disconnect(self, close_code):
        print(f'Соединение закрылось, код {close_code} user={self.scope["user"]}')


class GetUserInfo(AsyncJsonWebsocketConsumer):
    async def websocket_connect(self, event):
        if self.scope["user"].is_authenticated:
            print(f'Запрос данных пользователя , event={event}, юзер = {self.scope["user"]}')
            await self.accept()
            await asyncio.sleep(1.0)
            await self.send_json({
                "type": "websocket.send",
                "message":{"id":self.scope["user"].id,"first_name":self.scope["user"].first_name,"last_name":self.scope["user"].last_name,"email":self.scope["user"].email}
            })
            await asyncio.sleep(1.0)
            await self.close(code=1000)
        else:
            await self.close(code=500)


    async def disconnect(self, close_code):
        print(f'Соединение закрылось, код {close_code} user={self.scope["user"]}')