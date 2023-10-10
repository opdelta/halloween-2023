# consumers.py

import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

class YourConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass # Do nothing

    async def some_event_handler(self, event):
        # Handle SSE or WebSocket events here
        await self.send(text_data=json.dumps(event))