import asyncio
from collections import defaultdict
from datetime import datetime, timedelta
from functools import wraps
from random import gauss
from typing import Dict

from django.utils import timezone
import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class ActionsConsumer(AsyncWebsocketConsumer):
    actions: Dict = defaultdict(list)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for prop in dir(self):
            handler = getattr(self, prop)
            if (
                callable(handler)
                and prop.startswith("__") == False
                and hasattr(handler, "action")
                and handler.action == True
            ):
                if handler.key not in self.actions.keys():
                    self.actions[handler.key].append(prop)


def action(key):
    @wraps(key)
    def wrapper(handler):
        handler.action = True
        handler.key = key
        return handler

    return wrapper


class UserNotificationsConsumer(ActionsConsumer):

    async def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["id"]
        await self.accept()
        user_group_name = f"user.{self.user_id}"
        await self.channel_layer.group_add(user_group_name, self.channel_name)
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(f"user.{self.user_id}", self.channel_name)
        await super().disconnect(code)
    
    """
    This is a custom decorator i have written that allows me to route messages easier and with more control
    """
    @action(key="offer")
    async def unique_offer(self, event):
        await asyncio.sleep(1) # do something
        await self.send(event["promotion"])

    async def receive(self, text_data):
        message = json.loads(text_data)
        print(f"Message recieved for user: {self.user_id}")
        await self.channel_layer.group_send(f"user.{self.user_id}", message)

    async def action(self, event):
        for handler in self.actions[event["key"]]:
            method = getattr(self, handler)
            await method(event)