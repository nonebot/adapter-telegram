import inspect
from uuid import uuid4
from functools import partial
from typing import Any, Union, Optional, cast

from pydantic import parse_obj_as
from nonebot.typing import overrides
from nonebot.message import handle_event

from nonebot.adapters import Adapter
from nonebot.adapters import Bot as BaseBot

from .api import API
from .config import BotConfig
from .exception import ApiNotAvailable
from .model import InputMedia, MessageEntity
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

    def __init__(self, adapter: "Adapter", config: BotConfig):
        self.adapter = adapter
        self.self_id = config.token.split(":")[0]
        self.username: Optional[str] = None
        self.bot_config = config
        self.secret_token = uuid4().hex

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
                isinstance(
                    event.reply_to_message,
                    (GroupMessageEvent, PrivateMessageEvent),
                )
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
            return parse_obj_as(
                sign.return_annotation,
                await super().call_api(api, **kargs),
            )
        return await super().call_api(api, **kargs)

    def __getattribute__(self, __name: str) -> Any:
        if not __name.startswith("__") and hasattr(API, __name):
            return partial(self.call_api, __name)
        return object.__getattribute__(self, __name)

    # TODO 重构
    @overrides(BaseBot)
    async def send(
        self,
        event: Event,
        message: Union[str, Message, MessageSegment],
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        media_group_caption_index: int = 0,
        **kwargs,
    ) -> Any:
        """
        由于 Telegram 对于不同类型的消息有不同的 API，如果需要使用同一方法发送不同类型的消息请使用此方法。

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

        if not isinstance(event, EventWithChat):
            raise ApiNotAvailable

        message_thread_id = cast(
            Optional[int],
            getattr(event, "message_thread_id", None),
        )

        # 普通文本
        if isinstance(message, str):
            return await self.send_message(
                chat_id=event.chat.id,
                message_thread_id=message_thread_id,
                text=message,
                **kwargs,
            )

        # 单个 segment
        if isinstance(message, MessageSegment):
            if message.is_text():
                return await self.send_message(
                    chat_id=event.chat.id,
                    message_thread_id=message_thread_id,
                    text=str(message),
                    entities=[
                        MessageEntity(
                            type=message.type,
                            offset=0,
                            length=len(message.data["text"]),
                            url=message.data.get("url"),
                            user=message.data.get("user"),
                            language=message.data.get("language"),
                        ),
                    ]
                    if message.type != "text"
                    else None,
                    **kwargs,
                )

            if isinstance(message, File):
                return await self.call_api(
                    f"send_{message.type}",
                    chat_id=event.chat.id,
                    message_thread_id=message_thread_id,
                    **{message.type: message.data["file"]},
                    **kwargs,
                )

            return await self.call_api(
                f"send_{message.type}",
                chat_id=event.chat.id,
                message_thread_id=message_thread_id,
                **message.data,
                **kwargs,
            )

        # message 处理
        entities = Message(filter(lambda x: isinstance(x, Entity), message))
        files = Message(
            filter(
                lambda x: isinstance(x, File) and not isinstance(message, UnCombinFile),
                message,
            ),
        )
        others = Message(
            filter(
                lambda x: not (isinstance(x, (Entity, File)))
                or isinstance(message, UnCombinFile),
                message,
            ),
        )

        # 处理只能单独发送的特殊消息
        if others and (len(others) > 1 or files or entities):
            raise ApiNotAvailable

        if not files:
            return await self.send_message(
                chat_id=event.chat.id,
                message_thread_id=message_thread_id,
                text=str(message),
                entities=[
                    MessageEntity(
                        type=entity.type,
                        offset=sum(map(len, message[:i])),
                        length=len(entity.data["text"]),
                        url=entity.data.get("url"),
                        user=entity.data.get("user"),
                        language=entity.data.get("language"),
                    )
                    for i, entity in enumerate(message)
                    if entity.is_text() and entity.type != "text"
                ],
                **kwargs,
            )

        # 发送带文件的消息
        if len(files) > 1:
            # 多个文件
            medias = [
                InputMedia(
                    type=file.type,
                    media=file.data["file"],
                )
                for file in files
            ]

            try:
                media_will_edit = medias[media_group_caption_index]
            except IndexError:
                media_will_edit = medias[0]

            media_will_edit.caption = str(entities)
            media_will_edit.caption_entities = [
                MessageEntity(
                    type=entity.type,
                    offset=sum(map(len, message[:i])),
                    length=len(entity.data["text"]),
                    url=entity.data.get("url"),
                    user=entity.data.get("user"),
                    language=entity.data.get("language"),
                )
                for i, entity in enumerate(message)
                if entity.is_text() and entity.type != "text"
            ]

            return await self.send_media_group(
                chat_id=event.chat.id,
                message_thread_id=message_thread_id,
                media=medias,  # type:ignore
                **kwargs,
            )

        # 单个文件
        file = files[0]
        return await self.call_api(
            f"send_{file.type}",
            chat_id=event.chat.id,
            message_thread_id=message_thread_id,
            **{
                file.type: file.data.get("file"),
                "caption": str(entities) if entities else None,
                "caption_entities": [
                    MessageEntity(
                        type=entity.type,
                        offset=sum(map(len, message[:i])),
                        length=len(entity.data["text"]),
                        url=entity.data.get("url"),
                        user=entity.data.get("user"),
                        language=entity.data.get("language"),
                    )
                    for i, entity in enumerate(message)
                    if entity.is_text() and entity.type != "text"
                ]
                if entities
                else None,
            },
            **kwargs,
        )
