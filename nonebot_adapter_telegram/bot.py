from typing import Any, Mapping, Union, Optional, TYPE_CHECKING

import httpx
from nonebot.log import logger
from nonebot.message import handle_event
from nonebot.adapters import Bot as BaseBot
from nonebot.exception import RequestDenied
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
        # 检查连接方式
        if connection_type != "http":
            logger.warning("Unsupported connection type")
            raise RequestDenied(405, "Unsupported connection type")
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
            await handle_event(self, event)
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                f"<r><bg #f8bbd0>Failed to handle event. Raw: {message}</bg #f8bbd0></r>"
            )

    async def _call_api(self, api: str, **data) -> Any:
        api = api.split("_",maxsplit=1)[0] + "".join(s.capitalize() for s in api.split("_")[1:])
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.telegram_config.api_server}bot{self.telegram_config.token}/{api}",
                json=data,
            )
        return response

    async def send(
        self, event: Event, message: Union[str, Message, MessageSegment], **kwargs
    ) -> Any:
        await self.send_message(chat_id=event.chat.id,text = message)
