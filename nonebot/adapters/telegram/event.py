from typing import List, Literal, Optional
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

    def get_message_description(self) -> str:
        msg_string: List[str] = []
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
    forward_from: Optional[User]
    forward_from_chat: Optional[Chat]
    forward_from_message_id: Optional[int]
    forward_signature: Optional[str]
    forward_sender_name: Optional[str]
    forward_date: Optional[int]
    via_bot: Optional[User]
    has_protected_content: Optional[Literal[True]]
    media_group_id: Optional[str]
    author_signature: Optional[str]
    reply_to_message: Optional["MessageEvent"] = None
    message: Message = Message()
    _tome: bool = False

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

    @overrides(Event)
    def is_tome(self) -> bool:
        return self._tome

    @overrides(Event)
    def get_event_description(self) -> str:
        return f"Message {self.message_id} @[Chat {self.chat.id}]: {self.get_message_description()}"


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
        return f"Message {self.message_id} from {self.from_.id}: {self.get_message_description()}"


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
        return f"Message {self.message_id} from {self.from_.id}@[Chat {self.chat.id}]: {self.get_message_description()}"


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
        return f"Message {self.message_id} from {self.from_.id}@[Chat {self.chat.id} Thread {self.message_thread_id}]: {self.get_message_description()}"


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

    @overrides(Event)
    def get_event_description(self) -> str:
        return f"EditedMessage {self.message_id} @[Chat {self.chat.id}]: {self.get_message_description()}"


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
        return f"EditedMessage {self.message_id} from {self.from_.id}: {self.get_message_description()}"


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
        return f"EditedMessage {self.message_id} from {self.from_.id}@[Chat {self.chat.id}]: {self.get_message_description()}"


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
        return f"EditedMessage {self.message_id} from {self.from_.id}@[Chat {self.chat.id} Thread {self.message_thread_id}]: {self.get_message_description()}"


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
        return f"PinnedMessage {self.pinned_message.message_id} @[Chat {self.pinned_message.chat.id}]: {self.get_message_description()}"


class NewChatMemberEvent(NoticeEvent):
    message_id: int
    from_: Optional[User] = Field(default=None, alias="from")
    chat: Chat
    date: int
    new_chat_members: List[User]

    @overrides(NoticeEvent)
    def get_event_name(self) -> str:
        return "notice.chat_member.new"


class LeftChatMemberEvent(NoticeEvent):
    message_id: int
    from_: Optional[User] = Field(default=None, alias="from")
    chat: Chat
    date: int
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


class NewChatTitleEvent(NoticeEvent):
    date: int
    from_: Optional[User] = Field(default=None, alias="from")
    chat: Chat
    new_chat_title: str

    @overrides(Event)
    def get_event_name(self) -> str:
        return "notice.chat.new_title"


class NewChatPhotoEvent(NoticeEvent):
    date: int
    from_: Optional[User] = Field(default=None, alias="from")
    chat: Chat
    new_chat_photo: List[PhotoSize]

    @overrides(Event)
    def get_event_name(self) -> str:
        return "notice.chat.new_photo"


class DeleteChatPhotoEvent(NoticeEvent):
    date: int
    from_: Optional[User] = Field(default=None, alias="from")
    chat: Chat
    delete_chat_photo: Literal[True]

    @overrides(Event)
    def get_event_name(self) -> str:
        return "notice.chat.delete_photo"


class ForumTopicCreatedEvent(NoticeEvent):
    message_thread_id: int
    from_: Optional[User] = Field(default=None, alias="from")
    chat: Chat
    date: int
    forum_topic_created: ForumTopicCreated

    @overrides(Event)
    def get_event_name(self) -> str:
        return "notice.forum_topic.created"


class ForumTopicEditedEvent(NoticeEvent):
    message_thread_id: int
    from_: Optional[User] = Field(default=None, alias="from")
    chat: Chat
    date: int
    forum_topic_edited: ForumTopicEdited

    @overrides(Event)
    def get_event_name(self) -> str:
        return "notice.forum_topic.edited"


class ForumTopicClosedEvent(NoticeEvent):
    message_thread_id: int
    from_: Optional[User] = Field(default=None, alias="from")
    chat: Chat
    date: int
    forum_topic_closed: ForumTopicClosed

    @overrides(Event)
    def get_event_name(self) -> str:
        return "notice.forum_topic.closed"


class ForumTopicReopenedEvent(NoticeEvent):
    message_thread_id: int
    from_: Optional[User] = Field(default=None, alias="from")
    chat: Chat
    date: int
    forum_topic_reopened: ForumTopicReopened

    @overrides(Event)
    def get_event_name(self) -> str:
        return "notice.forum_topic.reopened"


class GeneralForumTopicHiddenEvent(NoticeEvent):
    from_: Optional[User] = Field(default=None, alias="from")
    chat: Chat
    date: int
    general_forum_topic_hidden: GeneralForumTopicHidden

    @overrides(Event)
    def get_event_name(self) -> str:
        return "notice.general_forum_topic.hidden"


class GeneralForumTopicUnhiddenEvent(NoticeEvent):
    from_: Optional[User] = Field(default=None, alias="from")
    chat: Chat
    date: int
    general_forum_topic_unhidden: GeneralForumTopicUnhidden

    @overrides(Event)
    def get_event_name(self) -> str:
        return "notice.general_forum_topic.unhidden"


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
        return f"InlineQuery {self.id} from {self.from_.id}: {self.get_message_description()}"


class ChosenInlineResultEvent(InlineEvent, ChosenInlineResult):
    @overrides(Event)
    def get_event_name(self) -> str:
        return "inline.chosen_result"

    @overrides(Event)
    def get_event_description(self) -> str:
        return f"ChosenInlineResult {self.result_id} from {self.from_.id} for Query {self.query}"


class CallbackQueryEvent(InlineEvent, CallbackQuery):
    @overrides(Event)
    def get_event_name(self) -> str:
        return "inline.callback_query"

    @overrides(Event)
    def get_event_description(self) -> str:
        return f"CallbackQuery {self.id} from {self.from_.id}: {self.data}"


# TODO DELAY
class ShippingQueryEvent(Event, ShippingQuery):
    pass


# TODO DELAY
class PreCheckoutQueryEvent(Event, PreCheckoutQuery):
    pass
