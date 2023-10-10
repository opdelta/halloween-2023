# routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from your_app import consumers

application = ProtocolTypeRouter({
    # Use URLRouter to route WebSocket requests
    "websocket": URLRouter([
        path("ws/countdown/", consumers.YourConsumer.as_asgi()),
        # Add more WebSocket routes as needed
    ]),
})