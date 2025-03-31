from aiogram import BaseMiddleware
from aiogram.types import (
    Message,
    TelegramObject,
)
import asyncio
from typing import Any, Awaitable, Callable, Dict, List, Union

#мидлварь для обработки альбомов (отдельные message альбомов лежат в data как album: list[message]) 

#а ещё теперь каждое сообщение с атачментом теперь будет дублировать себя в album

DEFAULT_DELAY = 0.6 #задержка для доставки тгшкой сообщений альюбома

#сам в шоке, что этого метода нету у Message
def has_attachments(message: Message) -> bool:
    if message.photo or message.video or message.document or message.audio or message.voice or message.animation:
        return True
    return False

class MediaGroupMiddleware(BaseMiddleware):
    ALBUM_DATA: Dict[str, List[Message]] = {}

    def __init__(self, delay: Union[int, float] = DEFAULT_DELAY):
        self.delay = delay

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if not event.media_group_id:
            if has_attachments(event):
                data["album"] = [event]
                return await handler(event, data)
            return await handler(event, data)
        try:
            self.ALBUM_DATA[event.media_group_id].append(event)
            return  # Don't propagate the event
        except KeyError:
            self.ALBUM_DATA[event.media_group_id] = [event]
            await asyncio.sleep(self.delay)
            data["album"] = self.ALBUM_DATA.pop(event.media_group_id)

        return await handler(event, data)
