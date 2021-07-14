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

    @overrides(BaseEvent)
    def get_message(self) -> Message:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_plaintext(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_user_id(self) -> str:
        raise ValueError("Event has no user!")

    @overrides(BaseEvent)
    def get_session_id(self) -> str:
        raise ValueError("Event has no session!")

    @overrides(BaseEvent)
    def is_tome(self) -> bool:
        return False


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

class PrivateMessageEvent(MessageEvent):
    from_: Optional[User] = Field(default=None, alias="from")
    sender_chat: Optional[Chat]

    @overrides(MessageEvent)
    def get_event_name(self) -> str:
        return "message.private"

    @overrides(MessageEvent)
    def get_user_id(self) -> str:
        return str(self.from_.id)

    @overrides(MessageEvent)
    def get_session_id(self) -> str:
        return f"private_{self.chat.id}"

    @overrides(MessageEvent)
    def is_tome(self) -> bool:
        return True


class GroupMessageEvent(MessageEvent):
    from_: Optional[User] = Field(default=None, alias="from")
    sender_chat: Optional[Chat]

    @overrides(MessageEvent)
    def get_event_name(self) -> str:
        return "message.group"

    @overrides(MessageEvent)
    def get_user_id(self) -> str:
        return str(self.from_.id)

    @overrides(MessageEvent)
    def get_session_id(self) -> str:
        return f"group_{self.from_.id}"


class ChannelPostEvent(MessageEvent):
    sender_chat: Optional[Chat]

    def get_event_name(self) -> str:
        return "message.channel_post"

    @overrides(MessageEvent)
    def get_session_id(self) -> str:
        return str(self.chat.id)


class NoticeEvent(Event):
    @overrides(Event)
    def get_type(self) -> str:
        return "notice"

    @overrides(Event)
    def get_event_name(self) -> str:
        return "notice"

class EditedMessageEvent(NoticeEvent):
    message_id: int
    date: int
    edit_date: int
    chat: Chat
    message: Optional[Message] = None


class PrivateEditedMessageEvent(EditedMessageEvent):
    from_: Optional[User] = Field(default=None, alias="from")
    sender_chat: Optional[Chat]

    @overrides(EditedMessageEvent)
    def get_event_name(self) -> str:
        return "notice.edited_message.private"

    @overrides(EditedMessageEvent)
    def get_user_id(self) -> str:
        return str(self.from_.id)


class GroupEditedMessageEvent(EditedMessageEvent):
    from_: Optional[User] = Field(default=None, alias="from")
    sender_chat: Optional[Chat]

    @overrides(EditedMessageEvent)
    def get_event_name(self) -> str:
        return "notice.edited_message.group"

    @overrides(EditedMessageEvent)
    def get_user_id(self) -> str:
        return str(self.from_.id)


class EditedChannelPostEvent(EditedMessageEvent):
    sender_chat: Optional[Chat]

    @overrides(EditedMessageEvent)
    def get_event_name(self) -> str:
        return "notice.edited_message.channel_post"

    @overrides(EditedMessageEvent)
    def get_user_id(self) -> str:
        return str(self.from_.id)


class ChatMemberUpdatedEvent(NoticeEvent):
    chat: Chat
    from_: Optional[User] = Field(default=None, alias="from")
    date: int
    old_chat_member: ChatMember
    new_chat_member: ChatMember
    invite_link: Optional[ChatInviteLink]

    @overrides(EditedMessageEvent)
    def get_event_name(self) -> str:
        return "notice.chat_member_updated"

    @overrides(EditedMessageEvent)
    def get_user_id(self) -> str:
        return str(self.from_.id)