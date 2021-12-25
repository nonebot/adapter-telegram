from typing import Any, Union

from nonebot.adapters import Adapter
from nonebot.adapters import Bot as BaseBot
from nonebot.typing import overrides

from .config import BotConfig
from .event import Event
from .message import Message, MessageSegment


class Bot(BaseBot):
    """
    Telegram Bot 适配。继承属性参考 `BaseBot <./#class-basebot>`_ 。
    """

    def __init__(self, adapter: "Adapter", config: BotConfig):
        self.adapter = adapter
        self.self_id = config.token.split(":")[0]
        self.bot_config: BotConfig = config

    @overrides(BaseBot)
    async def send(
        self, event: Event, message: Union[str, Message, MessageSegment], **kwargs
    ) -> Any:
        """
        由于 Telegram 对于不同类型的消息有不同的 API，如果需要批量发送不同类型的消息请尽量使用此方法，Nonebot 将会自动帮你转换成多条消息。
        """
        if isinstance(message, str):
            response = await self.send_message(chat_id=event.chat.id, text=message)
        elif isinstance(message, MessageSegment):
            if message.type == "text":
                response = await self.send_message(
                    chat_id=event.chat.id, text=message.data.get("text")
                )
            elif message.type in [
                "animation",
                "audio",
                "document",
                "photo",
                "video",
                "voice",
            ]:
                response = await self.call_api(
                    f"send_{message.type}",
                    chat_id=event.chat.id,
                    **{
                        message.type: message.data.get("file"),
                        "caption": message.data.get("caption"),
                    },
                )
        else:
            for seg in message:
                if seg.type == "text":
                    response = await self.send_message(
                        chat_id=event.chat.id, text=seg.data.get("text")
                    )
        return response
