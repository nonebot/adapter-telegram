from typing import Any, Optional, cast
from typing_extensions import Protocol, runtime_checkable

from pydantic import Field
from nonebot.log import logger
from nonebot.typing import overrides

from nonebot.adapters import Event as BaseEvent

from .model import *
from .message import Message


@runtime_checkable
class EventWithChat(Protocol):
    chat: Chat


class Event(BaseEvent):
    @classmethod
    def __parse_event(cls, obj: dict) -> "Event":
        logger.debug('"RAW":' + str(obj))
        post_type: str = list(obj.keys())[1]
        event_map = {
            "message": MessageEvent,
            "edited_message": EditedMessageEvent,
            "channel_post": MessageEvent,
            "edited_channel_post": EditedMessageEvent,
            "inline_query": InlineQueryEvent,
            "chosen_inline_result": ChosenInlineResult,
            "callback_query": CallbackQueryEvent,
            "shipping_query": ShippingQueryEvent,
            "pre_checkout_query": PreCheckoutQueryEvent,
            "poll": PollEvent,
            "poll_answer": PollAnswerEvent,
            "chat_member": ChatMemberUpdatedEvent,
            "my_chat_member": ChatMemberUpdatedEvent,
        }
        return event_map[post_type].parse_event(obj[post_type])

    @classmethod
    def _parse_event(cls, obj: dict, failed: set = set()) -> "Event":
        for subclass in cls.__subclasses__():
            if subclass not in failed:
                try:
                    return subclass.parse_event(obj)
                except:
                    pass
        return cls.parse_obj(obj)

    @classmethod
    def parse_event(cls, obj: dict) -> "Event":
        if hasattr(cls, f"_{cls.__name__}__parse_event"):
            return getattr(cls, f"_{cls.__name__}__parse_event")(obj)
        else:
            return cls._parse_event(obj)

    @overrides(BaseEvent)
    def get_type(self) -> str:
        return ""

    @overrides(BaseEvent)
    def get_event_name(self) -> str:
        return ""

    @overrides(BaseEvent)
    def get_event_description(self) -> str:
        return str(self.dict(by_alias=True, exclude_none=True))

    @overrides(BaseEvent)
    def get_user_id(self) -> str:
        raise ValueError("Event has no user!")

    @overrides(BaseEvent)
    def get_session_id(self) -> str:
        raise ValueError("Event has no session!")

    @overrides(BaseEvent)
    def get_message(self) -> Message:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_plaintext(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def is_tome(self) -> bool:
        return False


class MessageEvent(Event):
    message_id: int
    date: int
    chat: Chat
    forward_from: Optional[User]
    forward_from_chat: Optional[Chat]
    forward_from_message_id: Optional[int]
    forward_signature: Optional[str]
    forward_sender_name: Optional[str]
    via_bot: Optional[User]
    media_group_id: Optional[str]
    author_signature: Optional[str]
    reply_to_message: Optional["MessageEvent"] = None
    message: Message = Message()

    @classmethod
    def __parse_event(cls, obj: dict) -> "Event":
        if not Message(obj):
            return NoticeEvent.parse_event(obj)
        else:
            message_type = obj["chat"]["type"]
            event_map = {
                "private": PrivateMessageEvent,
                "group": GroupMessageEvent,
                "supergroup": GroupMessageEvent,
                "channel": ChannelPostEvent,
            }
            return event_map[message_type].parse_event(obj)

    def __init__(self, **data: Any) -> None:
        reply_to_message = data.pop("reply_to_message", None)
        super().__init__(**data)
        self.message = Message(data)
        if reply_to_message:
            self.reply_to_message = cast(
                MessageEvent, self.parse_event(reply_to_message)
            )

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

    # TODO
    @overrides(Event)
    def is_tome(self) -> bool:
        return super().is_tome()


class PrivateMessageEvent(MessageEvent):
    from_: User = Field(alias="from")

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
    from_: User = Field(alias="from")
    sender_chat: Optional[Chat]

    @overrides(MessageEvent)
    def get_event_name(self) -> str:
        return "message.group"

    @overrides(MessageEvent)
    def get_user_id(self) -> str:
        return str(self.from_.id)

    @overrides(MessageEvent)
    def get_session_id(self) -> str:
        return f"group_{self.chat.id}_{self.from_.id}"


class ChannelPostEvent(MessageEvent):
    sender_chat: Optional[Chat]

    @overrides(MessageEvent)
    def get_event_name(self) -> str:
        return "message.channel_post"

    @overrides(MessageEvent)
    def get_session_id(self) -> str:
        return f"channel_{self.chat.id}"


class EditedMessageEvent(Event):
    message_id: int
    date: int
    chat: Chat
    via_bot: Optional[User]
    edit_date: int
    media_group_id: Optional[str]
    author_signature: Optional[str]
    reply_to_message: Optional["MessageEvent"]
    message: Message = Message()

    @classmethod
    def __parse_event(cls, obj: dict):
        message_type = obj["chat"]["type"]
        event_map = {
            "private": PrivateEditedMessageEvent,
            "group": GroupEditedMessageEvent,
            "supergroup": GroupEditedMessageEvent,
            "channel": EditedChannelPostEvent,
        }
        return event_map[message_type].parse_event(obj)

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.message = Message(data)

    @overrides(Event)
    def get_type(self) -> str:
        return "edit_message"

    @overrides(Event)
    def get_event_name(self) -> str:
        return "edit_message"

    @overrides(Event)
    def get_message(self) -> Message:
        return self.message

    @overrides(Event)
    def get_plaintext(self) -> str:
        return self.message.extract_plain_text()

    # TODO
    @overrides(Event)
    def is_tome(self) -> bool:
        return super().is_tome()


class PrivateEditedMessageEvent(EditedMessageEvent):
    from_: User = Field(alias="from")
    sender_chat: Optional[Chat]

    @overrides(EditedMessageEvent)
    def get_event_name(self) -> str:
        return "edited_message.private"

    @overrides(EditedMessageEvent)
    def get_user_id(self) -> str:
        return str(self.from_.id)

    @overrides(EditedMessageEvent)
    def get_session_id(self) -> str:
        return f"private_{self.chat.id}"

    @overrides(EditedMessageEvent)
    def is_tome(self) -> bool:
        return True


class GroupEditedMessageEvent(EditedMessageEvent):
    from_: User = Field(default=None, alias="from")
    sender_chat: Optional[Chat]

    @overrides(EditedMessageEvent)
    def get_event_name(self) -> str:
        return f"edited_message.group"

    @overrides(EditedMessageEvent)
    def get_user_id(self) -> str:
        return str(self.from_.id)

    @overrides(EditedMessageEvent)
    def get_session_id(self) -> str:
        return f"group_{self.chat.id}_{self.from_.id}"


class EditedChannelPostEvent(EditedMessageEvent):
    sender_chat: Optional[Chat]

    @overrides(EditedMessageEvent)
    def get_event_name(self) -> str:
        return "edited_message.channel_post"

    @overrides(EditedMessageEvent)
    def get_session_id(self) -> str:
        return f"channel_{self.chat.id}"


class NoticeEvent(Event):
    @classmethod
    def __parse_event(cls, obj: dict) -> "Event":
        if "pinned_message" in obj:
            return PinnedMessageEvent.parse_event(obj)
        elif "new_chat_member" in obj:
            return NewChatMemberEvent.parse_event(obj)
        elif "left_chat_member" in obj:
            return LeftChatMemberEvent.parse_event(obj)
        else:
            return cls._parse_event(obj)

    @overrides(Event)
    def get_type(self) -> str:
        return "notice"

    @overrides(Event)
    def get_event_name(self) -> str:
        return "notice"


class PinnedMessageEvent(NoticeEvent):
    message_id: int
    from_: User = Field(alias="from")
    sender_chat: Optional[Chat]
    chat: Chat
    date: int
    pinned_message: MessageEvent

    @overrides(NoticeEvent)
    def get_event_name(self) -> str:
        return "notice.pinned_message"

    @overrides(NoticeEvent)
    def get_message(self) -> Message:
        return self.pinned_message.get_message()

    @overrides(NoticeEvent)
    def get_plaintext(self) -> str:
        return self.pinned_message.get_plaintext()


class NewChatMemberEvent(NoticeEvent):
    message_id: int
    from_: Optional[User] = Field(default=None, alias="from")
    chat: Chat
    date: int
    new_chat_participant: Optional[User]
    new_chat_member: User
    new_chat_members: Optional[List[User]]

    @overrides(NoticeEvent)
    def get_event_name(self) -> str:
        return "notice.chat_member.new"


class LeftChatMemberEvent(NoticeEvent):
    message_id: int
    from_: Optional[User] = Field(default=None, alias="from")
    chat: Chat
    date: int
    left_chat_participant: Optional[User]
    left_chat_member: User

    @overrides(Event)
    def get_event_name(self) -> str:
        return "notice.chat_member.left"


class ChatMemberUpdatedEvent(NoticeEvent):
    chat: Chat
    from_: User = Field(alias="from")
    date: int
    old_chat_member: ChatMember
    new_chat_member: ChatMember
    invite_link: Optional[ChatInviteLink]

    @overrides(Event)
    def get_event_name(self) -> str:
        return "notice.chat_member.updated"


# TODO
class InlineQueryEvent(Event):
    id: str
    from_: User = Field(alias="from")
    query: str
    offset: str
    chat_type: Optional[str]
    Location: Optional[Location]


# TODO
class ChosenInlineResultEvent(Event):
    result_id: str
    from_: User = Field(alias="from")
    Location: Optional[Location]
    inline_message_id: Optional[str]
    query: str


# TODO
class CallbackQueryEvent(Event):
    id: str
    from_: Optional[User] = Field(default=None, alias="from")
    message: Optional[Message_]
    inline_message_id: Optional[str]
    chat_instance: Optional[str]
    data: Optional[str]
    game_short_name: Optional[str]


# DELAY
class ShippingQueryEvent(Event):
    id: str
    from_: User = Field(alias="from")
    invoice_payload: str
    shipping_address: ShippingAddress


# DELAY
class PreCheckoutQueryEvent(Event):
    id: str
    from_: User = Field(alias="from")
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: Optional[str]
    order_info: Optional[OrderInfo]


# TODO
class PollEvent(Event):
    id: str
    question: str
    options: List[PollOption]
    total_voter_count: int
    is_closed: bool
    is_anonymous: bool
    type: str
    allows_multiple_answers: bool
    correct_option_id: Optional[int]
    explanation: Optional[str]
    explanation_entities: Optional[List[MessageEntity]]
    open_period: Optional[int]
    close_date: Optional[int]


# TODO
class PollAnswerEvent(Event):
    poll_id: str
    user: User
    option_ids: List[int]
