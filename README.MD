# Install
uvicorn==0.34.3
channels==4.2.2

# Настройка проекта

в settings: ASGI_APPLICATION
в корне проекта asgi.py корень маршрутизатора


## Настройка Pycharm запуск проекта (запускаем uvicorn, как HTTP и WS сервер)
Run/Debug Configurations

Слева выбираем Python. 
Справа:
1. Имя - пофиг, пишем uvicorn
2. **Важно**: тип ставим **module**
3. **важно** скрипт - uvicorn
4. **важно** параметр скрипта: - в asgi.py файле в корне проекта, путь к переменной, в которой лежит ASGI-приложение (application = get_asgi_application()).asgi: (выглядит так ChannelsWS.asgi:application)
5. **важно** Working directory: к внешней папке проекта (где manage.py)


# Как использовать:
## Маршрутизация запросов

Основной маршрутизатор, который выделяет протокол и потом распределяет запрос на конкретного обработчика живет в файле asgi.py в корне проекта (рядом с settings)

Тут происходит такая магия:
```python asgi.py
application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": django_asgi_app,

    # WebSocket chat handler
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                custom_users_routing.websocket_urlpatterns # + custom_users_routing.websocket_urlpatterns_ДРУГОЕ приложение
            )
        )
    ),
})
```
Запросы HTTP (https мы уже сняли на nginx) идут на "родной" обработчик Django
Запросы WS (wss мы уже сняли на nginx) идут на "родной" обработчик Channels

Маршрутизация самих запросов, после того, как поняли, что: 
1. это WS
2. Проверен CSRF
3. Если есть сессионная кука - заполнится self.scope["user"] - НАДО ПРОВЕРЯТЬ ПЕРЕД ТЕМ

Прописываем маршруты внутри приложения, кажждый маршрут смотрит на свой класс-консьюмер
```python routing.py
from django.urls import path
from .consumers import EchoConsumerText, EchoConsumerJSON

websocket_urlpatterns = [
    path("echo-text/", EchoConsumerText.as_asgi()),
    path("echo-json/", EchoConsumerJSON.as_asgi()),
]
```

## Consumer - Класс принимает WS и обрабатывает его
Consumer - это класс, они живут в каждом приложении (по несколько штук) в consumers.py
каждый консьюмер обрабатывает один тип запроса (один url). Можно смаршрутизить и несколько на одного, но это путаница.
```consumers.py
from channels.consumer import AsyncConsumer, SyncConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer, JsonWebsocketConsumer

class EchoConsumerText(AsyncConsumer):
    async def websocket_connect(self, event):
      ...    
    async def websocket_receive(self, event):
      ...
    async def websocket_disconnect(self, close_code):
      ...

class EchoConsumerJSON(AsyncJsonWebsocketConsumer):
    async def websocket_connect(self, event):
      ...
    async def websocket_receive(self, event):
      ...
```

**Синхронный** consumer будет запускаться в отдельном **Thread** при каждом подключении к ws
**А-Синхронный** consumer будет крутиться в event-loop Uvicorn


#  Прод схема
Строка запуска прод:
```shell
gunicorn your_project_name.asgi:application -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```
Общая схема взаимодействия:
Интернет-пользователь <--> Nginx <--> Gunicorn (с Uvicorn воркерами) <--> Django ASGI-приложение

Пошаговое описание работы:
1. Запрос от пользователя: Пользователь (например, через браузер) отправляет HTTP-запрос на ваш сервер (например, на yourdomain.com).
2. Nginx принимает запрос:•Nginx — это первый, кто "встречает" этот запрос. Он слушает стандартные порты (обычно 80 для HTTP и 443 для HTTPS).•
    - Обработка статики (если настроено)
    - Обработка SSL
    - Проксирование динамических запросов
3. Gunicorn получает запрос от Nginx:•
   - В команде ```gunicorn your_project_name.asgi:application -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000``` 
   - Gunicorn слушает на 0.0.0.0:8000. 
   - Nginx настроен так, чтобы перенаправлять запросы именно на этот адрес и порт (например, http://127.0.0.1:8000 или http://localhost:8000, если Nginx и Gunicorn работают на одном сервере).
   - Gunicorn, как менеджер процессов, выбирает один из своих свободных Uvicorn-воркеров для обработки этого запроса.
4. Uvicorn-воркер обрабатывает запрос:
   - Выбранный Uvicorn-воркер получает запрос от Gunicorn.
   - Uvicorn, будучи ASGI-сервером, взаимодействует с Django ASGI-приложением (your_project_name.asgi:application).
   - Если это обычный HTTP-запрос, он будет обработан соответствующими Django views.
   - Если это WebSocket-соединение, Uvicorn будет управлять этим соединением, передавая данные между клиентом и Django Channels consumers.
5. Приложение формирует ответ: 
   - Django-приложение (views или consumers) обрабатывает запрос и формирует ответ.
6. Ответ возвращается по цепочке:
   - Ответ от Django-приложения передается Uvicorn-воркеру.
   - Uvicorn-воркер передает ответ Gunicorn'у.
   - Gunicorn передает ответ Nginx'у.
   - Nginx передает финальный HTTP-ответ обратно интернет-пользователю.
### Конфигурация Nginx для такой схемы:
В конфигурационном файле Nginx (обычно в /etc/nginx/sites-available/your_project_name или аналогичном) будет блок location, который отвечает за проксирование запросов к Gunicorn. 
Он может выглядеть примерно так:
```editorconfig
    myServer {
                listen 80;
                server_name yourdomain.com www.yourdomain.com;

                # Настройки для статических файлов (опционально, но рекомендуется)
                location /static/ {
                    alias /path/to/your/project/staticfiles/; # Путь к вашим собранным статическим файлам
                }

                location /media/ {
                    alias /path/to/your/project/media/; # Путь к вашим медиа файлам
                }

                # Проксирование всех остальных запросов на Gunicorn
                location / {
                    proxy_pass http://127.0.0.1:8000; # Адрес и порт, на котором слушает Gunicorn
                    proxy_set_header Host $host;
                    proxy_set_header X-Real-IP $remote_addr;
                    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                    proxy_set_header X-Forwarded-Proto $scheme;

                    # Настройки для WebSocket (если используются)
                    proxy_http_version 1.1;
                    proxy_set_header Upgrade $http_upgrade;
                    proxy_set_header Connection "upgrade";
                }
            }
```
