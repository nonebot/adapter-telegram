from typing import Any, Literal, Optional, get_type_hints
from nonebot.typing import overrides
from pydantic import BaseModel, Field
from nonebot.adapters import Event as BaseEvent

from .message import Message
from nonebot_adapter_telegram import message


class User(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    language_code: Optional[str]
    """
    :说明: 用户的语言编码，比如中文用户是 zh-hans

    :类型: ``Optional[str]``
    """
    can_join_groups: Optional[bool]
    """
    :说明: 是否可加入群聊，只会在机器人的 get_me 方法中返回

    :类型: ``Optional[bool]``
    """
    can_read_all_group_messages: Optional[bool]
    """
    :说明: 是否可以读取所有群消息，只会在机器人的 get_me 方法中返回

    :类型: ``Optional[bool]``
    """
    supports_inline_queries: Optional[bool]
    """
    :说明: 是否支持 inline_queries，只会在机器人的 get_me 方法中返回

    :类型: ``Optional[bool]``
    """

    class Config:
        extra = "allow"


class Chat(BaseModel):
    id: int
    type: Literal["private", "group", "supergroup", "channel"]
    title: Optional[str]
    """
    :说明: 聊天标题，只会在聊天类型为 group supergroups channel 时返回

    :类型: ``Optional[str]``
    """
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    photo: Optional[Any]
    bio: Optional[str]
    description: Optional[str]
    invite_link: Optional[str]
    pinned_message: Optional[Any]
    permissions: Optional[Any]
    slow_mode_delay: Optional[int]
    message_auto_delete_time: Optional[int]
    sticker_set_name: Optional[str]
    can_set_sticker_set: Optional[bool]
    linked_chat_id: Optional[int]
    location: Optional[Any]

    class Config:
        extra = "allow"


class Event(BaseEvent):
    @overrides(BaseEvent)
    def get_type(self) -> str:
        return super().get_type()

    @overrides(BaseEvent)
    def get_event_name(self) -> str:
        return "message"
    
    @overrides(BaseEvent)
    def get_event_description(self) -> str:
        return str(self.dict())


class MessageEvent(Event):
    message_id: int
    date: int
    chat: Chat
    from_: Optional[User] = Field(default=None, alias="from")
    sender_chat: Optional[Chat]
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


class PrivateMessageEvent(MessageEvent):
    @overrides(MessageEvent)
    def get_event_name(self) -> str:
        return "message.private"


class GroupMessageEvent(MessageEvent):
    pass


class ChannelPostEvent(MessageEvent):
    pass
