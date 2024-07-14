from copy import deepcopy
from typing import Literal, Optional
from typing_extensions import Protocol, override, runtime_checkable

from pydantic import Field
from nonebot.utils import escape_tag

from nonebot.adapters import Event as BaseEvent

from .message import Message
from .model import (
    Chat,
    Poll,
    User,
    Update,
    PhotoSize,
    PollAnswer,
    InlineQuery,
    CallbackQuery,
    ShippingQuery,
    ChatJoinRequest,
    ForumTopicClosed,
    ForumTopicEdited,
    PreCheckoutQuery,
    ChatMemberUpdated,
    ForumTopicCreated,
    ChosenInlineResult,
    ForumTopicReopened,
    GeneralForumTopicHidden,
    GeneralForumTopicUnhidden,
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
        setattr(event, "telegram_model", Update.model_validate(obj))
        return event

    @classmethod
    def _parse_event(cls, obj: dict, failed: set = set()) -> "Event":
        for subclass in cls.__subclasses__():
            if subclass not in failed:
                try:
                    return subclass.parse_event(obj)
                except:
                    pass
        return cls.model_validate(obj)

    @classmethod
    def parse_event(cls, obj: dict) -> "Event":
        if hasattr(cls, f"_{cls.__name__}__parse_event"):
            return getattr(cls, f"_{cls.__name__}__parse_event")(obj)
        else:
            return cls._parse_event(obj)

    @override
    def get_type(self) -> str:
        return ""

    @override
    def get_event_name(self) -> str:
        return ""

    @override
    def get_event_description(self) -> str:
        return escape_tag(
            str(
                self.model_dump(
                    by_alias=True, exclude_none=True, exclude={"telegram_model"}
                )
            )
        )

    @override
    def get_user_id(self) -> str:
        raise ValueError("Event has no user!")

    @override
    def get_session_id(self) -> str:
        raise ValueError("Event has no session!")

    @override
    def get_message(self) -> Message:
        raise ValueError("Event has no message!")

    @override
    def is_tome(self) -> bool:
        return False

    def get_message_description(self) -> str:
        msg_string: list[str] = []
        for seg in self.get_message():
            text = escape_tag(repr(seg))
            if seg.type == "text":
                msg_string.append(text)
            else:
                msg_string.append(f"<le>{text}</le>")
        return "".join(msg_string)


class MessageEvent(Event):
    message_id: int
    date: int
    chat: Chat
    forward_from: Optional[User] = None
    forward_from_chat: Optional[Chat] = None
    forward_from_message_id: Optional[int] = None
    forward_signature: Optional[str] = None
    forward_sender_name: Optional[str] = None
    forward_date: Optional[int] = None
    via_bot: Optional[User] = None
    has_protected_content: Optional[Literal[True]] = None
    media_group_id: Optional[str] = None
    author_signature: Optional[str] = None
    reply_to_message: Optional["MessageEvent"] = None
    message: Message = Message()
    original_message: Message = Message()
    _tome: bool = False

    @classmethod
    def __parse_event(cls, obj: dict) -> "Event":
        message = Message.model_validate(obj)
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
            setattr(event, "original_message", deepcopy(message))
            if reply_to_message:
                setattr(event, "reply_to_message", cls.parse_event(reply_to_message))
            return event

    @override
    def get_type(self) -> str:
        return "message"

    @override
    def get_event_name(self) -> str:
        return "message"

    @override
    def get_message(self) -> Message:
        return self.message

    @override
    def is_tome(self) -> bool:
        return self._tome

    @override
    def get_event_description(self) -> str:
        return f"Message {self.message_id} @[Chat {self.chat.id}]: {self.get_message_description()}"


class PrivateMessageEvent(MessageEvent):
    from_: User = Field(alias="from")

    @override
    def get_event_name(self) -> str:
        return "message.private"

    @override
    def get_user_id(self) -> str:
        return str(self.from_.id)

    @override
    def get_session_id(self) -> str:
        return f"private_{self.chat.id}"

    @override
    def is_tome(self) -> bool:
        return True

    @override
    def get_event_description(self) -> str:
        return f"Message {self.message_id} from {self.from_.id}: {self.get_message_description()}"


class GroupMessageEvent(MessageEvent):
    @classmethod
    def __parse_event(cls, obj: dict) -> "Event":
        if obj.pop("is_topic_message", None):
            event = ForumTopicMessageEvent.parse_event(obj)
        else:
            obj.pop("message_thread_id", None)
            event = cls.model_validate(obj)
        return event

    from_: User = Field(alias="from")
    sender_chat: Optional[Chat] = None

    @override
    def get_event_name(self) -> str:
        return "message.group"

    @override
    def get_user_id(self) -> str:
        return str(self.from_.id)

    @override
    def get_session_id(self) -> str:
        return f"group_{self.chat.id}_{self.from_.id}"

    @override
    def get_event_description(self) -> str:
        return f"Message {self.message_id} from {self.from_.id}@[Chat {self.chat.id}]: {self.get_message_description()}"


class ForumTopicMessageEvent(GroupMessageEvent):
    message_thread_id: int

    @override
    def get_event_name(self) -> str:
        return "message.group.forum_topic"

    @override
    def get_session_id(self) -> str:
        return f"group_{self.chat.id}_thread{self.message_thread_id}_{self.from_.id}"

    @override
    def get_event_description(self) -> str:
        return f"Message {self.message_id} from {self.from_.id}@[Chat {self.chat.id} Thread {self.message_thread_id}]: {self.get_message_description()}"


class ChannelPostEvent(MessageEvent):
    sender_chat: Optional[Chat] = None

    @override
    def get_event_name(self) -> str:
        return "message.channel_post"

    @override
    def get_session_id(self) -> str:
        return f"channel_{self.chat.id}"


class EditedMessageEvent(Event):
    message_id: int
    date: int
    chat: Chat
    via_bot: Optional[User] = None
    edit_date: int
    media_group_id: Optional[str] = None
    author_signature: Optional[str] = None
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
        setattr(event, "message", Message.model_validate(obj))
        if reply_to_message:
            setattr(
                event, "reply_to_message", MessageEvent.parse_event(reply_to_message)
            )
        return event

    @override
    def get_type(self) -> str:
        return "edit_message"

    @override
    def get_event_name(self) -> str:
        return "edit_message"

    @override
    def get_message(self) -> Message:
        return self.message

    @override
    def get_plaintext(self) -> str:
        return self.message.extract_plain_text()

    @override
    def get_event_description(self) -> str:
        return f"EditedMessage {self.message_id} @[Chat {self.chat.id}]: {self.get_message_description()}"


class PrivateEditedMessageEvent(EditedMessageEvent):
    from_: User = Field(alias="from")
    sender_chat: Optional[Chat] = None

    @override
    def get_event_name(self) -> str:
        return "edited_message.private"

    @override
    def get_user_id(self) -> str:
        return str(self.from_.id)

    @override
    def get_session_id(self) -> str:
        return f"private_{self.chat.id}"

    @override
    def is_tome(self) -> bool:
        return True

    @override
    def get_event_description(self) -> str:
        return f"EditedMessage {self.message_id} from {self.from_.id}: {self.get_message_description()}"


class GroupEditedMessageEvent(EditedMessageEvent):
    from_: User = Field(default=None, alias="from")
    sender_chat: Optional[Chat] = None

    @classmethod
    def __parse_event(cls, obj: dict) -> "Event":
        if obj.pop("is_topic_message", None):
            event = ForumTopicEditedMessageEvent.parse_event(obj)
        else:
            obj.pop("message_thread_id", None)
            event = cls.model_validate(obj)
        return event

    @override
    def get_event_name(self) -> str:
        return "edited_message.group"

    @override
    def get_user_id(self) -> str:
        return str(self.from_.id)

    @override
    def get_session_id(self) -> str:
        return f"group_{self.chat.id}_{self.from_.id}"

    @override
    def get_event_description(self) -> str:
        return f"EditedMessage {self.message_id} from {self.from_.id}@[Chat {self.chat.id}]: {self.get_message_description()}"


class ForumTopicEditedMessageEvent(GroupEditedMessageEvent):
    message_thread_id: int

    @override
    def get_event_name(self) -> str:
        return "edited_message.group.forum_topic"

    @override
    def get_session_id(self) -> str:
        return f"group_{self.chat.id}_thread{self.message_thread_id}_{self.from_.id}"

    @override
    def get_event_description(self) -> str:
        return f"EditedMessage {self.message_id} from {self.from_.id}@[Chat {self.chat.id} Thread {self.message_thread_id}]: {self.get_message_description()}"


class EditedChannelPostEvent(EditedMessageEvent):
    sender_chat: Optional[Chat] = None

    @override
    def get_event_name(self) -> str:
        return "edited_message.channel_post"

    @override
    def get_session_id(self) -> str:
        return f"channel_{self.chat.id}"


class NoticeEvent(Event):
    @classmethod
    def __parse_event(cls, obj: dict) -> "Event":
        if "pinned_message" in obj:
            return PinnedMessageEvent.parse_event(obj)
        elif "new_chat_members" in obj:
            return NewChatMemberEvent.parse_event(obj)
        elif "left_chat_member" in obj:
            return LeftChatMemberEvent.parse_event(obj)
        elif "new_chat_title" in obj:
            return NewChatTitleEvent.parse_event(obj)
        elif "new_chat_photo" in obj:
            return NewChatPhotoEvent.parse_event(obj)
        elif "delete_chat_photo" in obj:
            return DeleteChatPhotoEvent.parse_event(obj)
        elif "forum_topic_created" in obj:
            return ForumTopicCreatedEvent.parse_event(obj)
        elif "forum_topic_edited" in obj:
            return ForumTopicEditedEvent.parse_event(obj)
        elif "forum_topic_closed" in obj:
            return ForumTopicClosedEvent.parse_event(obj)
        elif "forum_topic_reopened" in obj:
            return ForumTopicReopenedEvent.parse_event(obj)
        elif "general_forum_topic_hidden" in obj:
            return GeneralForumTopicHiddenEvent.parse_event(obj)
        elif "general_forum_topic_unhidden" in obj:
            return GeneralForumTopicUnhiddenEvent.parse_event(obj)
        else:
            return cls._parse_event(obj)

    @override
    def get_type(self) -> str:
        return "notice"

    @override
    def get_event_name(self) -> str:
        return "notice"


class PinnedMessageEvent(NoticeEvent):
    message_id: int
    from_: Optional[User] = Field(alias="from")
    sender_chat: Optional[Chat] = None
    chat: Chat
    date: int
    pinned_message: MessageEvent = Field(default=None)

    @classmethod
    def __parse_event(cls, obj: dict):
        pinned_message = obj.pop("pinned_message")
        event = cls.model_validate(obj)
        setattr(event, "pinned_message", MessageEvent.parse_event(pinned_message))
        return event

    @override
    def get_event_name(self) -> str:
        return "notice.pinned_message"

    @override
    def get_message(self) -> Message:
        return self.pinned_message.get_message()

    @override
    def get_event_description(self) -> str:
        return f"PinnedMessage {self.pinned_message.message_id} @[Chat {self.pinned_message.chat.id}]: {self.get_message_description()}"


class NewChatMemberEvent(NoticeEvent):
    message_id: int
    from_: Optional[User] = Field(default=None, alias="from")
    chat: Chat
    date: int
    new_chat_members: list[User]

    @override
    def get_event_name(self) -> str:
        return "notice.chat_member.new"


class LeftChatMemberEvent(NoticeEvent):
    message_id: int
    from_: Optional[User] = Field(default=None, alias="from")
    chat: Chat
    date: int
    left_chat_member: User

    @override
    def get_event_name(self) -> str:
        return "notice.chat_member.left"


class ChatMemberUpdatedEvent(NoticeEvent, ChatMemberUpdated):
    @override
    def get_event_name(self) -> str:
        return "notice.chat_member.updated"


class PollEvent(NoticeEvent, Poll):
    @override
    def get_event_name(self) -> str:
        return "notice.poll"


class PollAnswerEvent(NoticeEvent, PollAnswer):
    @override
    def get_event_name(self) -> str:
        return "notice.poll_answer"


class NewChatTitleEvent(NoticeEvent):
    date: int
    from_: Optional[User] = Field(default=None, alias="from")
    chat: Chat
    new_chat_title: str

    @override
    def get_event_name(self) -> str:
        return "notice.chat.new_title"


class NewChatPhotoEvent(NoticeEvent):
    date: int
    from_: Optional[User] = Field(default=None, alias="from")
    chat: Chat
    new_chat_photo: list[PhotoSize]

    @override
    def get_event_name(self) -> str:
        return "notice.chat.new_photo"


class DeleteChatPhotoEvent(NoticeEvent):
    date: int
    from_: Optional[User] = Field(default=None, alias="from")
    chat: Chat
    delete_chat_photo: Literal[True]

    @override
    def get_event_name(self) -> str:
        return "notice.chat.delete_photo"


class ForumTopicCreatedEvent(NoticeEvent):
    message_thread_id: int
    from_: Optional[User] = Field(default=None, alias="from")
    chat: Chat
    date: int
    forum_topic_created: ForumTopicCreated

    @override
    def get_event_name(self) -> str:
        return "notice.forum_topic.created"


class ForumTopicEditedEvent(NoticeEvent):
    message_thread_id: int
    from_: Optional[User] = Field(default=None, alias="from")
    chat: Chat
    date: int
    forum_topic_edited: ForumTopicEdited

    @override
    def get_event_name(self) -> str:
        return "notice.forum_topic.edited"


class ForumTopicClosedEvent(NoticeEvent):
    message_thread_id: int
    from_: Optional[User] = Field(default=None, alias="from")
    chat: Chat
    date: int
    forum_topic_closed: ForumTopicClosed

    @override
    def get_event_name(self) -> str:
        return "notice.forum_topic.closed"


class ForumTopicReopenedEvent(NoticeEvent):
    message_thread_id: int
    from_: Optional[User] = Field(default=None, alias="from")
    chat: Chat
    date: int
    forum_topic_reopened: ForumTopicReopened

    @override
    def get_event_name(self) -> str:
        return "notice.forum_topic.reopened"


class GeneralForumTopicHiddenEvent(NoticeEvent):
    from_: Optional[User] = Field(default=None, alias="from")
    chat: Chat
    date: int
    general_forum_topic_hidden: GeneralForumTopicHidden

    @override
    def get_event_name(self) -> str:
        return "notice.general_forum_topic.hidden"


class GeneralForumTopicUnhiddenEvent(NoticeEvent):
    from_: Optional[User] = Field(default=None, alias="from")
    chat: Chat
    date: int
    general_forum_topic_unhidden: GeneralForumTopicUnhidden

    @override
    def get_event_name(self) -> str:
        return "notice.general_forum_topic.unhidden"


class RequestEvent(Event):
    @override
    def get_type(self) -> str:
        return "request"

    @override
    def get_event_name(self) -> str:
        return "request"


class ChatJoinRequestEvent(RequestEvent, ChatJoinRequest):
    @override
    def get_event_name(self) -> str:
        return "request.chat_join"


class InlineEvent(Event):
    @override
    def get_type(self) -> str:
        return "inline"

    @override
    def get_event_name(self) -> str:
        return "inline"


class InlineQueryEvent(InlineEvent, InlineQuery):
    @override
    def get_event_name(self) -> str:
        return "inline.query"

    @override
    def get_message(self) -> Message:
        return Message(self.query)

    @override
    def get_plaintext(self) -> str:
        return self.query

    @override
    def is_tome(self) -> bool:
        return True

    @override
    def get_event_description(self) -> str:
        return f"InlineQuery {self.id} from {self.from_.id}: {self.get_message_description()}"


class ChosenInlineResultEvent(InlineEvent, ChosenInlineResult):
    @override
    def get_event_name(self) -> str:
        return "inline.chosen_result"

    @override
    def get_event_description(self) -> str:
        return f"ChosenInlineResult {self.result_id} from {self.from_.id} for Query {self.query}"


class CallbackQueryEvent(InlineEvent, CallbackQuery):
    chat: Chat = Field(default=None)

    @override
    def get_event_name(self) -> str:
        return "inline.callback_query"

    @override
    def get_event_description(self) -> str:
        return f"CallbackQuery {self.id} from {self.from_.id}: {self.data}"


# TODO DELAY
class ShippingQueryEvent(Event, ShippingQuery):
    pass


# TODO DELAY
class PreCheckoutQueryEvent(Event, PreCheckoutQuery):
    pass
