from typing import Optional

from pydantic import Field

from nonebot.typing import overrides
from nonebot.adapters import Event as BaseEvent
from nonebot.utils import DataclassEncoder

from .model import *
from .message import Message


class Event(BaseEvent):
    class Config:
        extra = "ignore"
        json_encoders = {Message: DataclassEncoder}

    @overrides(BaseEvent)
    def get_event_description(self) -> str:
        return str(self.dict(by_alias=True, exclude_none=True))


class MessageEvent(Event):
    message_id: int
    date: int
    chat: Chat
    message: Optional[Message] = None

    @overrides(Event)
    def get_type(self) -> str:
        return "message"

    @overrides(Event)
    def get_event_name(self) -> str:
        return "message"

    @overrides(Event)
    def get_message(self) -> Message:
        return self.message

    @overrides(Event)
    def get_plaintext(self) -> str:
        return self.message.extract_plain_text()

    @overrides(Event)
    def get_session_id(self) -> str:
        return str(self.chat.id)

    @overrides(Event)
    def is_tome(self) -> bool:
        return False

    @overrides(Event)
    def get_user_id(self) -> str:
        raise NotImplementedError


class PrivateMessageEvent(MessageEvent):
    from_: Optional[User] = Field(default=None, alias="from")
    sender_chat: Optional[Chat]

    @overrides(MessageEvent)
    def get_event_name(self) -> str:
        return "message.private"

    @overrides(MessageEvent)
    def get_user_id(self) -> str:
        return str(self.from_.id)


class GroupMessageEvent(MessageEvent):
    from_: Optional[User] = Field(default=None, alias="from")
    sender_chat: Optional[Chat]

    @overrides(MessageEvent)
    def get_event_name(self) -> str:
        return "message.group"

    @overrides(MessageEvent)
    def get_user_id(self) -> str:
        return str(self.from_.id)


class ChannelPostEvent(MessageEvent):
    sender_chat: Optional[Chat]

    def get_event_name(self) -> str:
        return "message.channel_post"

    @overrides(MessageEvent)
    def get_user_id(self) -> str:
        return str(self.chat.id)


class NoticeEvent(Event):
    @overrides(Event)
    def get_type(self) -> str:
        return "notice"

    @overrides(Event)
    def get_event_name(self) -> str:
        return "notice"

    @overrides(Event)
    def get_message(self) -> Message:
        return self.message

    @overrides(Event)
    def get_plaintext(self) -> str:
        return self.message

    @overrides(Event)
    def get_user_id(self) -> str:
        return str(self.chat.id)

    @overrides(Event)
    def get_session_id(self) -> str:
        return str(self.chat.id)

    @overrides(Event)
    def is_tome(self) -> bool:
        return False


class MessageEditedEvent(NoticeEvent):
    message_id: int
    date: int
    edit_date: int
    chat: Chat
    message: Optional[Message] = None


class PrivateMessageEditedEvent(MessageEditedEvent):
    pass


class GroupMessageEditedEvent(MessageEditedEvent):
    pass


class ChannelPostEditedEvent(MessageEditedEvent):
    pass
