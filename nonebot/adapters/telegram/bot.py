import inspect
from uuid import uuid4
from functools import partial
from typing_extensions import override
from typing import Any, Union, Optional, cast

from pydantic import TypeAdapter
from nonebot.message import handle_event

from nonebot.adapters import Adapter
from nonebot.adapters import Bot as BaseBot

from .api import API
from .config import BotConfig
from .exception import ApiNotAvailable
from .model import InputMedia, ReplyParameters
from .message import File, Entity, Message, UnCombinFile, MessageSegment
from .event import (
    Event,
    MessageEvent,
    EventWithChat,
    GroupMessageEvent,
    PrivateMessageEvent,
)


class Bot(BaseBot, API):
    """
    Telegram Bot 适配。继承属性参考 `BaseBot <./#class-basebot>`_ 。
    """

    def __init__(
        self,
        adapter: "Adapter",
        self_id: str,
        *,
        config: Optional[BotConfig] = None,
    ):
        if not config:
            raise ValueError("config is required")

        super().__init__(adapter, self_id)
        self.username: Optional[str] = None
        self.bot_config = config
        self.secret_token = uuid4().hex

    @staticmethod
    def get_bot_id_by_token(token: str) -> str:
        return token.split(":")[0]

    def _check_tome(self, event: MessageEvent):
        def process_first_segment(message: Message):
            if not message:
                message.append(Entity.text(""))
            elif message[0].is_text():
                message[0].data["text"] = message[0].data["text"].lstrip()
                if not str(message[0]):
                    del message[0]
                    process_first_segment(message)

        if (
            event.reply_to_message
            and (
                isinstance(event.reply_to_message, GroupMessageEvent)
                or isinstance(event.reply_to_message, PrivateMessageEvent)
            )
            and str(event.reply_to_message.from_.id) == self.self_id
        ):
            event._tome = True
            return

        segment = event.message[0]
        if segment.type == "mention":
            if segment.data.get("text", "")[1:] == self.username:
                del event.message[0]
                process_first_segment(event.message)
                event._tome = True
        elif segment.type == "text":
            text = str(segment)
            for nickname in self.config.nickname:
                if nickname in text:
                    event.message[0].data["text"] = text.replace(nickname, "", 1)
                    process_first_segment(event.message)
                    event._tome = True
                    break

    async def handle_event(self, event: Event):
        if isinstance(event, MessageEvent):
            self._check_tome(event)
        await handle_event(self, event)

    async def call_api(self, api: str, *args: Any, **kargs: Any) -> Any:
        if hasattr(API, api):
            sign = inspect.signature(getattr(API, api))
            args_ = list(args)
            for param in sign.parameters.values():
                if param.name != "self" and param.name not in kargs:
                    try:
                        kargs[param.name] = args_.pop(0)
                    except IndexError:
                        kargs[param.name] = None
            return TypeAdapter(sign.return_annotation).validate_python(
                await super().call_api(api, **kargs)
            )
        return await super().call_api(api, **kargs)

    def __getattribute__(self, __name: str) -> Any:
        if not __name.startswith("__") and hasattr(API, __name):
            return partial(self.call_api, __name)
        return object.__getattribute__(self, __name)

    # TODO 重构
    async def send_to(
        self,
        chat_id: Union[int, str],
        message: Union[str, Message, MessageSegment],
        message_thread_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,  # Deprecated
        allow_sending_without_reply: Optional[bool] = None,  # Deprecated
        media_group_caption_index: int = 0,  # 非 Telegram 原生参数
        **kwargs,
    ):
        """
        由于 Telegram 对于不同类型的消息有不同的 API，
        如果需要使用同一方法发送不同类型的消息请使用此方法。

        - `File` 或 `Entity` 可随意组合
        - 非 `File` 非 `Entity` 的 `MessageSegment` 无法组合
        """
        kwargs.update(
            {
                "disable_notification": disable_notification,
                "protect_content": protect_content,
                "reply_to_message_id": reply_to_message_id,
                "allow_sending_without_reply": allow_sending_without_reply,
            },
        )

        # 普通文本
        if isinstance(message, str):
            return await self.send_message(
                chat_id=chat_id,
                message_thread_id=message_thread_id,
                text=message,
                **kwargs,
            )

        # 单个 segment
        if isinstance(message, MessageSegment):
            if isinstance(message, Entity):
                return await self.send_message(
                    chat_id=chat_id,
                    message_thread_id=message_thread_id,
                    text=str(message),
                    entities=Entity.build_telegram_entities(Message(message)),
                    **kwargs,
                )

            if isinstance(message, File):
                return await self.call_api(
                    f"send_{message.type}",
                    chat_id=chat_id,
                    message_thread_id=message_thread_id,
                    **{message.type: message.data["file"]},
                    **kwargs,
                )

            return await self.call_api(
                f"send_{message.type}",
                chat_id=chat_id,
                message_thread_id=message_thread_id,
                **message.data,
                **kwargs,
            )

        # 处理 Message 的发送
        # 分离各类型 seg
        reply_parameters = None
        if (reply_count := message.count("reply")) > 1:
            raise ApiNotAvailable
        elif reply_count:
            reply_parameters = ReplyParameters(**message["reply", 0].data)
            message = message.exclude("reply")

        entities = Message(x for x in message if isinstance(x, Entity))
        files = Message(
            x
            for x in message
            if isinstance(x, File) and not isinstance(x, UnCombinFile)
        )
        others = Message(
            x
            for x in message
            if not (isinstance(x, (Entity, File))) or isinstance(x, UnCombinFile)
        )

        if others:
            # 如果只能单独发送的消息段和其他消息段在一起，那么抛出错误
            if len(others) > 1 or files or entities:
                raise ApiNotAvailable
            other = others[0]
            return await self.call_api(
                f"send_{other.type}",
                chat_id=chat_id,
                message_thread_id=message_thread_id,
                **other.data,
                reply_parameters=reply_parameters,
                **kwargs,
            )

        # 发送纯文本消息
        if not files:
            return await self.send_message(
                chat_id=chat_id,
                message_thread_id=message_thread_id,
                text=str(message),
                entities=Entity.build_telegram_entities(entities),
                reply_parameters=reply_parameters,
                **kwargs,
            )

        # 发送带文件的消息
        if len(files) > 1:
            # animation 和 voice 不能组合发送
            if any(file.type in ("voice", "animation") for file in files):
                raise ApiNotAvailable
            # 多个文件
            medias = [
                TypeAdapter(InputMedia).validate_python(
                    {
                        "type": file.type,
                        "media": file.data.pop("file"),
                        **file.get("data", {}),
                    },
                )
                for file in files
            ]

            try:
                media_will_edit = medias[media_group_caption_index]
            except IndexError:
                media_will_edit = medias[0]

            media_will_edit.caption = str(entities) if entities else None
            media_will_edit.caption_entities = Entity.build_telegram_entities(entities)

            return await self.send_media_group(
                chat_id=chat_id,
                message_thread_id=message_thread_id,
                media=medias,  # type: ignore
                reply_parameters=reply_parameters,
                **kwargs,
            )

        # 单个文件
        file = files[0]
        return await self.call_api(
            f"send_{file.type}",
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            **{
                file.type: file.data.get("file"),
                "caption": str(entities) if entities else None,
                "caption_entities": Entity.build_telegram_entities(entities),
            },
            reply_parameters=reply_parameters,
            **kwargs,
        )

    @override
    async def send(
        self,
        event: Event,
        message: Union[str, Message, MessageSegment],
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        **kwargs,
    ) -> Any:
        if not isinstance(event, EventWithChat):
            raise ApiNotAvailable

        kwargs.update(
            {
                "disable_notification": disable_notification,
                "protect_content": protect_content,
            },
        )

        message_thread_id = cast(
            Optional[int],
            getattr(event, "message_thread_id", None),
        )

        return await self.send_to(
            event.chat.id,
            message,
            message_thread_id=message_thread_id,
            **kwargs,
        )
