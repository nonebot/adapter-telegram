import json
from typing import Any, Union, Optional, Tuple, TYPE_CHECKING

import httpx
from nonebot.log import logger
from nonebot.message import handle_event
from nonebot.adapters import Bot as BaseBot
from nonebot.typing import overrides
from nonebot.drivers import Driver, HTTPConnection, HTTPResponse

from .event import Event
from .config import Config as TelegramConfig
from .message import Message, MessageSegment

if TYPE_CHECKING:
    from nonebot.config import Config


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
        cls, driver: Driver, request: HTTPConnection
    ) -> Tuple[Optional[str], Optional[HTTPResponse]]:
        # TODO Telegram 的 Webhook 方式完全不带机器人本身的标识符，所以只能默认所有上报都通过
        return cls.telegram_config.token.split(":", maxsplit=1)[0], HTTPResponse(204)

    async def handle_message(self, message: bytes):
        try:
            message: dict = json.loads(message)
            event = Event.parse_event(message)
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

        # TODO 简单的 httpx 调用，等 a14 稳定实装了正向 Driver 再改
        async with httpx.AsyncClient(
            proxies=self.telegram_config.proxy, timeout=10
        ) as client:
            response = await client.post(
                f"{self.telegram_config.api_server}bot{self.telegram_config.token}/{api}",
                json=data,
            )
        return response.text

    async def send(
        self, event: Event, message: Union[str, Message, MessageSegment], **kwargs
    ) -> Any:
        """
        TODO

        由于 Telegram 对于不同类型的消息有不同的 API，如果需要批量发送不同类型的消息请尽量使用此方法
        """
        if isinstance(message, str):
            response = await self.send_message(chat_id=event.chat.id, text=message)
        elif isinstance(message, MessageSegment):
            if message.type == "text":
                response = await self.send_message(
                    chat_id=event.chat.id, text=message.data.get("text")
                )
        else:
            for seg in message:
                if seg.type == "text":
                    response = await self.send_message(
                        chat_id=event.chat.id, text=seg.data.get("text")
                    )
        return response
