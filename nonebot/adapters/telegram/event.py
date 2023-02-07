from typing import List, Optional
from typing_extensions import Protocol, runtime_checkable

from pydantic import Field
from nonebot.typing import overrides
from nonebot.utils import escape_tag

from nonebot.adapters import Event as BaseEvent

from .message import Message
from .model import (
    Chat,
    Poll,
    User,
    Update,
    PollAnswer,
    InlineQuery,
    CallbackQuery,
    ShippingQuery,
    ChatJoinRequest,
    PreCheckoutQuery,
    ChatMemberUpdated,
    ChosenInlineResult,
)


@runtime_checkable
class EventWithChat(Protocol):
    chat: Chat


class Event(BaseEvent):
    telegram_model: Update = Field(default=None)

    @classmethod
    def __parse_event(cls, obj: dict) -> "Event":
        post_type: str = list(obj.keys())[1]
        event_map = {
            "message": MessageEvent,
            "edited_message": EditedMessageEvent,
            "channel_post": MessageEvent,
            "edited_channel_post": EditedMessageEvent,
            "inline_query": InlineQueryEvent,
            "chosen_inline_result": ChosenInlineResultEvent,
            "callback_query": CallbackQueryEvent,
            "shipping_query": ShippingQueryEvent,
            "pre_checkout_query": PreCheckoutQueryEvent,
            "poll": PollEvent,
            "poll_answer": PollAnswerEvent,
            "chat_member": ChatMemberUpdatedEvent,
            "my_chat_member": ChatMemberUpdatedEvent,
            "chat_join_request": ChatJoinRequestEvent,
        }

        event = event_map[post_type].parse_event(obj[post_type])
        setattr(event, "telegram_model", Update.parse_obj(obj))
        return event

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
        return escape_tag(
            str(self.dict(by_alias=True, exclude_none=True, exclude={"telegram_model"}))
        )

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
        message = Message.parse_obj(obj)
        if not message:
            return NoticeEvent.parse_event(obj)
        else:
            reply_to_message = obj.pop("reply_to_message", None)
            message_type = obj["chat"]["type"]
            event_map = {
                "private": PrivateMessageEvent,
                "group": GroupMessageEvent,
                "supergroup": GroupMessageEvent,
                "channel": ChannelPostEvent,
            }
            event = event_map[message_type].parse_event(obj)
            setattr(event, "message", message)
            if reply_to_message:
                setattr(event, "reply_to_message", cls.parse_event(reply_to_message))
            return event

    @overrides(Event)
    def get_type(self) -> str:
        return "message"

    @overrides(Event)
    def get_event_name(self) -> str:
        return "message"

    @overrides(Event)
    def get_message(self) -> Message:
        return self.message

    # TODO
    @overrides(Event)
    def is_tome(self) -> bool:
        return super().is_tome()

    @overrides(Event)
    def get_event_description(self) -> str:
        return escape_tag(
            f"Message {self.message_id} @[Chat {self.chat.id}]: {str(self.message)}"
        )


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

    @overrides(Event)
    def get_event_description(self) -> str:
        return escape_tag(
            f"Message {self.message_id} from {self.from_.id}: {str(self.message)}"
        )


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

    @overrides(Event)
    def get_event_description(self) -> str:
        return escape_tag(
            f"Message {self.message_id} from {self.from_.id}@[Chat {self.chat.id}]: {str(self.message)}"
        )


class ForumTopicMessageEvent(GroupMessageEvent):
    message_thread_id: int

    @overrides(MessageEvent)
    def get_event_name(self) -> str:
        return "message.group.forum_topic"

    @overrides(MessageEvent)
    def get_session_id(self) -> str:
        return f"group_{self.chat.id}_thread{self.message_thread_id}_{self.from_.id}"

    @overrides(Event)
    def get_event_description(self) -> str:
        return escape_tag(
            f"Message {self.message_id} from {self.from_.id}@[Chat {self.chat.id} Thread {self.message_thread_id}]: {str(self.message)}"
        )


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
    reply_to_message: Optional["MessageEvent"] = None
    message: Message = Message()

    @classmethod
    def __parse_event(cls, obj: dict):
        reply_to_message = obj.pop("reply_to_message", None)
        message_type = obj["chat"]["type"]
        event_map = {
            "private": PrivateEditedMessageEvent,
            "group": GroupEditedMessageEvent,
            "supergroup": GroupEditedMessageEvent,
            "channel": EditedChannelPostEvent,
        }
        event = event_map[message_type].parse_event(obj)
        setattr(event, "message", Message.parse_obj(obj))
        if reply_to_message:
            setattr(
                event, "reply_to_message", MessageEvent.parse_event(reply_to_message)
            )
        return event

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

    @overrides(Event)
    def get_event_description(self) -> str:
        return escape_tag(
            f"EditedMessage {self.message_id} @[Chat {self.chat.id}]: {str(self.message)}"
        )


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

    @overrides(Event)
    def get_event_description(self) -> str:
        return escape_tag(
            f"EditedMessage {self.message_id} from {self.from_.id}: {str(self.message)}"
        )


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

    @overrides(Event)
    def get_event_description(self) -> str:
        return escape_tag(
            f"EditedMessage {self.message_id} from {self.from_.id}@[Chat {self.chat.id}]: {str(self.message)}"
        )


