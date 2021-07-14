from dataclasses import field
from datetime import time
from io import BufferedReader
from typing import Any, Union, Optional, TYPE_CHECKING

import httpx
from nonebot.log import logger
from nonebot.message import handle_event
from nonebot.adapters import Bot as BaseBot
from nonebot.typing import overrides

from .event import *
from .config import Config as TelegramConfig
from .message import Message, MessageSegment

if TYPE_CHECKING:
    from nonebot.config import Config
    from nonebot.drivers import Driver


class Bot(BaseBot):
    """
    telegram bot 适配。继承属性参考 `BaseBot <./#class-basebot>`_ 。
    """

    telegram_config: TelegramConfig

    def __init__(self, connection_type: str, self_id: str):
        super().__init__(connection_type, self_id)

    @property
    @overrides(BaseBot)
    def type(self) -> str:
        """
        - 返回: ``"telegram"``
        """
        return "telegram"

    @classmethod
    def register(cls, driver: "Driver", config: "Config"):
        super().register(driver, config)
        cls.telegram_config = TelegramConfig(**config.dict())

    @classmethod
    async def check_permission(
        cls, driver: "Driver", connection_type: str, headers: dict, body: Optional[dict]
    ) -> str:
        return cls.telegram_config.token.split(":", maxsplit=1)[0]

    async def handle_message(self, message: dict):
        try:
            post_type = list(message.keys())[1]
            message = message[post_type]
            if post_type == "message" or post_type == "channel_post":
                event = MessageEvent.parse_obj(message)
                if event.chat.type == "private":
                    event = PrivateMessageEvent.parse_obj(message)
                elif event.chat.type == "channel":
                    event = ChannelPostEvent.parse_obj(message)
                else:
                    event = GroupMessageEvent.parse_obj(message)
                event.message = Message(message)
            elif post_type == "edited_message" or post_type == "edited_channel_post":
                event = EditedMessageEvent.parse_obj(message)
                if event.chat.type == "private":
                    event = PrivateEditedMessageEvent.parse_obj(message)
                elif event.chat.type == "channel":
                    event = EditedChannelPostEvent.parse_obj(message)
                else:
                    event = GroupEditedMessageEvent.parse_obj(message)
                event.message = Message(message)
            elif post_type == "my_chat_member" or post_type == "chat_member":
                event = ChatMemberUpdatedEvent.parse_obj(message)
            await handle_event(self, event)
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                f"<r><bg #f8bbd0>Failed to handle event. Raw: {message}</bg #f8bbd0></r>"
            )

    async def _call_api(self, api: str, **data) -> Any:
        # 将方法名称改为驼峰式
        api = api.split("_", maxsplit=1)[0] + "".join(
            s.capitalize() for s in api.split("_")[1:]
        )

        # 分离要上传的文件
        files = {}
        for key in data:
            if isinstance(data[key], BufferedReader):
                files[key] = data[key]
        data = {key: str(data[key]) for key in data if key not in files}

        # TODO 简单的 httpx 调用，等 a14 实装了正向 Driver 再改
        async with httpx.AsyncClient(
            proxies=self.telegram_config.proxy, timeout=10
        ) as client:
            response = await client.post(
                f"{self.telegram_config.api_server}bot{self.telegram_config.token}/{api}",
                data=data,
                files=files,
            )
        return response

    async def send(
        self, event: Event, message: Union[str, Message, MessageSegment], **kwargs
    ) -> Any:
        """
        TODO

        因为 Telegram 对于不同类型的消息有不同的 API，如果需要批量发送不同类型的消息请尽量使用此方法
        """
        if isinstance(message, str):
            await self.send_message(chat_id=event.chat.id, text=message)
        elif isinstance(message, Message):
            for seg in message:
                pass
        else:
            if message.type == "photo":
                await self.send_photo(chat_id=event.chat.id, **message.data)
