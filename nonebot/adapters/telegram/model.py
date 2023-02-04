from typing import List, Union, Literal, Optional

from pydantic import Field, BaseModel


class Update(BaseModel):
    update_id: int
    message: Optional["Message"] = None
    edited_message: Optional["Message"] = None
    channel_post: Optional["Message"] = None
    edited_channel_post: Optional["Message"] = None
    inline_query: Optional["InlineQuery"] = None
    chosen_inline_result: Optional["ChosenInlineResult"] = None
    callback_query: Optional["CallbackQuery"] = None
    shipping_query: Optional["ShippingQuery"] = None
    pre_checkout_query: Optional["PreCheckoutQuery"] = None
    poll: Optional["Poll"] = None
    poll_answer: Optional["PollAnswer"] = None
    my_chat_member: Optional["ChatMemberUpdated"] = None
    chat_member: Optional["ChatMemberUpdated"] = None
    chat_join_request: Optional["ChatJoinRequest"] = None


class WebhookInfo(BaseModel):
    url: str
    has_custom_certificate: bool
    pending_update_count: int
    ip_address: Optional[str] = None
    last_error_date: Optional[int] = None
    last_error_message: Optional[str] = None
    last_synchronization_error_date: Optional[int] = None
    max_connections: Optional[int] = None
    allowed_updates: Optional[List[str]] = None


