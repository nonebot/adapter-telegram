from typing import Union, Literal, Optional

from pydantic import Field, BaseModel


class User(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    is_premium: Literal[True] | None = None
    added_to_attachment_menu: Literal[True] | None = None
    can_join_groups: bool | None = None
    can_read_all_group_messages: bool | None = None
    supports_inline_queries: bool | None = None
    can_connect_to_business: bool | None = None
    has_main_web_app: bool | None = None


class Chat(BaseModel):
    id: int
    type: Literal["private", "group", "supergroup", "channel"]
    title: str | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_forum: Literal[True] | None = None


class MessageOriginUser(BaseModel):
    type: Literal["user"] = "user"
    date: int
    sender_user: User


class MessageOriginHiddenUser(BaseModel):
    type: Literal["hidden_user"] = "hidden_user"
    date: int
    sender_user_name: str


class MessageOriginChat(BaseModel):
    type: Literal["chat"] = "chat"
    date: int
    sender_chat: Chat
    author_signature: str | None = None


class MessageOriginChannel(BaseModel):
    type: Literal["channel"] = "channel"
    date: int
    chat: Chat
    message_id: int
    author_signature: str | None = None


MessageOrigin = Union[
    MessageOriginUser, MessageOriginHiddenUser, MessageOriginChat, MessageOriginChannel
]


class LinkPreviewOptions(BaseModel):
    is_disabled: bool | None = None
    url: str | None = None
    prefer_small_media: bool | None = None
    prefer_large_media: bool | None = None
    show_above_text: bool | None = None


class PhotoSize(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: int | None = None


class Animation(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumbnail: PhotoSize | None = None
    file_name: str | None = None
    mime_type: str | None = None
    file_size: int | None = None


class Audio(BaseModel):
    file_id: str
    file_unique_id: str
    duration: int
    performer: str | None = None
    title: str | None = None
    file_name: str | None = None
    mime_type: str | None = None
    file_size: int | None = None
    thumbnail: PhotoSize | None = None


class Document(BaseModel):
    file_id: str
    file_unique_id: str
    thumbnail: PhotoSize | None = None
    file_name: str | None = None
    mime_type: str | None = None
    file_size: int | None = None


class PaidMediaPreview(BaseModel):
    type: Literal["preview"] = "preview"
    width: int | None = None
    height: int | None = None
    duration: int | None = None


class PaidMediaPhoto(BaseModel):
    type: Literal["photo"] = "photo"
    photo: list[PhotoSize]


class Video(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumbnail: PhotoSize | None = None
    file_name: str | None = None
    mime_type: str | None = None
    file_size: int | None = None


class PaidMediaVideo(BaseModel):
    type: Literal["video"] = "video"
    video: Video


PaidMedia = Union[PaidMediaPreview, PaidMediaPhoto, PaidMediaVideo]


class PaidMediaInfo(BaseModel):
    star_count: int
    paid_media: list[PaidMedia]


class File(BaseModel):
    file_id: str
    file_unique_id: str
    file_size: int | None = None
    file_path: str | None = None


class MaskPosition(BaseModel):
    point: Literal["forehead", "eyes", "mouth", "chin"]
    x_shift: float
    y_shift: float
    scale: float


class Sticker(BaseModel):
    file_id: str
    file_unique_id: str
    type: Literal["regular", "mask", "custom_emoji"]
    width: int
    height: int
    is_animated: bool
    is_video: bool
    thumbnail: PhotoSize | None = None
    emoji: str | None = None
    set_name: str | None = None
    premium_animation: File | None = None
    mask_position: MaskPosition | None = None
    custom_emoji_id: str | None = None
    needs_repainting: Literal[True] | None = None
    file_size: int | None = None


class Story(BaseModel):
    chat: Chat
    id: int


class VideoNote(BaseModel):
    file_id: str
    file_unique_id: str
    length: int
    duration: int
    thumbnail: PhotoSize | None = None
    file_size: int | None = None


class Voice(BaseModel):
    file_id: str
    file_unique_id: str
    duration: int
    mime_type: str | None = None
    file_size: int | None = None


class Contact(BaseModel):
    phone_number: str
    first_name: str
    last_name: str | None = None
    user_id: int | None = None
    vcard: str | None = None


class Dice(BaseModel):
    emoji: Literal["🎲", "🎯", "🏀", "⚽", "🎳", "🎰"]
    value: int


class MessageEntity(BaseModel):
    type: Literal[
        "mention",
        "hashtag",
        "cashtag",
        "bot_command",
        "url",
        "email",
        "phone_number",
        "bold",
        "italic",
        "underline",
        "strikethrough",
        "spoiler",
        "expandable_blockquote",
        "blockquote",
        "code",
        "pre",
        "text_link",
        "text_mention",
        "custom_emoji",
    ]
    offset: int
    length: int
    url: str | None = None
    user: User | None = None
    language: str | None = None
    custom_emoji_id: str | None = None


class Game(BaseModel):
    title: str
    description: str
    photo: list[PhotoSize]
    text: str | None = None
    text_entities: list[MessageEntity] | None = None
    animation: Animation | None = None


class Giveaway(BaseModel):
    chats: list[Chat]
    winners_selection_date: int
    winner_count: int
    only_new_members: Literal[True] | None = None
    has_public_winners: Literal[True] | None = None
    prize_description: str | None = None
    country_codes: list[str] | None = None
    prize_star_count: int | None = None
    premium_subscription_month_count: int | None = None


class GiveawayWinners(BaseModel):
    chat: Chat
    giveaway_message_id: int
    winners_selection_date: int
    winner_count: int
    winners: list[User]
    additional_chat_count: int | None = None
    prize_star_count: int | None = None
    premium_subscription_month_count: int | None = None
    unclaimed_prize_count: int | None = None
    only_new_members: Literal[True] | None = None
    was_refunded: Literal[True] | None = None
    prize_description: str | None = None


class Invoice(BaseModel):
    title: str
    description: str
    start_parameter: str
    currency: str
    total_amount: int


class Location(BaseModel):
    latitude: float
    longitude: float
    horizontal_accuracy: float | None = None
    live_period: int | None = None
    heading: int | None = None
    proximity_alert_radius: int | None = None


class PollOption(BaseModel):
    text: str
    text_entities: list[MessageEntity] | None = None
    voter_count: int


class Poll(BaseModel):
    id: str
    question: str
    question_entities: list[MessageEntity] | None = None
    options: list[PollOption]
    total_voter_count: int
    is_closed: bool
    is_anonymous: bool
    type: Literal["regular", "quiz"]
    allows_multiple_answers: bool
    correct_option_id: int | None = None
    explanation: str | None = None
    explanation_entities: list[MessageEntity] | None = None
    open_period: int | None = None
    close_date: int | None = None


class Venue(BaseModel):
    location: Location
    title: str
    address: str
    foursquare_id: str | None = None
    foursquare_type: str | None = None
    google_place_id: str | None = None
    google_place_type: str | None = None


class ExternalReplyInfo(BaseModel):
    origin: MessageOrigin
    chat: Chat | None = None
    message_id: int | None = None
    link_preview_options: LinkPreviewOptions | None = None
    animation: Animation | None = None
    audio: Audio | None = None
    document: Document | None = None
    paid_media: PaidMediaInfo | None = None
    photo: list[PhotoSize] | None = None
    sticker: Sticker | None = None
    story: Story | None = None
    video: Video | None = None
    video_note: VideoNote | None = None
    voice: Voice | None = None
    has_media_spoiler: Literal[True] | None = None
    contact: Contact | None = None
    dice: Dice | None = None
    game: Game | None = None
    giveaway: Giveaway | None = None
    giveaway_winners: GiveawayWinners | None = None
    invoice: Invoice | None = None
    location: Location | None = None
    poll: Poll | None = None
    venue: Venue | None = None


class TextQuote(BaseModel):
    text: str
    entities: list[MessageEntity] | None = None
    position: int
    is_manual: Literal[True] | None = None


class MessageAutoDeleteTimerChanged(BaseModel):
    message_auto_delete_time: int


class InaccessibleMessage(BaseModel):
    chat: Chat
    message_id: int
    date: int


MaybeInaccessibleMessage = Union["Message", InaccessibleMessage]


class ShippingAddress(BaseModel):
    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str


class OrderInfo(BaseModel):
    name: str | None = None
    phone_number: str | None = None
    email: str | None = None
    shipping_address: ShippingAddress | None = None


class SuccessfulPayment(BaseModel):
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: str | None = None
    order_info: OrderInfo | None = None
    telegram_payment_charge_id: str
    provider_payment_charge_id: str


class RefundedPayment(BaseModel):
    currency: str
    total_amount: int
    invoice_payload: str
    telegram_payment_charge_id: str
    provider_payment_charge_id: str | None = None


class SharedUser(BaseModel):
    user_id: int
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    photo: list[PhotoSize] | None = None


class UsersShared(BaseModel):
    request_id: int
    users: list[SharedUser]


class ChatShared(BaseModel):
    request_id: int
    chat_id: int
    title: str | None = None
    username: str | None = None
    photo: list[PhotoSize] | None = None


class WriteAccessAllowed(BaseModel):
    from_request: bool | None = None
    web_app_name: str | None = None
    from_attachment_menu: bool | None = None


class PassportFile(BaseModel):
    file_id: str
    file_unique_id: str
    file_size: int
    file_date: int


class EncryptedPassportElement(BaseModel):
    type: Literal[
        "personal_details",
        "passport",
        "driver_license",
        "identity_card",
        "internal_passport",
        "address",
        "utility_bill",
        "bank_statement",
        "rental_agreement",
        "passport_registration",
        "temporary_registration",
        "phone_number",
        "email",
    ]
    data: str | None = None
    phone_number: str | None = None
    email: str | None = None
    files: list[PassportFile] | None = None
    front_side: PassportFile | None = None
    reverse_side: PassportFile | None = None
    selfie: PassportFile | None = None
    translation: list[PassportFile] | None = None
    hash: str


class EncryptedCredentials(BaseModel):
    data: str
    hash: str
    secret: str


class PassportData(BaseModel):
    data: list[EncryptedPassportElement]
    credentials: EncryptedCredentials


class ProximityAlertTriggered(BaseModel):
    traveler: User
    watcher: User
    distance: int


class ChatBoostAdded(BaseModel):
    boost_count: int


class BackgroundFillSolid(BaseModel):
    type: Literal["solid"] = "solid"
    color: int


class BackgroundFillGradient(BaseModel):
    type: Literal["gradient"] = "gradient"
    top_color: int
    bottom_color: int
    rotation_angle: int


class BackgroundFillFreeformGradient(BaseModel):
    type: Literal["freeform_gradient"] = "freeform_gradient"
    colors: list[int]


BackgroundFill = Union[
    BackgroundFillSolid, BackgroundFillGradient, BackgroundFillFreeformGradient
]


class BackgroundTypeFill(BaseModel):
    type: Literal["fill"] = "fill"
    fill: BackgroundFill
    dark_theme_dimming: int


class BackgroundTypeWallpaper(BaseModel):
    type: Literal["wallpaper"] = "wallpaper"
    document: Document
    dark_theme_dimming: int
    is_blurred: Literal[True] | None = None
    is_moving: Literal[True] | None = None


class BackgroundTypePattern(BaseModel):
    type: Literal["pattern"] = "pattern"
    document: Document
    fill: BackgroundFill
    intensity: int
    is_inverted: Literal[True] | None = None
    is_moving: Literal[True] | None = None


class BackgroundTypeChatTheme(BaseModel):
    type: Literal["chat_theme"] = "chat_theme"
    theme_name: str


BackgroundType = Union[
    BackgroundTypeFill,
    BackgroundTypeWallpaper,
    BackgroundTypePattern,
    BackgroundTypeChatTheme,
]


class ChatBackground(BaseModel):
    type: BackgroundType


class ForumTopicCreated(BaseModel):
    name: str
    icon_color: int
    icon_custom_emoji_id: str | None = None


class ForumTopicEdited(BaseModel):
    name: str | None = None
    icon_custom_emoji_id: str | None = None


class ForumTopicClosed(BaseModel):
    pass


class ForumTopicReopened(BaseModel):
    pass


class GeneralForumTopicHidden(BaseModel):
    pass


class GeneralForumTopicUnhidden(BaseModel):
    pass


class GiveawayCreated(BaseModel):
    prize_star_count: int | None = None


class GiveawayCompleted(BaseModel):
    winner_count: int
    unclaimed_prize_count: int | None = None
    giveaway_message: Optional["Message"] = None
    is_star_giveaway: Literal[True] | None = None


class VideoChatScheduled(BaseModel):
    start_date: int


class VideoChatStarted(BaseModel):
    pass


class VideoChatEnded(BaseModel):
    duration: int


class VideoChatParticipantsInvited(BaseModel):
    users: list[User]


class WebAppData(BaseModel):
    data: str
    button_text: str


class WebAppInfo(BaseModel):
    url: str


class LoginUrl(BaseModel):
    url: str
    forward_text: str | None = None
    bot_username: str | None = None
    request_write_access: bool | None = None


class SwitchInlineQueryChosenChat(BaseModel):
    query: str | None = None
    allow_user_chats: bool | None = None
    allow_bot_chats: bool | None = None
    allow_group_chats: bool | None = None
    allow_channel_chats: bool | None = None


class CopyTextButton(BaseModel):
    text: str


class CallbackGame(BaseModel):
    pass


class InlineKeyboardButton(BaseModel):
    text: str
    url: str | None = None
    callback_data: str | None = None
    web_app: WebAppInfo | None = None
    login_url: LoginUrl | None = None
    switch_inline_query: str | None = None
    switch_inline_query_current_chat: str | None = None
    switch_inline_query_chosen_chat: SwitchInlineQueryChosenChat | None = None
    copy_text: CopyTextButton | None = None
    callback_game: CallbackGame | None = None
    pay: bool | None = None


class InlineKeyboardMarkup(BaseModel):
    inline_keyboard: list[list[InlineKeyboardButton]]


class Message(BaseModel):
    message_id: int
    message_thread_id: int | None = None
    from_: User | None = Field(default=None, alias="from")
    sender_chat: Chat | None = None
    sender_boost_count: int | None = None
    sender_business_bot: User | None = None
    date: int
    business_connection_id: str | None = None
    chat: Chat
    forward_origin: MessageOrigin | None = None
    is_topic_message: Literal[True] | None = None
    is_automatic_forward: Literal[True] | None = None
    reply_to_message: Optional["Message"] = None
    external_reply: ExternalReplyInfo | None = None
    quote: TextQuote | None = None
    reply_to_story: Story | None = None
    via_bot: User | None = None
    edit_date: int | None = None
    has_protected_content: Literal[True] | None = None
    is_from_offline: Literal[True] | None = None
    media_group_id: str | None = None
    author_signature: str | None = None
    text: str | None = None
    entities: list[MessageEntity] | None = None
    link_preview_options: LinkPreviewOptions | None = None
    effect_id: str | None = None
    animation: Animation | None = None
    audio: Audio | None = None
    document: Document | None = None
    paid_media: PaidMediaInfo | None = None
    photo: list[PhotoSize] | None = None
    sticker: Sticker | None = None
    story: Story | None = None
    video: Video | None = None
    video_note: VideoNote | None = None
    voice: Voice | None = None
    caption: str | None = None
    caption_entities: list[MessageEntity] | None = None
    show_caption_above_media: Literal[True] | None = None
    has_media_spoiler: Literal[True] | None = None
    contact: Contact | None = None
    dice: Dice | None = None
    game: Game | None = None
    poll: Poll | None = None
    venue: Venue | None = None
    location: Location | None = None
    new_chat_members: list[User] | None = None
    left_chat_member: User | None = None
    new_chat_title: str | None = None
    new_chat_photo: list[PhotoSize] | None = None
    delete_chat_photo: Literal[True] | None = None
    group_chat_created: Literal[True] | None = None
    supergroup_chat_created: Literal[True] | None = None
    channel_chat_created: Literal[True] | None = None
    message_auto_delete_timer_changed: MessageAutoDeleteTimerChanged | None = None
    migrate_to_chat_id: int | None = None
    migrate_from_chat_id: int | None = None
    pinned_message: MaybeInaccessibleMessage | None = None
    invoice: Invoice | None = None
    successful_payment: SuccessfulPayment | None = None
    refunded_payment: RefundedPayment | None = None
    users_shared: UsersShared | None = None
    chat_shared: ChatShared | None = None
    connected_website: str | None = None
    write_access_allowed: WriteAccessAllowed | None = None
    passport_data: PassportData | None = None
    proximity_alert_triggered: ProximityAlertTriggered | None = None
    boost_added: ChatBoostAdded | None = None
    chat_background_set: ChatBackground | None = None
    forum_topic_created: ForumTopicCreated | None = None
    forum_topic_edited: ForumTopicEdited | None = None
    forum_topic_closed: ForumTopicClosed | None = None
    forum_topic_reopened: ForumTopicReopened | None = None
    general_forum_topic_hidden: GeneralForumTopicHidden | None = None
    general_forum_topic_unhidden: GeneralForumTopicUnhidden | None = None
    giveaway_created: GiveawayCreated | None = None
    giveaway: Giveaway | None = None
    giveaway_winners: GiveawayWinners | None = None
    giveaway_completed: GiveawayCompleted | None = None
    video_chat_scheduled: VideoChatScheduled | None = None
    video_chat_started: VideoChatStarted | None = None
    video_chat_ended: VideoChatEnded | None = None
    video_chat_participants_invited: VideoChatParticipantsInvited | None = None
    web_app_data: WebAppData | None = None
    reply_markup: InlineKeyboardMarkup | None = None


class BusinessConnection(BaseModel):
    id: str
    user: User
    user_chat_id: int
    date: int
    can_reply: bool
    is_enabled: bool


class BusinessMessagesDeleted(BaseModel):
    business_connection_id: str
    chat: Chat
    message_ids: list[int]


class ReactionTypeEmoji(BaseModel):
    type: Literal["emoji"] = "emoji"
    emoji: str


class ReactionTypeCustomEmoji(BaseModel):
    type: Literal["custom_emoji"] = "custom_emoji"
    custom_emoji_id: str


class ReactionTypePaid(BaseModel):
    type: str


ReactionType = Union[ReactionTypeEmoji, ReactionTypeCustomEmoji, ReactionTypePaid]


class MessageReactionUpdated(BaseModel):
    chat: Chat
    message_id: int
    user: User | None = None
    actor_chat: Chat | None = None
    date: int
    old_reaction: list[ReactionType]
    new_reaction: list[ReactionType]


class ReactionCount(BaseModel):
    type: ReactionType
    total_count: int


class MessageReactionCountUpdated(BaseModel):
    chat: Chat
    message_id: int
    date: int
    reactions: list[ReactionCount]


class InlineQuery(BaseModel):
    id: str
    from_: User = Field(alias="from")
    query: str
    offset: str
    chat_type: Literal["sender", "private", "group", "supergroup", "channel"] | None = (
        None
    )
    location: Location | None = None


class ChosenInlineResult(BaseModel):
    result_id: str
    from_: User = Field(alias="from")
    location: Location | None = None
    inline_message_id: str | None = None
    query: str


class CallbackQuery(BaseModel):
    id: str
    from_: User = Field(alias="from")
    message: MaybeInaccessibleMessage | None = None
    inline_message_id: str | None = None
    chat_instance: str
    data: str | None = None
    game_short_name: str | None = None


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
    shipping_option_id: str | None = None
    order_info: OrderInfo | None = None


class PaidMediaPurchased(BaseModel):
    from_: User = Field(alias="from")
    paid_media_payload: str


class PollAnswer(BaseModel):
    poll_id: str
    voter_chat: Chat | None = None
    user: User | None = None
    option_ids: list[int]


class ChatMemberOwner(BaseModel):
    status: Literal["creator"] = "creator"
    user: User
    is_anonymous: bool
    custom_title: str | None = None


class ChatMemberAdministrator(BaseModel):
    status: Literal["administrator"] = "administrator"
    user: User
    can_be_edited: bool
    is_anonymous: bool
    can_manage_chat: bool
    can_delete_messages: bool
    can_manage_video_chats: bool
    can_restrict_members: bool
    can_promote_members: bool
    can_change_info: bool
    can_invite_users: bool
    can_post_stories: bool
    can_edit_stories: bool
    can_delete_stories: bool
    can_post_messages: bool | None = None
    can_edit_messages: bool | None = None
    can_pin_messages: bool | None = None
    can_manage_topics: bool | None = None
    custom_title: str | None = None


class ChatMemberMember(BaseModel):
    status: Literal["member"] = "member"
    user: User
    until_date: int | None = None


class ChatMemberRestricted(BaseModel):
    status: Literal["restricted"] = "restricted"
    user: User
    is_member: bool
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
    can_change_info: bool
    can_invite_users: bool
    can_pin_messages: bool
    can_manage_topics: bool
    until_date: int


class ChatMemberLeft(BaseModel):
    status: Literal["left"] = "left"
    user: User


class ChatMemberBanned(BaseModel):
    status: Literal["kicked"] = "kicked"
    user: User
    until_date: int


ChatMember = Union[
    ChatMemberOwner,
    ChatMemberAdministrator,
    ChatMemberMember,
    ChatMemberRestricted,
    ChatMemberLeft,
    ChatMemberBanned,
]


class ChatInviteLink(BaseModel):
    invite_link: str
    creator: User
    creates_join_request: bool
    is_primary: bool
    is_revoked: bool
    name: str | None = None
    expire_date: int | None = None
    member_limit: int | None = None
    pending_join_request_count: int | None = None
    subscription_period: int | None = None
    subscription_price: int | None = None


class ChatMemberUpdated(BaseModel):
    chat: Chat
    from_: User = Field(alias="from")
    date: int
    old_chat_member: ChatMember
    new_chat_member: ChatMember
    invite_link: ChatInviteLink | None = None
    via_join_request: bool | None = None
    via_chat_folder_invite_link: bool | None = None


class ChatJoinRequest(BaseModel):
    chat: Chat
    from_: User = Field(alias="from")
    user_chat_id: int
    date: int
    bio: str | None = None
    invite_link: ChatInviteLink | None = None


class ChatBoostSourcePremium(BaseModel):
    source: Literal["premium"] = "premium"
    user: User


class ChatBoostSourceGiftCode(BaseModel):
    source: Literal["gift_code"] = "gift_code"
    user: User


class ChatBoostSourceGiveaway(BaseModel):
    source: Literal["giveaway"] = "giveaway"
    giveaway_message_id: int
    user: User | None = None
    prize_star_count: int | None = None
    is_unclaimed: Literal[True] | None = None


ChatBoostSource = Union[
    ChatBoostSourcePremium, ChatBoostSourceGiftCode, ChatBoostSourceGiveaway
]


class ChatBoost(BaseModel):
    boost_id: str
    add_date: int
    expiration_date: int
    source: ChatBoostSource


class ChatBoostUpdated(BaseModel):
    chat: Chat
    boost: ChatBoost


class ChatBoostRemoved(BaseModel):
    chat: Chat
    boost_id: str
    remove_date: int
    source: ChatBoostSource


class Update(BaseModel):
    update_id: int
    message: Message | None = None
    edited_message: Message | None = None
    channel_post: Message | None = None
    edited_channel_post: Message | None = None
    business_connection: BusinessConnection | None = None
    business_message: Message | None = None
    edited_business_message: Message | None = None
    deleted_business_messages: BusinessMessagesDeleted | None = None
    message_reaction: MessageReactionUpdated | None = None
    message_reaction_count: MessageReactionCountUpdated | None = None
    inline_query: InlineQuery | None = None
    chosen_inline_result: ChosenInlineResult | None = None
    callback_query: CallbackQuery | None = None
    shipping_query: ShippingQuery | None = None
    pre_checkout_query: PreCheckoutQuery | None = None
    purchased_paid_media: PaidMediaPurchased | None = None
    poll: Poll | None = None
    poll_answer: PollAnswer | None = None
    my_chat_member: ChatMemberUpdated | None = None
    chat_member: ChatMemberUpdated | None = None
    chat_join_request: ChatJoinRequest | None = None
    chat_boost: ChatBoostUpdated | None = None
    removed_chat_boost: ChatBoostRemoved | None = None


class WebhookInfo(BaseModel):
    url: str
    has_custom_certificate: bool
    pending_update_count: int
    ip_address: str | None = None
    last_error_date: int | None = None
    last_error_message: str | None = None
    last_synchronization_error_date: int | None = None
    max_connections: int | None = None
    allowed_updates: list[str] | None = None


class ChatPhoto(BaseModel):
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str


class Birthdate(BaseModel):
    day: int
    month: int
    year: int | None = None


class BusinessIntro(BaseModel):
    title: str | None = None
    message: str | None = None
    sticker: Sticker | None = None


class BusinessLocation(BaseModel):
    address: str
    location: Location | None = None


class BusinessOpeningHoursInterval(BaseModel):
    opening_minute: int
    closing_minute: int


class BusinessOpeningHours(BaseModel):
    time_zone_name: str
    opening_hours: list[BusinessOpeningHoursInterval]


class ChatPermissions(BaseModel):
    can_send_messages: bool | None = None
    can_send_audios: bool | None = None
    can_send_documents: bool | None = None
    can_send_photos: bool | None = None
    can_send_videos: bool | None = None
    can_send_video_notes: bool | None = None
    can_send_voice_notes: bool | None = None
    can_send_polls: bool | None = None
    can_send_other_messages: bool | None = None
    can_add_web_page_previews: bool | None = None
    can_change_info: bool | None = None
    can_invite_users: bool | None = None
    can_pin_messages: bool | None = None
    can_manage_topics: bool | None = None


class ChatLocation(BaseModel):
    location: Location
    address: str


class ChatFullInfo(BaseModel):
    id: int
    type: Literal["private", "group", "supergroup", "channel"]
    title: str | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_forum: Literal[True] | None = None
    accent_color_id: int
    max_reaction_count: int
    photo: ChatPhoto | None = None
    active_usernames: list[str] | None = None
    birthdate: Birthdate | None = None
    business_intro: BusinessIntro | None = None
    business_location: BusinessLocation | None = None
    business_opening_hours: BusinessOpeningHours | None = None
    personal_chat: Chat | None = None
    available_reactions: list[ReactionType] | None = None
    background_custom_emoji_id: str | None = None
    profile_accent_color_id: int | None = None
    profile_background_custom_emoji_id: str | None = None
    emoji_status_custom_emoji_id: str | None = None
    emoji_status_expiration_date: int | None = None
    bio: str | None = None
    has_private_forwards: Literal[True] | None = None
    has_restricted_voice_and_video_messages: Literal[True] | None = None
    join_to_send_messages: Literal[True] | None = None
    join_by_request: Literal[True] | None = None
    description: str | None = None
    invite_link: str | None = None
    pinned_message: Optional["Message"] = None
    permissions: ChatPermissions | None = None
    can_send_paid_media: Literal[True] | None = None
    slow_mode_delay: int | None = None
    unrestrict_boost_count: int | None = None
    message_auto_delete_time: int | None = None
    has_aggressive_anti_spam_enabled: Literal[True] | None = None
    has_hidden_members: Literal[True] | None = None
    has_protected_content: Literal[True] | None = None
    has_visible_history: Literal[True] | None = None
    sticker_set_name: str | None = None
    can_set_sticker_set: Literal[True] | None = None
    custom_emoji_sticker_set_name: str | None = None
    linked_chat_id: int | None = None
    location: ChatLocation | None = None


class MessageId(BaseModel):
    message_id: int


class ReplyParameters(BaseModel):
    message_id: int
    chat_id: int | str | None = None
    allow_sending_without_reply: bool | None = None
    quote: str | None = None
    quote_parse_mode: Literal["MarkdownV2", "HTML"] | None = None
    quote_entities: list[MessageEntity] | None = None
    quote_position: int | None = None


class InputPollOption(BaseModel):
    text: str
    text_parse_mode: str | None = None
    text_entities: list[MessageEntity] | None = None


class UserProfilePhotos(BaseModel):
    total_count: int
    photos: list[list[PhotoSize]]


class KeyboardButtonRequestUsers(BaseModel):
    request_id: int
    user_is_bot: bool | None = None
    user_is_premium: bool | None = None
    max_quantity: int | None = None
    request_name: bool | None = None
    request_username: bool | None = None
    request_photo: bool | None = None


class ChatAdministratorRights(BaseModel):
    is_anonymous: bool
    can_manage_chat: bool
    can_delete_messages: bool
    can_manage_video_chats: bool
    can_restrict_members: bool
    can_promote_members: bool
    can_change_info: bool
    can_invite_users: bool
    can_post_stories: bool
    can_edit_stories: bool
    can_delete_stories: bool
    can_post_messages: bool | None = None
    can_edit_messages: bool | None = None
    can_pin_messages: bool | None = None
    can_manage_topics: bool | None = None


class KeyboardButtonRequestChat(BaseModel):
    request_id: int
    chat_is_channel: bool
    chat_is_forum: bool | None = None
    chat_has_username: bool | None = None
    chat_is_created: bool | None = None
    user_administrator_rights: ChatAdministratorRights | None = None
    bot_administrator_rights: ChatAdministratorRights | None = None
    bot_is_member: bool | None = None
    request_title: bool | None = None
    request_username: bool | None = None
    request_photo: bool | None = None


class KeyboardButtonPollType(BaseModel):
    type: str | None = None


class KeyboardButton(BaseModel):
    text: str
    request_users: KeyboardButtonRequestUsers | None = None
    request_chat: KeyboardButtonRequestChat | None = None
    request_contact: bool | None = None
    request_location: bool | None = None
    request_poll: KeyboardButtonPollType | None = None
    web_app: WebAppInfo | None = None


class ReplyKeyboardMarkup(BaseModel):
    keyboard: list[list[KeyboardButton]]
    is_persistent: bool | None = None
    resize_keyboard: bool | None = None
    one_time_keyboard: bool | None = None
    input_field_placeholder: str | None = None
    selective: bool | None = None


class ReplyKeyboardRemove(BaseModel):
    remove_keyboard: Literal[True]
    selective: bool | None = None


class ForceReply(BaseModel):
    force_reply: Literal[True]
    input_field_placeholder: str | None = None
    selective: bool | None = None


class ForumTopic(BaseModel):
    message_thread_id: int
    name: str
    icon_color: int
    icon_custom_emoji_id: str | None = None


class BotCommand(BaseModel):
    command: str
    description: str


class BotCommandScopeDefault(BaseModel):
    type: Literal["default"] = "default"


class BotCommandScopeAllPrivateChats(BaseModel):
    type: Literal["all_private_chats"] = "all_private_chats"


class BotCommandScopeAllGroupChats(BaseModel):
    type: Literal["all_group_chats"] = "all_group_chats"


class BotCommandScopeAllChatAdministrators(BaseModel):
    type: Literal["all_chat_administrators"] = "all_chat_administrators"


class BotCommandScopeChat(BaseModel):
    type: Literal["chat"] = "chat"
    chat_id: int | str


class BotCommandScopeChatAdministrators(BaseModel):
    type: Literal["chat_administrators"] = "chat_administrators"
    chat_id: int | str


class BotCommandScopeChatMember(BaseModel):
    type: Literal["chat_member"] = "chat_member"
    chat_id: int | str
    user_id: int


BotCommandScope = Union[
    BotCommandScopeDefault,
    BotCommandScopeAllPrivateChats,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllChatAdministrators,
    BotCommandScopeChat,
    BotCommandScopeChatAdministrators,
    BotCommandScopeChatMember,
]


class BotName(BaseModel):
    name: str


class BotDescription(BaseModel):
    description: str


class BotShortDescription(BaseModel):
    short_description: str


class MenuButtonCommands(BaseModel):
    type: Literal["commands"] = "commands"


class MenuButtonWebApp(BaseModel):
    type: Literal["web_app"] = "web_app"
    text: str
    web_app: WebAppInfo


class MenuButtonDefault(BaseModel):
    type: Literal["default"] = "default"


MenuButton = Union[MenuButtonCommands, MenuButtonWebApp, MenuButtonDefault]


class UserChatBoosts(BaseModel):
    boosts: list[ChatBoost]


class ResponseParameters(BaseModel):
    migrate_to_chat_id: int | None = None
    retry_after: int | None = None


InputFile = Union[bytes, tuple[str, bytes]]


class InputMediaAnimation(BaseModel):
    type: Literal["animation"] = "animation"
    media: str | InputFile
    thumbnail: str | InputFile | None = None
    caption: str | None = None
    parse_mode: Literal["MarkdownV2", "Markdown" "HTML"] | None = None
    caption_entities: list[MessageEntity] | None = None
    width: int | None = None
    height: int | None = None
    duration: int | None = None
    has_spoiler: bool | None = None


class InputMediaDocument(BaseModel):
    type: Literal["document"] = "document"
    media: str | InputFile
    thumbnail: str | InputFile | None = None
    caption: str | None = None
    parse_mode: Literal["MarkdownV2", "Markdown" "HTML"] | None = None
    caption_entities: list[MessageEntity] | None = None
    disable_content_type_detection: bool | None = None


class InputMediaAudio(BaseModel):
    type: Literal["audio"] = "audio"
    media: str | InputFile
    thumbnail: str | InputFile | None = None
    caption: str | None = None
    parse_mode: Literal["MarkdownV2", "Markdown" "HTML"] | None = None
    caption_entities: list[MessageEntity] | None = None
    duration: int | None = None
    performer: str | None = None
    title: str | None = None


class InputMediaPhoto(BaseModel):
    type: Literal["photo"] = "photo"
    media: str | InputFile
    caption: str | None = None
    parse_mode: Literal["MarkdownV2", "Markdown" "HTML"] | None = None
    caption_entities: list[MessageEntity] | None = None
    show_caption_above_media: bool | None = None
    has_spoiler: bool | None = None


class InputMediaVideo(BaseModel):
    type: Literal["video"] = "video"
    media: str | InputFile
    thumbnail: str | InputFile | None = None
    caption: str | None = None
    parse_mode: Literal["MarkdownV2", "Markdown" "HTML"] | None = None
    caption_entities: list[MessageEntity] | None = None
    show_caption_above_media: bool | None = None
    width: int | None = None
    height: int | None = None
    duration: int | None = None
    supports_streaming: bool | None = None
    has_spoiler: bool | None = None


InputMedia = Union[
    InputMediaAnimation,
    InputMediaDocument,
    InputMediaAudio,
    InputMediaPhoto,
    InputMediaVideo,
]


class InputPaidMediaPhoto(BaseModel):
    type: Literal["photo"] = "photo"
    media: str | InputFile


class InputPaidMediaVideo(BaseModel):
    type: Literal["video"] = "video"
    media: str | InputFile
    thumbnail: str | InputFile | None = None
    width: int | None = None
    height: int | None = None
    duration: int | None = None
    supports_streaming: bool | None = None


InputPaidMedia = Union[InputPaidMediaPhoto, InputPaidMediaVideo]


class StickerSet(BaseModel):
    name: str
    title: str
    sticker_type: Literal["regular", "mask", "custom_emoji"]
    stickers: list[Sticker]
    thumbnail: PhotoSize | None = None


class InputSticker(BaseModel):
    sticker: str | InputFile
    format: Literal["static", "animated", "video"]
    emoji_list: list[str]
    mask_position: MaskPosition | None = None
    keywords: list[str] | None = None


class InlineQueryResultsButton(BaseModel):
    text: str
    web_app: WebAppInfo | None = None
    start_parameter: str | None = None


class InputTextMessageContent(BaseModel):
    message_text: str
    parse_mode: Literal["MarkdownV2", "Markdown" "HTML"] | None = None
    entities: list[MessageEntity] | None = None
    link_preview_options: LinkPreviewOptions | None = None


class InputLocationMessageContent(BaseModel):
    latitude: float
    longitude: float
    horizontal_accuracy: float | None = None
    live_period: int | None = None
    heading: int | None = None
    proximity_alert_radius: int | None = None


class InputVenueMessageContent(BaseModel):
    latitude: float
    longitude: float
    title: str
    address: str
    foursquare_id: str | None = None
    foursquare_type: str | None = None
    google_place_id: str | None = None
    google_place_type: str | None = None


class InputContactMessageContent(BaseModel):
    phone_number: str
    first_name: str
    last_name: str | None = None
    vcard: str | None = None


class LabeledPrice(BaseModel):
    label: str
    amount: int


class InputInvoiceMessageContent(BaseModel):
    title: str
    description: str
    payload: str
    provider_token: str | None = None
    currency: str
    prices: list[LabeledPrice]
    max_tip_amount: int | None = None
    suggested_tip_amounts: list[int] | None = None
    provider_data: str | None = None
    photo_url: str | None = None
    photo_size: int | None = None
    photo_width: int | None = None
    photo_height: int | None = None
    need_name: bool | None = None
    need_phone_number: bool | None = None
    need_email: bool | None = None
    need_shipping_address: bool | None = None
    send_phone_number_to_provider: bool | None = None
    send_email_to_provider: bool | None = None
    is_flexible: bool | None = None


InputMessageContent = Union[
    InputTextMessageContent,
    InputLocationMessageContent,
    InputVenueMessageContent,
    InputContactMessageContent,
    InputInvoiceMessageContent,
]


class InlineQueryResultCachedAudio(BaseModel):
    type: Literal["audio"] = "audio"
    id: str
    audio_file_id: str
    caption: str | None = None
    parse_mode: Literal["MarkdownV2", "Markdown" "HTML"] | None = None
    caption_entities: list[MessageEntity] | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class InlineQueryResultCachedDocument(BaseModel):
    type: Literal["document"] = "document"
    id: str
    title: str
    document_file_id: str
    description: str | None = None
    caption: str | None = None
    parse_mode: Literal["MarkdownV2", "Markdown" "HTML"] | None = None
    caption_entities: list[MessageEntity] | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class InlineQueryResultCachedGif(BaseModel):
    type: Literal["gif"] = "gif"
    id: str
    gif_file_id: str
    title: str | None = None
    caption: str | None = None
    parse_mode: Literal["MarkdownV2", "Markdown" "HTML"] | None = None
    caption_entities: list[MessageEntity] | None = None
    show_caption_above_media: bool | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class InlineQueryResultCachedMpeg4Gif(BaseModel):
    type: Literal["mpeg4_gif"] = "mpeg4_gif"
    id: str
    mpeg4_file_id: str
    title: str | None = None
    caption: str | None = None
    parse_mode: Literal["MarkdownV2", "Markdown" "HTML"] | None = None
    caption_entities: list[MessageEntity] | None = None
    show_caption_above_media: bool | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class InlineQueryResultCachedPhoto(BaseModel):
    type: Literal["photo"] = "photo"
    id: str
    photo_file_id: str
    title: str | None = None
    description: str | None = None
    caption: str | None = None
    parse_mode: Literal["MarkdownV2", "Markdown" "HTML"] | None = None
    caption_entities: list[MessageEntity] | None = None
    show_caption_above_media: bool | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class InlineQueryResultCachedSticker(BaseModel):
    type: Literal["sticker"] = "sticker"
    id: str
    sticker_file_id: str
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class InlineQueryResultCachedVideo(BaseModel):
    type: Literal["video"] = "video"
    id: str
    video_file_id: str
    title: str
    description: str | None = None
    caption: str | None = None
    parse_mode: Literal["MarkdownV2", "Markdown" "HTML"] | None = None
    caption_entities: list[MessageEntity] | None = None
    show_caption_above_media: bool | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class InlineQueryResultCachedVoice(BaseModel):
    type: Literal["voice"] = "voice"
    id: str
    voice_file_id: str
    title: str
    caption: str | None = None
    parse_mode: Literal["MarkdownV2", "Markdown" "HTML"] | None = None
    caption_entities: list[MessageEntity] | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class InlineQueryResultArticle(BaseModel):
    type: Literal["article"] = "article"
    id: str
    title: str
    input_message_content: InputMessageContent
    reply_markup: InlineKeyboardMarkup | None = None
    url: str | None = None
    hide_url: bool | None = None
    description: str | None = None
    thumbnail_url: str | None = None
    thumbnail_width: int | None = None
    thumbnail_height: int | None = None


class InlineQueryResultAudio(BaseModel):
    type: Literal["audio"] = "audio"
    id: str
    audio_url: str
    title: str
    caption: str | None = None
    parse_mode: Literal["MarkdownV2", "Markdown" "HTML"] | None = None
    caption_entities: list[MessageEntity] | None = None
    performer: str | None = None
    audio_duration: int | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class InlineQueryResultContact(BaseModel):
    type: Literal["contact"] = "contact"
    id: str
    phone_number: str
    first_name: str
    last_name: str | None = None
    vcard: str | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None
    thumbnail_url: str | None = None
    thumbnail_width: int | None = None
    thumbnail_height: int | None = None


class InlineQueryResultGame(BaseModel):
    type: Literal["game"] = "game"
    id: str
    game_short_name: str
    reply_markup: InlineKeyboardMarkup | None = None


class InlineQueryResultDocument(BaseModel):
    type: Literal["document"] = "document"
    id: str
    title: str
    caption: str | None = None
    parse_mode: Literal["MarkdownV2", "Markdown" "HTML"] | None = None
    caption_entities: list[MessageEntity] | None = None
    document_url: str
    mime_type: str
    description: str | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None
    thumbnail_url: str | None = None
    thumbnail_width: int | None = None
    thumbnail_height: int | None = None


class InlineQueryResultGif(BaseModel):
    type: Literal["gif"] = "gif"
    id: str
    gif_url: str
    gif_width: int | None = None
    gif_height: int | None = None
    gif_duration: int | None = None
    thumbnail_url: str
    thumbnail_mime_type: str | None = None
    title: str | None = None
    caption: str | None = None
    parse_mode: Literal["MarkdownV2", "Markdown" "HTML"] | None = None
    caption_entities: list[MessageEntity] | None = None
    show_caption_above_media: bool | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class InlineQueryResultLocation(BaseModel):
    type: Literal["location"] = "location"
    id: str
    latitude: float
    longitude: float
    title: str
    horizontal_accuracy: float | None = None
    live_period: int | None = None
    heading: int | None = None
    proximity_alert_radius: int | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None
    thumbnail_url: str | None = None
    thumbnail_width: int | None = None
    thumbnail_height: int | None = None


class InlineQueryResultMpeg4Gif(BaseModel):
    type: Literal["mpeg4_gif"] = "mpeg4_gif"
    id: str
    mpeg4_url: str
    mpeg4_width: int | None = None
    mpeg4_height: int | None = None
    mpeg4_duration: int | None = None
    thumbnail_url: str
    thumbnail_mime_type: str | None = None
    title: str | None = None
    caption: str | None = None
    parse_mode: Literal["MarkdownV2", "Markdown" "HTML"] | None = None
    caption_entities: list[MessageEntity] | None = None
    show_caption_above_media: bool | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class InlineQueryResultPhoto(BaseModel):
    type: Literal["photo"] = "photo"
    id: str
    photo_url: str
    thumbnail_url: str
    photo_width: int | None = None
    photo_height: int | None = None
    title: str | None = None
    description: str | None = None
    caption: str | None = None
    parse_mode: Literal["MarkdownV2", "Markdown" "HTML"] | None = None
    caption_entities: list[MessageEntity] | None = None
    show_caption_above_media: bool | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class InlineQueryResultVenue(BaseModel):
    type: Literal["venue"] = "venue"
    id: str
    latitude: float
    longitude: float
    title: str
    address: str
    foursquare_id: str | None = None
    foursquare_type: str | None = None
    google_place_id: str | None = None
    google_place_type: str | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None
    thumbnail_url: str | None = None
    thumbnail_width: int | None = None
    thumbnail_height: int | None = None


class InlineQueryResultVideo(BaseModel):
    type: Literal["video"] = "video"
    id: str
    video_url: str
    mime_type: str
    thumbnail_url: str
    title: str
    caption: str | None = None
    parse_mode: Literal["MarkdownV2", "Markdown" "HTML"] | None = None
    caption_entities: list[MessageEntity] | None = None
    show_caption_above_media: bool | None = None
    video_width: int | None = None
    video_height: int | None = None
    video_duration: int | None = None
    description: str | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class InlineQueryResultVoice(BaseModel):
    type: Literal["voice"] = "voice"
    id: str
    voice_url: str
    title: str
    caption: str | None = None
    parse_mode: Literal["MarkdownV2", "Markdown" "HTML"] | None = None
    caption_entities: list[MessageEntity] | None = None
    voice_duration: int | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


InlineQueryResult = Union[
    InlineQueryResultCachedAudio,
    InlineQueryResultCachedDocument,
    InlineQueryResultCachedGif,
    InlineQueryResultCachedMpeg4Gif,
    InlineQueryResultCachedPhoto,
    InlineQueryResultCachedSticker,
    InlineQueryResultCachedVideo,
    InlineQueryResultCachedVoice,
    InlineQueryResultArticle,
    InlineQueryResultAudio,
    InlineQueryResultContact,
    InlineQueryResultGame,
    InlineQueryResultDocument,
    InlineQueryResultGif,
    InlineQueryResultLocation,
    InlineQueryResultMpeg4Gif,
    InlineQueryResultPhoto,
    InlineQueryResultVenue,
    InlineQueryResultVideo,
    InlineQueryResultVoice,
]


class SentWebAppMessage(BaseModel):
    inline_message_id: str | None = None


class ShippingOption(BaseModel):
    id: str
    title: str
    prices: list[LabeledPrice]


class RevenueWithdrawalStatePending(BaseModel):
    type: str


class RevenueWithdrawalStateSucceeded(BaseModel):
    type: str
    date: int
    url: str


class RevenueWithdrawalStateFailed(BaseModel):
    type: str


RevenueWithdrawalState = Union[
    RevenueWithdrawalStatePending,
    RevenueWithdrawalStateSucceeded,
    RevenueWithdrawalStateFailed,
]


class TransactionPartnerUser(BaseModel):
    type: str
    user: User
    invoice_payload: str | None = None
    paid_media: list[PaidMedia] | None = None
    paid_media_payload: str | None = None


class TransactionPartnerFragment(BaseModel):
    type: str
    withdrawal_state: RevenueWithdrawalState | None = None


class TransactionPartnerTelegramAds(BaseModel):
    type: str


class TransactionPartnerTelegramApi(BaseModel):
    type: str
    request_count: int


class TransactionPartnerOther(BaseModel):
    type: str


TransactionPartner = Union[
    TransactionPartnerUser,
    TransactionPartnerFragment,
    TransactionPartnerTelegramAds,
    TransactionPartnerTelegramApi,
    TransactionPartnerOther,
]


class StarTransaction(BaseModel):
    id: str
    amount: int
    date: int
    source: TransactionPartner | None = None
    receiver: TransactionPartner | None = None


class StarTransactions(BaseModel):
    transactions: list[StarTransaction]


class PassportElementErrorDataField(BaseModel):
    source: Literal["data"] = "data"
    type: str
    field_name: str
    data_hash: str
    message: str


class PassportElementErrorFrontSide(BaseModel):
    source: Literal["front_side"] = "front_side"
    type: str
    file_hash: str
    message: str


class PassportElementErrorReverseSide(BaseModel):
    source: Literal["reverse_side"] = "reverse_side"
    type: str
    file_hash: str
    message: str


class PassportElementErrorSelfie(BaseModel):
    source: Literal["selfie"] = "selfie"
    type: str
    file_hash: str
    message: str


class PassportElementErrorFile(BaseModel):
    source: Literal["file"] = "file"
    type: str
    file_hash: str
    message: str


class PassportElementErrorFiles(BaseModel):
    source: Literal["files"] = "files"
    type: str
    file_hashes: list[str]
    message: str


class PassportElementErrorTranslationFile(BaseModel):
    source: Literal["translation_file"] = "translation_file"
    type: str
    file_hash: str
    message: str


class PassportElementErrorTranslationFiles(BaseModel):
    source: Literal["translation_files"] = "translation_files"
    type: str
    file_hashes: list[str]
    message: str


class PassportElementErrorUnspecified(BaseModel):
    source: Literal["unspecified"] = "unspecified"
    type: str
    element_hash: str
    message: str


PassportElementError = Union[
    PassportElementErrorDataField,
    PassportElementErrorFrontSide,
    PassportElementErrorReverseSide,
    PassportElementErrorSelfie,
    PassportElementErrorFile,
    PassportElementErrorFiles,
    PassportElementErrorTranslationFile,
    PassportElementErrorTranslationFiles,
    PassportElementErrorUnspecified,
]


class GameHighScore(BaseModel):
    position: int
    user: User
    score: int
