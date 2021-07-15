from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field
from pydantic.types import OptionalInt


class Update(BaseModel):
    update_id: int
    message: Optional["Message"]
    edited_message: Optional["Message"]
    channel_post: Optional["Message"]
    edited_channel_post: Optional["Message"]
    inline_query: Optional["InlineQuery"]
    chosen_inline_result: Optional["ChosenInlineResult"]
    callback_query: Optional["CallbackQuery"]
    shipping_query: Optional["ShippingQuery"]
    pre_checkout_query: Optional["PreCheckoutQuery"]
    poll: Optional["Poll"]
    poll_answer: Optional["PollAnswer"]
    my_chat_member: Optional["ChatMemberUpdated"]
    chat_member: Optional["ChatMemberUpdated"]


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
    photo: Optional["ChatPhoto"]
    """
    :说明: 聊天图片，仅在使用 get_chat 方法时返回

    :类型: ``Optional[ChatPhoto]``
    """
    bio: Optional[str]
    """
    :说明: 聊天 ?，仅在使用 get_chat 方法时返回

    :类型: ``Optional[str]``
    """
    description: Optional[str]
    """
    :说明: 聊天简介，仅在使用 get_chat 方法时返回

    :类型: ``Optional[str]``
    """
    invite_link: Optional[str]
    """
    :说明: 邀请链接，仅在使用 get_chat 方法时返回

    :类型: ``Optional[str]``
    """
    pinned_message: Optional["Message"]
    """
    :说明: 置顶消息，仅在使用 get_chat 方法时返回

    :类型: ``Optional[Message]``
    """
    permissions: Optional["ChatPermissions"]
    """
    :说明: 成员权限，仅在使用 get_chat 方法时返回

    :类型: ``Optional[ChatPermissions]``
    """
    slow_mode_delay: Optional[int]
    """
    :说明: 消息频率限制，仅在使用 get_chat 方法时返回

    :类型: ``Optional[int]``
    """
    message_auto_delete_time: Optional[int]
    """
    :说明: 消息自动撤回时间，仅在使用 get_chat 方法时返回

    :类型: ``Optional[int]``
    """
    sticker_set_name: Optional[str]
    """
    :说明: 聊天表情包，仅在使用 get_chat 方法时返回

    :类型: ``Optional[string]``
    """
    can_set_sticker_set: Optional[bool]
    """
    :说明: 机器人是否可设置聊天表情包，仅在使用 get_chat 方法时返回

    :类型: ``Optional[bool]``
    """
    linked_chat_id: Optional[int]
    """
    :说明: 链接到的聊天的 id，仅在使用 get_chat 方法时返回

    :类型: ``Optional[int]``
    """
    location: Optional["ChatLocation"]
    """
    :说明: 聊天地址，仅在使用 get_chat 方法时返回

    :类型: ``Optional[ChatLocation]``
    """


class Message(BaseModel):
    message_id: int
    from_: Optional[User] = Field(default=None, alias="from")
    sender_chat: Optional[Chat]
    date: int
    chat: "Chat"
    forward_from: Optional[User]
    forward_from_chat: Optional[Chat]
    forward_from_message_id: Optional[int]
    forward_signature: Optional[str]
    forward_sender_name: Optional[str]
    forward_date: Optional[int]
    reply_to_message: Optional["Message"]
    via_bot: Optional[User]
    edit_date: Optional[int]
    media_group_id: Optional[str]
    author_signature: Optional[str]
    text: Optional[str]
    entities: Optional[List["MessageEntity"]]
    animation: Optional["Animation"]
    audio: Optional["Audio"]
    document: Optional["Document"]
    photo: Optional[List["PhotoSize"]]
    sticker: Optional["Sticker"]
    video: Optional["Video"]
    video_note: Optional["VideoNote"]
    voice: Optional["Voice"]
    caption: Optional[str]
    caption_entities: Optional[List["MessageEntity"]]
    contact: Optional["Contact"]
    dice: Optional["Dice"]
    game: Optional["Game"]
    poll: Optional["Poll"]
    venue: Optional["Venue"]
    location: Optional["Location"]
    new_chat_members: Optional[List[User]]
    left_chat_member: Optional[User]
    new_chat_title: Optional[str]
    new_chat_photo: Optional[List["PhotoSize"]]
    delete_chat_photo: Optional[True]
    group_chat_created: Optional[True]
    supergroup_chat_created: Optional[True]
    channel_chat_created: Optional[True]
    message_auto_delete_timer_changed: Optional["MessageAutoDeleteTimerChanged"]
    migrate_to_chat_id: Optional[int]
    migrate_from_chat_id: Optional[int]
    pinned_message: Optional["Message"]
    invoice: Optional["Invoice"]
    successful_payment: Optional["SuccessfulPayment"]
    connected_website: Optional[str]
    passport_data: Optional["PassportData"]
    proximity_alert_triggered: Optional["ProximityAlertTriggered"]
    voice_chat_scheduled: Optional["VoiceChatScheduled"]
    voice_chat_started: Optional["VoiceChatStarted"]
    voice_chat_ended: Optional["VoiceChatEnded"]
    voice_chat_participants_invited: Optional["VoiceChatParticipantsInvited"]
    reply_markup: Optional["InlineKeyboardMarkup"]