class ForumTopicEditedMessageEvent(GroupEditedMessageEvent):
    message_thread_id: int

    @overrides(MessageEvent)
    def get_event_name(self) -> str:
        return "edited_message.group.forum_topic"

    @overrides(MessageEvent)
    def get_session_id(self) -> str:
        return f"group_{self.chat.id}_thread{self.message_thread_id}_{self.from_.id}"

    @overrides(Event)
    def get_event_description(self) -> str:
        return escape_tag(
            f"EditedMessage {self.message_id} from {self.from_.id}@[Chat {self.chat.id} Thread {self.message_thread_id}]: {str(self.message)}"
        )


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
    pinned_message: MessageEvent = Field(default=None)

    @classmethod
    def __parse_event(cls, obj: dict):
        pinned_message = obj.pop("pinned_message")
        event = cls.parse_obj(obj)
        setattr(event, "pinned_message", MessageEvent.parse_event(pinned_message))
        return event

    @overrides(NoticeEvent)
    def get_event_name(self) -> str:
        return "notice.pinned_message"

    @overrides(NoticeEvent)
    def get_message(self) -> Message:
        return self.pinned_message.get_message()

    @overrides(Event)
    def get_event_description(self) -> str:
        return escape_tag(
            f"PinnedMessage {self.pinned_message.message_id} @[Chat {self.pinned_message.chat.id}]: {str(self.get_message())}"
        )


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


class ChatMemberUpdatedEvent(NoticeEvent, ChatMemberUpdated):
    @overrides(Event)
    def get_event_name(self) -> str:
        return "notice.chat_member.updated"


class PollEvent(NoticeEvent, Poll):
    @overrides(Event)
    def get_event_name(self) -> str:
        return "notice.poll"


class PollAnswerEvent(NoticeEvent, PollAnswer):
    @overrides(Event)
    def get_event_name(self) -> str:
        return "notice.poll_answer"


class RequestEvent(Event):
    @overrides(Event)
    def get_type(self) -> str:
        return "request"

    @overrides(Event)
    def get_event_name(self) -> str:
        return "request"


class ChatJoinRequestEvent(RequestEvent, ChatJoinRequest):
    @overrides(NoticeEvent)
    def get_event_name(self) -> str:
        return "request.chat_join"


class InlineEvent(Event):
    @overrides(Event)
    def get_type(self) -> str:
        return "inline"

    @overrides(Event)
    def get_event_name(self) -> str:
        return "inline"


class InlineQueryEvent(InlineEvent, InlineQuery):
    @overrides(Event)
    def get_event_name(self) -> str:
        return "inline.query"

    @overrides(Event)
    def get_message(self) -> Message:
        return Message(self.query)

    @overrides(Event)
    def get_plaintext(self) -> str:
        return self.query

    @overrides(Event)
    def is_tome(self) -> bool:
        return True

    @overrides(Event)
    def get_event_description(self) -> str:
        return escape_tag(
            f"InlineQuery {self.id} from {self.from_.id}: {str(self.get_message())}"
        )


class ChosenInlineResultEvent(InlineEvent, ChosenInlineResult):
    @overrides(Event)
    def get_event_name(self) -> str:
        return "inline.chosen_result"

    @overrides(Event)
    def get_event_description(self) -> str:
        return escape_tag(
            f"ChosenInlineResult {self.result_id} from {self.from_.id} for Query {self.query}"
        )


class CallbackQueryEvent(InlineEvent, CallbackQuery):
    @overrides(Event)
    def get_event_name(self) -> str:
        return "inline.callback_query"

    @overrides(Event)
    def get_event_description(self) -> str:
        return escape_tag(f"CallbackQuery {self.id} from {self.from_.id}: {self.data}")


# TODO DELAY
class ShippingQueryEvent(Event, ShippingQuery):
    pass


# TODO DELAY
class PreCheckoutQueryEvent(Event, PreCheckoutQuery):
    pass