class User(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[Literal[True]] = None
    added_to_attachment_menu: Optional[Literal[True]] = None
    """
    :说明: 用户的语言编码，比如中文用户是 zh-hans

    :类型: ``Optional[str] = None``
    """
    can_join_groups: Optional[bool] = None
    """
    :说明: 是否可加入群聊，只会在机器人的 get_me 方法中返回

    :类型: ``Optional[bool] = None``
    """
    can_read_all_group_messages: Optional[bool] = None
    """
    :说明: 是否可以读取所有群消息，只会在机器人的 get_me 方法中返回

    :类型: ``Optional[bool] = None``
    """
    supports_inline_queries: Optional[bool] = None
    """
    :说明: 是否支持 inline_queries，只会在机器人的 get_me 方法中返回

    :类型: ``Optional[bool] = None``
    """


class Chat(BaseModel):
    id: int
    type: Literal["private", "group", "supergroup", "channel"]
    title: Optional[str] = None
    """
    :说明: 聊天标题，只会在聊天类型为 group supergroups channel 时返回

    :类型: ``Optional[str] = None``
    """
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_forum: Optional[Literal[True]] = None
    photo: Optional["ChatPhoto"] = None
    """
    :说明: 聊天图片，仅在使用 get_chat 方法时返回

    :类型: ``Optional[ChatPhoto] = None``
    """
    active_usernames: Optional[List[str]] = None
    emoji_status_custom_emoji_id: Optional[str] = None
    bio: Optional[str] = None
    """
    :说明: 聊天 ?，仅在使用 get_chat 方法时返回

    :类型: ``Optional[str] = None``
    """
    has_private_forwards: Optional[Literal[True]] = None
    has_restricted_voice_and_video_messages: Optional[Literal[True]] = None
    join_to_send_messages: Optional[Literal[True]] = None
    join_by_request: Optional[Literal[True]] = None
    description: Optional[str] = None
    """
    :说明: 聊天简介，仅在使用 get_chat 方法时返回

    :类型: ``Optional[str] = None``
    """
    invite_link: Optional[str] = None
    """
    :说明: 邀请链接，仅在使用 get_chat 方法时返回

    :类型: ``Optional[str] = None``
    """
    pinned_message: Optional["Message"] = None
    """
    :说明: 置顶消息，仅在使用 get_chat 方法时返回

    :类型: ``Optional[Message] = None``
    """
    permissions: Optional["ChatPermissions"] = None
    """
    :说明: 成员权限，仅在使用 get_chat 方法时返回

    :类型: ``Optional[ChatPermissions] = None``
    """
    slow_mode_delay: Optional[int] = None
    """
    :说明: 消息频率限制，仅在使用 get_chat 方法时返回

    :类型: ``Optional[int] = None``
    """
    message_auto_delete_time: Optional[int] = None
    """
    :说明: 消息自动撤回时间，仅在使用 get_chat 方法时返回

    :类型: ``Optional[int] = None``
    """
    has_aggressive_anti_spam_enabled: Optional[Literal[True]] = None
    has_hidden_members: Optional[Literal[True]] = None
    has_protected_content: Optional[Literal[True]] = None
    sticker_set_name: Optional[str] = None
    """
    :说明: 聊天表情包，仅在使用 get_chat 方法时返回

    :类型: ``Optional[string] = None``
    """
    can_set_sticker_set: Optional[Literal[True]] = None
    """
    :说明: 机器人是否可设置聊天表情包，仅在使用 get_chat 方法时返回

    :类型: ``Optional[bool] = None``
    """
    linked_chat_id: Optional[int] = None
    """
    :说明: 链接到的聊天的 id，仅在使用 get_chat 方法时返回

    :类型: ``Optional[int] = None``
    """
    location: Optional["ChatLocation"] = None
    """
    :说明: 聊天地址，仅在使用 get_chat 方法时返回

    :类型: ``Optional[ChatLocation] = None``
    """


class Message(BaseModel):
    message_id: int
    message_thread_id: Optional[int] = None
    from_: Optional[User] = Field(default=None, alias="from")
    sender_chat: Optional[Chat] = None
    date: int
    chat: Chat
    forward_from: Optional[User] = None
    forward_from_chat: Optional[Chat] = None
    forward_from_message_id: Optional[int] = None
    forward_signature: Optional[str] = None
    forward_sender_name: Optional[str] = None
    forward_date: Optional[int] = None
    is_topic_message: Optional[Literal[True]] = None
    is_automatic_forward: Optional[Literal[True]] = None
    reply_to_message: Optional["Message"] = None
    via_bot: Optional[User] = None
    edit_date: Optional[int] = None
    has_protected_content: Optional[Literal[True]] = None
    media_group_id: Optional[str] = None
    author_signature: Optional[str] = None
    text: Optional[str] = None
    entities: Optional[List["MessageEntity"]] = None
    animation: Optional["Animation"] = None
    audio: Optional["Audio"] = None
    document: Optional["Document"] = None
    photo: Optional[List["PhotoSize"]] = None
    sticker: Optional["Sticker"] = None
    video: Optional["Video"] = None
    video_note: Optional["VideoNote"] = None
    voice: Optional["Voice"] = None
    caption: Optional[str] = None
    caption_entities: Optional[List["MessageEntity"]] = None
    has_media_spoiler: Optional[Literal[True]] = None
    contact: Optional["Contact"] = None
    dice: Optional["Dice"] = None
    game: Optional["Game"] = None
    poll: Optional["Poll"] = None
    venue: Optional["Venue"] = None
    location: Optional["Location"] = None
    new_chat_members: Optional[List[User]] = None
    left_chat_member: Optional[User] = None
    new_chat_title: Optional[str] = None
    new_chat_photo: Optional[List["PhotoSize"]] = None
    delete_chat_photo: Optional[Literal[True]] = None
    group_chat_created: Optional[Literal[True]] = None
    supergroup_chat_created: Optional[Literal[True]] = None
    channel_chat_created: Optional[Literal[True]] = None
    message_auto_delete_timer_changed: Optional["MessageAutoDeleteTimerChanged"] = None
    migrate_to_chat_id: Optional[int] = None
    migrate_from_chat_id: Optional[int] = None
    pinned_message: Optional["Message"] = None
    invoice: Optional["Invoice"] = None
    successful_payment: Optional["SuccessfulPayment"] = None
    user_shared: Optional["UserShared"] = None
    chat_shared: Optional["ChatShared"] = None
    connected_website: Optional[str] = None
    write_access_allowed: Optional["WriteAccessAllowed"] = None
    passport_data: Optional["PassportData"] = None
    proximity_alert_triggered: Optional["ProximityAlertTriggered"] = None
    forum_topic_created: Optional["ForumTopicCreated"] = None
    forum_topic_edited: Optional["ForumTopicEdited"] = None
    general_forum_topic_hidden: Optional["GeneralForumTopicHidden"] = None
    general_forum_topic_unhidden: Optional["GeneralForumTopicUnhidden"] = None
    forum_topic_closed: Optional["ForumTopicClosed"] = None
    forum_topic_reopened: Optional["ForumTopicReopened"] = None
    video_chat_scheduled: Optional["VideoChatScheduled"] = None
    video_chat_started: Optional["VideoChatStarted"] = None
    video_chat_ended: Optional["VideoChatEnded"] = None
    video_chat_participants_invited: Optional["VideoChatParticipantsInvited"] = None
    web_app_data: Optional["WebAppData"] = None
    reply_markup: Optional["InlineKeyboardMarkup"] = None


class MessageId(BaseModel):
    message_id: int


class MessageEntity(BaseModel):
    type: str
    offset: int
    length: int
    url: Optional[str] = None
    user: Optional[User] = None
    language: Optional[str] = None
    custom_emoji_id: Optional[str] = None


class PhotoSize(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: Optional[int] = None


class Animation(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumb: Optional[PhotoSize] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None


class Audio(BaseModel):
    file_id: str
    file_unique_id: str
    duration: int
    performer: Optional[str] = None
    title: Optional[str] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    thumb: Optional[PhotoSize] = None


class Document(BaseModel):
    file_id: str
    file_unique_id: str
    thumb: Optional[PhotoSize] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None


class Video(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumb: Optional[PhotoSize] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None


class VideoNote(BaseModel):
    file_id: str
    file_unique_id: str
    length: int
    duration: int
    thumb: Optional[PhotoSize] = None
    file_size: Optional[int] = None


class Voice(BaseModel):
    file_id: str
    file_unique_id: str
    duration: int
    mime_type: Optional[str] = None
    file_size: Optional[int] = None


class Contact(BaseModel):
    phone_number: str
    first_name: str
    last_name: Optional[str] = None
    user_id: Optional[int] = None
    vcard: Optional[str] = None


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
    correct_option_id: Optional[int] = None
    explanation: Optional[str] = None
    explanation_entities: Optional[List[MessageEntity]] = None
    open_period: Optional[int] = None
    close_date: Optional[int] = None


class Location(BaseModel):
    longitude: float
    latitude: float
    horizontal_accuracy: Optional[float] = None
    live_period: Optional[int] = None
    heading: Optional[int] = None
    proximity_alert_radius: Optional[int] = None


class Venue(BaseModel):
    location: Location
    title: str
    address: str
    foursquare_id: Optional[str] = None
    foursquare_type: Optional[str] = None
    google_place_id: Optional[str] = None
    google_place_type: Optional[str] = None


class WebAppData(BaseModel):
    data: str
    button_text: str


class ProximityAlertTriggered(BaseModel):
    traveler: User
    watcher: User
    distance: int


class MessageAutoDeleteTimerChanged(BaseModel):
    message_auto_delete_time: int


class ForumTopicCreated(BaseModel):
    name: str
    icon_color: int
    icon_custom_emoji_id: Optional[str] = None


class ForumTopicClosed(BaseModel):
    pass


class ForumTopicEdited(BaseModel):
    name: Optional[str] = None
    icon_custom_emoji_id: Optional[str] = None


class ForumTopicReopened(BaseModel):
    pass


class GeneralForumTopicHidden(BaseModel):
    pass


class GeneralForumTopicUnhidden(BaseModel):
    pass


class UserShared(BaseModel):
    request_id: int
    user_id: int


class ChatShared(BaseModel):
    request_id: int
    chat_id: int


class WriteAccessAllowed(BaseModel):
    pass


class VideoChatScheduled(BaseModel):
    start_date: int


class VideoChatStarted(BaseModel):
    pass


class VideoChatEnded(BaseModel):
    duration: int


class VideoChatParticipantsInvited(BaseModel):
    users: List[User]


class UserProfilePhotos(BaseModel):
    total_count: int
    photos: List[List[PhotoSize]]


class File(BaseModel):
    file_id: str
    file_unique_id: str
    file_size: Optional[int] = None
    file_path: Optional[str] = None


class WebAppInfo(BaseModel):
    url: str


class KeyboardButtonRequestUser(BaseModel):
    request_id: int
    user_is_bot: Optional[bool] = None
    user_is_premium: Optional[bool] = None


class KeyboardButtonRequestChat(BaseModel):
    request_id: int
    chat_is_channel: bool
    chat_is_forum: Optional[bool] = None
    chat_has_username: Optional[bool] = None
    chat_is_created: Optional[bool] = None
    user_administrator_rights: Optional["ChatAdministratorRights"] = None
    bot_administrator_rights: Optional["ChatAdministratorRights"] = None
    bot_is_member: Optional[bool] = None


class KeyboardButtonPollType(BaseModel):
    type: Optional[str] = None


class KeyboardButton(BaseModel):
    text: str
    request_user: Optional[KeyboardButtonRequestUser] = None
    request_chat: Optional[KeyboardButtonRequestChat] = None
    request_contact: Optional[bool] = None
    request_location: Optional[bool] = None
    request_poll: Optional[KeyboardButtonPollType] = None
    web_app: Optional[WebAppInfo] = None


class ReplyKeyboardMarkup(BaseModel):
    keyboard: List[List[KeyboardButton]]
    is_persistent: Optional[bool] = None
    resize_keyboard: Optional[bool] = None
    one_time_keyboard: Optional[bool] = None
    input_field_placeholder: Optional[str] = None
    selective: Optional[bool] = None


class ReplyKeyboardRemove(BaseModel):
    remove_keyboard: Literal[True]
    selective: Optional[bool] = None


class LoginUrl(BaseModel):
    url: str
    forward_text: Optional[str] = None
    bot_username: Optional[str] = None
    request_write_access: Optional[bool] = None


class InlineKeyboardButton(BaseModel):
    text: str
    url: Optional[str] = None
    callback_data: Optional[str] = None
    web_app: Optional[WebAppInfo] = None
    login_url: Optional[LoginUrl] = None
    switch_inline_query: Optional[str] = None
    switch_inline_query_current_chat: Optional[str] = None
    callback_game: Optional["CallbackGame"] = None
    pay: Optional[bool] = None


class InlineKeyboardMarkup(BaseModel):
    inline_keyboard: List[List[InlineKeyboardButton]]


class CallbackQuery(BaseModel):
    id: str
    from_: User = Field(alias="from")
    message: Optional[Message] = None
    inline_message_id: Optional[str] = None
    chat_instance: str
    data: Optional[str] = None
    game_short_name: Optional[str] = None


class ForceReply(BaseModel):
    force_reply: Literal[True]
    input_field_placeholder: Optional[str] = None
    selective: Optional[bool] = None


class ChatPhoto(BaseModel):
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str


class ChatInviteLink(BaseModel):
    invite_link: str
    creator: User
    creates_join_request: bool
    is_primary: bool
    is_revoked: bool
    name: Optional[str] = None
    expire_date: Optional[int] = None
    member_limit: Optional[int] = None
    pending_join_request_count: Optional[int] = None


class ChatAdministratorRights(BaseModel):
    is_anonymous: bool
    can_manage_chat: bool
    can_delete_messages: bool
    can_manage_video_chats: bool
    can_restrict_members: bool
    can_promote_members: bool
    can_change_info: bool
    can_invite_users: bool
    can_post_messages: Optional[bool] = None
    can_edit_messages: Optional[bool] = None
    can_pin_messages: Optional[bool] = None
    can_manage_topics: Optional[bool] = None


class ChatMember(BaseModel):
    status: str
    user: User


class ChatMemberOwner(ChatMember):
    status: Literal["creator"] = "creator"
    is_anonymous: bool
    custom_title: Optional[str] = None


class ChatMemberAdministrator(ChatMember):
    status: Literal["administrator"] = "administrator"
    can_be_edited: bool
    is_anonymous: bool
    can_manage_chat: bool
    can_delete_messages: bool
    can_manage_video_chats: bool
    can_restrict_members: bool
    can_promote_members: bool
    can_change_info: bool
    can_invite_users: bool
    can_post_messages: Optional[bool] = None
    can_edit_messages: Optional[bool] = None
    can_pin_messages: Optional[bool] = None
    can_manage_topics: Optional[bool] = None
    custom_title: Optional[str] = None


class ChatMemberMember(ChatMember):
    status: Literal["member"] = "member"


class ChatMemberRestricted(ChatMember):
    status: Literal["restricted"] = "restricted"
    is_member: bool
    can_change_info: bool
    can_invite_users: bool
    can_pin_messages: bool
    can_manage_topics: bool
    can_send_messages: bool
    can_send_audios: bool
    can_send_documents: bool
    can_send_photos: bool
    can_send_videos: bool
    can_send_video_notes: bool
    can_send_voice_notes: bool
    can_send_polls: bool
    can_send_other_messages: bool
    can_add_web_page_previews: bool
    until_date: int


class ChatMemberLeft(ChatMember):
    status: Literal["left"] = "left"


class ChatMemberBanned(ChatMember):
    status: Literal["kicked"] = "kicked"
    until_date: int


class ChatMemberUpdated(BaseModel):
    chat: Chat
    from_: User = Field(alias="from")
    date: int
    old_chat_member: ChatMember
    new_chat_member: ChatMember
    invite_link: Optional[ChatInviteLink] = None


class ChatJoinRequest(BaseModel):
    chat: Chat
    from_: User = Field(alias="from")
    user_chat_id: int
    date: int
    bio: Optional[str] = None
    invite_link: Optional[ChatInviteLink] = None


class ChatPermissions(BaseModel):
    can_send_messages: Optional[bool] = None
    can_send_audios: Optional[bool] = None
    can_send_documents: Optional[bool] = None
    can_send_photos: Optional[bool] = None
    can_send_videos: Optional[bool] = None
    can_send_video_notes: Optional[bool] = None
    can_send_voice_notes: Optional[bool] = None
    can_send_polls: Optional[bool] = None
    can_send_other_messages: Optional[bool] = None
    can_add_web_page_previews: Optional[bool] = None
    can_change_info: Optional[bool] = None
    can_invite_users: Optional[bool] = None
    can_pin_messages: Optional[bool] = None
    can_manage_topics: Optional[bool] = None


class ChatLocation(BaseModel):
    location: Location
    address: str


class ForumTopic(BaseModel):
    message_thread_id: int
    name: str
    icon_color: int
    icon_custom_emoji_id: Optional[str] = None


class BotCommand(BaseModel):
    command: str
    description: str


class BotCommandScope(BaseModel):
    type: str


class BotCommandScopeDefault(BotCommandScope):
    type: Literal["default"] = "default"


class BotCommandScopeAllPrivateChats(BotCommandScope):
    type: Literal["all_private_chats"] = "all_private_chats"


class BotCommandScopeAllGroupChats(BotCommandScope):
    type: Literal["all_group_chats"] = "all_group_chats"


class BotCommandScopeAllChatAdministrators(BotCommandScope):
    type: Literal["all_chat_administrators"] = "all_chat_administrators"


class BotCommandScopeChat(BotCommandScope):
    type: Literal["chat"] = "chat"
    chat_id: Union[int, str]


class BotCommandScopeChatAdministrators(BotCommandScope):
    type: Literal["chat_administrators"] = "chat_administrators"
    chat_id: Union[int, str]


class BotCommandScopeChatMember(BotCommandScope):
    type: Literal["chat_member"] = "chat_member"
    chat_id: Union[int, str]
    user_id: int


class MenuButton(BaseModel):
    type: str


class MenuButtonCommands(MenuButton):
    type: Literal["commmands"] = "commmands"


class MenuButtonWebApp(MenuButton):
    type: Literal["web_app"] = "web_app"
    text: str
    web_app: WebAppInfo


class MenuButtonDefault(MenuButton):
    type: Literal["default"] = "default"


class ResponseParameters(BaseModel):
    migrate_to_chat_id: Optional[int] = None
    retry_after: Optional[int] = None


InputFile = bytes


class InputMedia(BaseModel):
    type: str
    media: str
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None


class InputMediaPhoto(InputMedia):
    type: Literal["photo"] = "photo"
    has_spoiler: Optional[bool] = None


class InputMediaVideo(InputMedia):
    type: Literal["video"] = "video"
    thumb: Optional[Union[InputFile, str]] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
    supports_streaming: Optional[bool] = None
    has_spoiler: Optional[bool] = None


class InputMediaAnimation(InputMedia):
    type: Literal["animation"] = "animation"
    thumb: Optional[Union[InputFile, str]] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
    has_spoiler: Optional[bool] = None


class InputMediaAudio(InputMedia):
    type: Literal["audio"] = "audio"
    thumb: Optional[Union[InputFile, str]] = None
    duration: Optional[int] = None
    performer: Optional[str] = None
    title: Optional[str] = None


class InputMediaDocument(InputMedia):
    type: Literal["document"] = "document"
    thumb: Optional[Union[InputFile, str]] = None
    disable_content_type_detection: Optional[bool] = None


class MaskPosition(BaseModel):
    point: str
    x_shift: float
    y_shift: float
    scale: float


class Sticker(BaseModel):
    file_id: str
    file_unique_id: str
    type: str
    width: int
    height: int
    is_animated: bool
    is_video: bool
    thumb: Optional[PhotoSize] = None
    emoji: Optional[str] = None
    set_name: Optional[str] = None
    premium_animation: Optional[File] = None
    mask_position: Optional[MaskPosition] = None
    custom_emoji_id: Optional[str] = None
    file_size: Optional[int] = None


class StickerSet(BaseModel):
    name: str
    title: str
    sticker_type: str
    is_animated: bool
    is_video: bool
    stickers: List[Sticker]
    thumb: Optional[PhotoSize] = None


class InlineQuery(BaseModel):
    id: str
    from_: User = Field(alias="from")
    query: str
    offset: str
    chat_type: Optional[str] = None
    location: Optional[Location] = None


class InputMessageContent(BaseModel):
    pass


class InputTextMessageContent(InputMessageContent):
    message_text: str
    parse_mode: Optional[str] = None
    entities: Optional[List[MessageEntity]] = None
    disable_web_page_preview: Optional[bool] = None


class InputLocationMessageContent(InputMessageContent):
    latitude: float
    longitude: float
    horizontal_accuracy: Optional[float] = None
    live_period: Optional[int] = None
    heading: Optional[int] = None
    proximity_alert_radius: Optional[int] = None


class InputVenueMessageContent(InputMessageContent):
    latitude: float
    longitude: float
    title: str
    address: str
    foursquare_id: Optional[str] = None
    foursquare_type: Optional[str] = None
    google_place_id: Optional[str] = None
    google_place_type: Optional[str] = None


class InputContactMessageContent(InputMessageContent):
    phone_number: str
    first_name: str
    last_name: Optional[str] = None
    vcard: Optional[str] = None


class InputInvoiceMessageContent(InputMessageContent):
    title: str
    description: str
    payload: str
    provider_token: str
    currency: str
    prices: List["LabeledPrice"]
    max_tip_amount: Optional[int] = None
    suggested_tip_amounts: Optional[List[int]] = None
    provider_data: Optional[str] = None
    photo_url: Optional[str] = None
    photo_size: Optional[int] = None
    photo_width: Optional[int] = None
    photo_height: Optional[int] = None
    need_name: Optional[bool] = None
    need_phone_number: Optional[bool] = None
    need_email: Optional[bool] = None
    need_shipping_address: Optional[bool] = None
    send_phone_number_to_provider: Optional[bool] = None
    send_email_to_provider: Optional[bool] = None
    is_flexible: Optional[bool] = None


class InlineQueryResult(BaseModel):
    type: str
    id: str
    reply_markup: Optional[InlineKeyboardMarkup] = None


class InlineQueryResultArticle(InlineQueryResult):
    type: Literal["article"] = "article"
    title: str
    input_message_content: InputMessageContent
    url: Optional[str] = None
    hide_url: Optional[bool] = None
    description: Optional[str] = None
    thumb_url: Optional[str] = None
    thumb_width: Optional[int] = None
    thumb_height: Optional[int] = None


class InlineQueryResultPhoto(InlineQueryResult):
    type: Literal["photo"] = "photo"
    photo_url: str
    thumb_url: str
    photo_width: Optional[int] = None
    photo_height: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    input_message_content: Optional[InputMessageContent] = None


class InlineQueryResultGif(InlineQueryResult):
    type: Literal["gif"] = "gif"
    gif_url: str
    gif_width: Optional[int] = None
    gif_height: Optional[int] = None
    gif_duration: Optional[int] = None
    thumb_url: str
    thumb_mime_type: Optional[str] = None
    title: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    input_message_content: Optional[InputMessageContent] = None


class InlineQueryResultMpeg4Gif(InlineQueryResult):
    type: Literal["mpeg4_gif"] = "mpeg4_gif"
    mpeg4_url: str
    mpeg4_width: Optional[int] = None
    mpeg4_height: Optional[int] = None
    mpeg4_duration: Optional[int] = None
    thumb_url: str
    thumb_mime_type: Optional[str] = None
    title: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    input_message_content: Optional[InputMessageContent] = None


class InlineQueryResultVideo(InlineQueryResult):
    type: Literal["video"] = "video"
    video_url: str
    mime_type: str
    thumb_url: str
    title: str
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    video_width: Optional[int] = None
    video_height: Optional[int] = None
    video_duration: Optional[int] = None
    description: Optional[str] = None
    input_message_content: Optional[InputMessageContent] = None


class InlineQueryResultAudio(InlineQueryResult):
    type: Literal["audio"] = "audio"
    audio_url: str
    title: str
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    performer: Optional[str] = None
    audio_duration: Optional[int] = None
    input_message_content: Optional[InputMessageContent] = None


class InlineQueryResultVoice(InlineQueryResult):
    type: Literal["voice"] = "voice"
    voice_url: str
    title: str
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    voice_duration: Optional[int] = None
    input_message_content: Optional[InputMessageContent] = None


class InlineQueryResultDocument(InlineQueryResult):
    type: Literal["document"] = "document"
    title: str
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    document_url: str
    mime_type: str
    description: Optional[str] = None
    input_message_content: Optional[InputMessageContent] = None
    thumb_url: Optional[str] = None
    thumb_width: Optional[int] = None
    thumb_height: Optional[int] = None


class InlineQueryResultLocation(InlineQueryResult):
    type: Literal["location"] = "location"
    latitude: float
    longitude: float
    title: str
    horizontal_accuracy: Optional[float] = None
    live_period: Optional[int] = None
    heading: Optional[int] = None
    proximity_alert_radius: Optional[int] = None
    input_message_content: Optional[InputMessageContent] = None
    thumb_url: Optional[str] = None
    thumb_width: Optional[int] = None
    thumb_height: Optional[int] = None


class InlineQueryResultVenue(InlineQueryResult):
    type: Literal["venue"] = "venue"
    latitude: float
    longitude: float
    title: str
    address: str
    foursquare_id: Optional[str] = None
    foursquare_type: Optional[str] = None
    google_place_id: Optional[str] = None
    google_place_type: Optional[str] = None
    input_message_content: Optional[InputMessageContent] = None
    thumb_url: Optional[str] = None
    thumb_width: Optional[int] = None
    thumb_height: Optional[int] = None


class InlineQueryResultContact(InlineQueryResult):
    type: Literal["contact"] = "contact"
    phone_number: str
    first_name: str
    last_name: Optional[str] = None
    user_id: Optional[int] = None
    vcard: Optional[str] = None
    input_message_content: Optional[InputMessageContent] = None
    thumb_url: Optional[str] = None
    thumb_width: Optional[int] = None
    thumb_height: Optional[int] = None


class InlineQueryResultGame(InlineQueryResult):
    type: Literal["game"] = "game"
    game_short_name: str


class InlineQueryResultCachedPhoto(InlineQueryResult):
    type: Literal["photo"] = "photo"
    photo_file_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    input_message_content: Optional[InputMessageContent] = None


class InlineQueryResultCachedGif(InlineQueryResult):
    type: Literal["gif"] = "gif"
    gif_file_id: str
    title: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    input_message_content: Optional[InputMessageContent] = None


class InlineQueryResultCachedMpeg4Gif(InlineQueryResult):
    type: Literal["mpeg4_gif"] = "mpeg4_gif"
    mpeg4_file_id: str
    title: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    input_message_content: Optional[InputMessageContent] = None


class InlineQueryResultCachedSticker(InlineQueryResult):
    type: Literal["sticker"] = "sticker"
    sticker_file_id: str
    input_message_content: Optional[InputMessageContent] = None


class InlineQueryResultCachedDocument(InlineQueryResult):
    type: Literal["document"] = "document"
    title: str
    document_file_id: str
    description: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    input_message_content: Optional[InputMessageContent] = None


class InlineQueryResultCachedVideo(InlineQueryResult):
    type: Literal["video"] = "video"
    video_file_id: str
    title: str
    description: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    input_message_content: Optional[InputMessageContent] = None


class InlineQueryResultCachedVoice(InlineQueryResult):
    type: Literal["voice"] = "voice"
    voice_file_id: str
    title: str
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    input_message_content: Optional[InputMessageContent] = None


class InlineQueryResultCachedAudio(InlineQueryResult):
    type: Literal["audio"] = "audio"
    audio_file_id: str
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    input_message_content: Optional[InputMessageContent] = None


class ChosenInlineResult(BaseModel):
    result_id: str
    from_: User = Field(alias="from")
    location: Optional[Location] = None
    inline_message_id: Optional[str] = None
    query: str


class SentWebAppMessage(BaseModel):
    inline_message_id: Optional[str] = None


class LabeledPrice(BaseModel):
    label: str
    amount: int


class Invoice(BaseModel):
    title: str
    description: str
    start_parameter: str
    currency: str
    total_amount: int


class ShippingAddress(BaseModel):
    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str


class OrderInfo(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    shipping_address: Optional[ShippingAddress] = None


class ShippingOption(BaseModel):
    id: str
    title: str
    prices: List[LabeledPrice]


class SuccessfulPayment(BaseModel):
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: Optional[str] = None
    order_info: Optional[OrderInfo] = None
    telegram_payment_charge_id: str
    provider_payment_charge_id: str


class ShippingQuery(BaseModel):
    id: str
    from_: User = Field(alias="from")
    invoice_payload: str
    shipping_address: ShippingAddress


class PreCheckoutQuery(BaseModel):
    id: str
    from_: User = Field(alias="from")
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: Optional[str] = None
    order_info: Optional[OrderInfo] = None


class PassportFile(BaseModel):
    file_id: str
    file_unique_id: str
    file_size: int
    file_date: int


class EncryptedPassportElement(BaseModel):
    type: str
    data: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    files: Optional[List[PassportFile]] = None
    front_side: Optional[PassportFile] = None
    reverse_side: Optional[PassportFile] = None
    selfie: Optional[PassportFile] = None
    translation: Optional[List[PassportFile]] = None
    hash: str


class EncryptedCredentials(BaseModel):
    data: str
    hash: str
    secret: str


class PassportElementError(BaseModel):
    source: str
    type: str
    message: str


class PassportElementErrorDataField(PassportElementError):
    source: Literal["data"] = "data"
    field_name: str
    data_hash: str


class PassportElementErrorFrontSide(PassportElementError):
    source: Literal["front_side"] = "front_side"
    file_hash: str


class PassportElementErrorReverseSide(PassportElementError):
    source: Literal["reverse_side"] = "reverse_side"
    file_hash: str


class PassportElementErrorSelfie(PassportElementError):
    source: Literal["selfie"] = "selfie"
    file_hash: str


class PassportElementErrorFile(PassportElementError):
    source: Literal["file"] = "file"
    file_hash: str


class PassportElementErrorFiles(PassportElementError):
    source: Literal["files"] = "files"
    file_hashes: List[str]


class PassportElementErrorTranslationFile(PassportElementError):
    source: Literal["translation_file"] = "translation_file"
    file_hash: str


class PassportElementErrorTranslationFiles(PassportElementError):
    source: Literal["translation_files"] = "translation_files"
    file_hashes: List[str]


class PassportElementErrorUnspecified(PassportElementError):
    source: Literal["unspecified"] = "unspecified"
    element_hash: str


class PassportData(BaseModel):
    data: List[EncryptedPassportElement]
    credentials: EncryptedCredentials


class Game(BaseModel):
    title: str
    description: str
    photo: List[PhotoSize]
    text: Optional[str] = None
    text_entities: Optional[List[MessageEntity]] = None
    animation: Optional[Animation] = None


class CallbackGame(BaseModel):
    pass


class GameHighScore(BaseModel):
    position: int
    user: User
    score: int


# 动态语言的悲哀
Update.update_forward_refs()
Chat.update_forward_refs()
Message.update_forward_refs()
KeyboardButtonRequestChat.update_forward_refs()
InlineKeyboardButton.update_forward_refs()
InputInvoiceMessageContent.update_forward_refs()