class MessageId(BaseModel):
    message_id: int


class MessageEntity(BaseModel):
    type: str
    offset: int
    length: int
    url: Optional[str]
    user: Optional[User]
    language: Optional[str]


class PhotoSize(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: Optional[int]


class Animation(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumb: Optional[PhotoSize]
    file_name: Optional[str]
    mime_type: Optional[str]
    file_size: Optional[int]


class Audio(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    performer: Optional[str]
    title: Optional[str]
    file_name: Optional[str]
    mime_type: Optional[str]
    file_size: Optional[int]
    thumb: Optional[PhotoSize]


class Document(BaseModel):
    file_id: str
    file_unique_id: str
    thumb: Optional[PhotoSize]
    file_name: Optional[str]
    mime_type: Optional[str]
    file_size: Optional[int]


class Video(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumb: Optional[PhotoSize]
    file_name: Optional[str]
    mime_type: Optional[str]
    file_size: Optional[int]


class VideoNote(BaseModel):
    file_id: str
    file_unique_id: str
    length: int
    duration: int
    thumb: Optional[PhotoSize]
    file_size: Optional[int]


class Voice(BaseModel):
    file_id: str
    file_unique_id: str
    duration: int
    mime_type: Optional[str]
    file_size: Optional[int]


class Contact(BaseModel):
    phone_number: str
    first_name: str
    last_name: Optional[str]
    user_id: Optional[int]
    vcard: Optional[str]


class Dice(BaseModel):
    emoji: str
    value: int


class PollOption(BaseModel):
    text: str
    voter_count: int


class PollAnswer(BaseModel):
    poll_id: str
    user: User
    option_ids: List[int]


class Poll(BaseModel):
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


class Location(BaseModel):
    longitude: float
    latitude: float
    horizontal_accuracy: Optional[float]
    live_period: Optional[int]
    heading: Optional[int]
    prpximity_alert_radius: Optional[int]


class Venue(BaseModel):
    location: Location
    titile: str
    address: str
    foursquare_id: Optional[str]
    foursquare_type: Optional[str]
    google_place_id: Optional[str]
    google_place_type: Optional[str]


class ProximityAlertTriggered(BaseModel):
    traveler: User
    watcher: User
    distance: int


class MessageAutoDeleteTimerChanged(BaseModel):
    message_auto_delete_time: int


class VoiceChatScheduled(BaseModel):
    start_date: int


class VoiceChatStarted(BaseModel):
    pass


class VoiceChatEnded(BaseModel):
    duration: int


class VoiceChatParticipantsInvited(BaseModel):
    users: Optional[List[User]]


class UserProfilePhotos(BaseModel):
    total_count: int
    photos: List[List[PhotoSize]]


class File(BaseModel):
    file_id: str
    file_unique_id: str
    file_size: Optional[int]
    file_path: Optional[str]


class ReplyKeyboardMarkup(BaseModel):
    keyboard: List[List["KeyboardButton"]]
    resize_keyboard: Optional[bool]
    one_time_keyboard: Optional[bool]
    input_field_placeholder: Optional[str]
    selective: Optional[bool]


class KeyboardButton(BaseModel):
    text: str
    request_contact: Optional[bool]
    request_location: Optional[bool]
    request_poll: Optional["KeyboardButtonPollType"]


class KeyboardButtonPollType(BaseModel):
    type: Optional[str]


class ReplyKeyboardRemove(BaseModel):
    remove_keyboard: True
    selective: Optional[bool]


class InlineKeyboardMarkup(BaseModel):
    inline_keyboard: List[List["InlineKeyboardButton"]]


class InlineKeyboardButton(BaseModel):
    text: str
    url: Optional[str]
    login_url: Optional["LoginUrl"]
    callback_date: Optional[str]
    switch_inline_query: Optional[str]
    switch_inline_query_current_chat: Optional[str]
    callback_game: Optional["CallbackGame"]
    pay: Optional[bool]


class LoginUrl(BaseModel):
    url: str
    forward_text: Optional[str]
    bot_username: Optional[str]
    request_write_access: Optional[bool]


class CallbackQuery(BaseModel):
    id: str
    from_: Optional[User] = Field(default=None, alias="from")
    message: Optional[Message]
    inline_message_id: Optional[str]
    chat_instance: Optional[str]
    date: Optional[str]
    game_short_name: Optional[str]


class ForceReply(BaseModel):
    force_reply: True
    input_field_placeholder: Optional[str]
    selective: Optional[bool]


class ChatPhoto(BaseModel):
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str


class ChatInviteLink(BaseModel):
    invite_link: str
    creator: User
    is_primary: bool
    is_revoked: bool
    expire_date: Optional[int]
    member_limit: Optional[int]


class ChatMember(BaseModel):
    status: str
    user: User


class ChatMemberOwner(ChatMember):
    status: str = "creator"
    is_anonymous: bool
    custom_title: str


class ChatMemberAdministrator(ChatMember):
    status: str = "administrator"
    can_be_edited: bool
    is_anonymous: bool
    can_manage_chat: bool
    can_delete_messages: bool
    can_manage_voice_chats: bool
    can_restrict_members: bool
    can_promote_members: bool
    can_change_info: bool
    can_invite_users: bool
    can_post_messages: Optional[bool]
    can_edit_messages: Optional[bool]
    can_pin_messages: Optional[bool]
    custom_title: Optional[str]


class ChatMemberMember(ChatMember):
    status: str = "member"


class ChatMemberRestricted(ChatMember):
    status: str = "restricted"
    is_member: bool
    can_change_info: bool
    can_invite_users: bool
    can_pin_messages: bool
    can_send_messages: bool
    can_send_media_messages: bool
    can_send_polls: bool
    can_send_other_messages: bool
    can_add_web_page_previews: bool
    until_date: int


class ChatMemberLeft(ChatMember):
    status: str = "left"


class ChatMemberBanned(ChatMember):
    status: str = "kicked"
    status: int


class ChatPermissions(BaseModel):
    can_send_messages: Optional[bool]
    can_send_media_messages: Optional[bool]
    can_send_polls: Optional[bool]
    can_send_other_messages: Optional[bool]
    can_add_web_page_previews: Optional[bool]
    can_change_info: Optional[bool]
    can_invite_users: Optional[bool]
    can_pin_messages: Optional[bool]


class ChatLocation(BaseModel):
    location: Location
    address: str


class BotCommand(BaseModel):
    command: str
    description: str


class BotCommandScopeDefault(BaseModel):
    type: str = "default"


class BotCommandScopeAllPrivateChats(BaseModel):
    type: str = "all_private_chats"


class BotCommandScopeAllGroupChats(BaseModel):
    type: str = "all_group_chats"


class BotCommandScopeAllChatAdministrators(BaseModel):
    type: str = "all_chat_administrators"


class BotCommandScopeChat(BaseModel):
    type: str = "chat"
    chat_id: Union[int, str]


class BotCommandScopeChatAdministrators(BaseModel):
    type: str = "chat_administrators"
    chat_id: Union[int, str]


class BotCommandScopeChatMember(BaseModel):
    type: str = "chat_member"
    chat_id: Union[int, str]
    user_id: int


class ResponseParameters(BaseModel):
    migrate_to_chat_id: Optional[int]
    retry_after: Optional[int]


class InputMediaPhoto(BaseModel):
    type: str = "photo"
    media: str
    caption: Optional[str]
    parse_mode: Optional[str]
    caption_entities: Optional[List[MessageEntity]]


class InputMediaVideo(BaseModel):
    type: str = "video"
    media: str
    thumb: Optional[Union["InputFile", str]]
    caption: Optional[str]
    parse_mode: Optional[str]
    caption_entities: Optional[List[MessageEntity]]
    width: Optional[int]
    height: Optional[int]
    duration: Optional[int]
    supports_streaming: Optional[bool]


class InputMediaAnimation(BaseModel):
    type: str = "animation"
    media: str
    thumb: Optional[Union["InputFile", str]]
    caption: Optional[str]
    parse_mode: Optional[str]
    caption_entities: Optional[List[MessageEntity]]
    width: Optional[int]
    height: Optional[int]
    duration: Optional[int]


class InputMediaAudio(BaseModel):
    type: str = "audio"
    media: str
    thumb: Optional[Union["InputFile", str]]
    caption: Optional[str]
    parse_mode: Optional[str]
    caption_entities: Optional[List[MessageEntity]]
    duration: Optional[int]
    performer: Optional[str]
    title: Optional[str]


class InputMediaDocument(BaseModel):
    type: str = "document"
    media: str
    thumb: Optional[Union["InputFile", str]]
    caption: Optional[str]
    parse_mode: Optional[str]
    caption_entities: Optional[List[MessageEntity]]
    disable_content_type_detection: Optional[bool]


class InputFile(BaseModel):
    pass
