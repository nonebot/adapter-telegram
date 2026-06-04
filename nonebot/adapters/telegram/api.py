from typing import Literal

from .model import (
    File,
    Poll,
    User,
    Update,
    BotName,
    Message,
    Sticker,
    InputFile,
    MessageId,
    BotCommand,
    ChatMember,
    ForceReply,
    ForumTopic,
    InputMedia,
    MenuButton,
    StickerSet,
    WebhookInfo,
    ChatFullInfo,
    InputSticker,
    LabeledPrice,
    MaskPosition,
    ReactionType,
    GameHighScore,
    MessageEntity,
    BotDescription,
    ChatInviteLink,
    InputPaidMedia,
    ShippingOption,
    UserChatBoosts,
    BotCommandScope,
    ChatPermissions,
    InputMediaAudio,
    InputMediaPhoto,
    InputMediaVideo,
    InputPollOption,
    ReplyParameters,
    StarTransaction,
    InlineQueryResult,
    SentWebAppMessage,
    UserProfilePhotos,
    BusinessConnection,
    InputMediaDocument,
    LinkPreviewOptions,
    BotShortDescription,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    PassportElementError,
    ChatAdministratorRights,
    InlineQueryResultsButton,
)


class API:
    async def get_updates(
        self,
        offset: int | None = None,
        limit: int | None = None,
        timeout: int | None = None,
        allowed_updates: list[str] | None = None,
    ) -> list[Update]: ...

    async def set_webhook(
        self,
        url: str,
        certificate: InputFile | None = None,
        ip_address: str | None = None,
        max_connections: int | None = None,
        allowed_updates: list[str] | None = None,
        drop_pending_updates: bool | None = None,
        secret_token: str | None = None,
    ) -> Literal[True]: ...

    async def delete_webhook(
        self, drop_pending_updates: bool | None = None
    ) -> Literal[True]: ...

    async def get_webhook_info(self) -> WebhookInfo: ...

    async def get_me(self) -> User:
        """
        :说明:
          用于测试机器人 Token 的 API
        :返回:
          * ``User``: 机器人本身的 User
        """
        ...

    async def log_out(self) -> Literal[True]: ...

    async def close(self) -> Literal[True]: ...

    async def send_message(
        self,
        chat_id: int | str,
        text: str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        parse_mode: Literal["MarkdownV2", "Markdown", "HTML"] | None = None,
        entities: list[MessageEntity] | None = None,
        link_preview_options: LinkPreviewOptions | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: (
            InlineKeyboardMarkup
            | ReplyKeyboardMarkup
            | ReplyKeyboardRemove
            | ForceReply
            | None
        ) = None,
    ) -> Message: ...

    async def forward_message(
        self,
        chat_id: int | str,
        from_chat_id: int | str,
        message_id: int,
        message_thread_id: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
    ) -> Message: ...

    async def forward_messages(
        self,
        chat_id: int | str,
        from_chat_id: int | str,
        message_ids: list[int],
        message_thread_id: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
    ) -> list[MessageId]: ...

    async def copy_message(
        self,
        chat_id: int | str,
        from_chat_id: int | str,
        message_id: int,
        message_thread_id: int | None = None,
        caption: str | None = None,
        parse_mode: Literal["MarkdownV2", "Markdown", "HTML"] | None = None,
        caption_entities: list[MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: (
            InlineKeyboardMarkup
            | ReplyKeyboardMarkup
            | ReplyKeyboardRemove
            | ForceReply
            | None
        ) = None,
    ) -> MessageId: ...

    async def copy_messages(
        self,
        chat_id: int | str,
        from_chat_id: int | str,
        message_ids: list[int],
        message_thread_id: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        remove_caption: bool | None = None,
    ) -> list[MessageId]: ...

    async def send_photo(
        self,
        chat_id: int | str,
        photo: str | InputFile,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        caption: str | None = None,
        parse_mode: Literal["MarkdownV2", "Markdown", "HTML"] | None = None,
        caption_entities: list[MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        has_spoiler: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: (
            InlineKeyboardMarkup
            | ReplyKeyboardMarkup
            | ReplyKeyboardRemove
            | ForceReply
            | None
        ) = None,
    ) -> Message: ...

    async def send_audio(
        self,
        chat_id: int | str,
        audio: str | InputFile,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        caption: str | None = None,
        parse_mode: Literal["MarkdownV2", "Markdown", "HTML"] | None = None,
        caption_entities: list[MessageEntity] | None = None,
        duration: int | None = None,
        performer: str | None = None,
        title: str | None = None,
        thumbnail: str | InputFile | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: (
            InlineKeyboardMarkup
            | ReplyKeyboardMarkup
            | ReplyKeyboardRemove
            | ForceReply
            | None
        ) = None,
    ) -> Message: ...

    async def send_document(
        self,
        chat_id: int | str,
        document: str | InputFile,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        thumbnail: str | InputFile | None = None,
        caption: str | None = None,
        parse_mode: Literal["MarkdownV2", "Markdown", "HTML"] | None = None,
        caption_entities: list[MessageEntity] | None = None,
        disable_content_type_detection: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: (
            InlineKeyboardMarkup
            | ReplyKeyboardMarkup
            | ReplyKeyboardRemove
            | ForceReply
            | None
        ) = None,
    ) -> Message: ...

    async def send_video(
        self,
        chat_id: int | str,
        video: str | InputFile,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        duration: int | None = None,
        width: int | None = None,
        height: int | None = None,
        thumbnail: str | InputFile | None = None,
        caption: str | None = None,
        parse_mode: Literal["MarkdownV2", "Markdown", "HTML"] | None = None,
        caption_entities: list[MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        has_spoiler: bool | None = None,
        supports_streaming: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: (
            InlineKeyboardMarkup
            | ReplyKeyboardMarkup
            | ReplyKeyboardRemove
            | ForceReply
            | None
        ) = None,
    ) -> Message: ...

    async def send_animation(
        self,
        chat_id: int | str,
        animation: str | InputFile,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        duration: int | None = None,
        width: int | None = None,
        height: int | None = None,
        thumbnail: str | InputFile | None = None,
        caption: str | None = None,
        parse_mode: Literal["MarkdownV2", "Markdown", "HTML"] | None = None,
        caption_entities: list[MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        has_spoiler: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: (
            InlineKeyboardMarkup
            | ReplyKeyboardMarkup
            | ReplyKeyboardRemove
            | ForceReply
            | None
        ) = None,
    ) -> Message: ...

    async def send_voice(
        self,
        chat_id: int | str,
        voice: str | InputFile,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        caption: str | None = None,
        parse_mode: Literal["MarkdownV2", "Markdown", "HTML"] | None = None,
        caption_entities: list[MessageEntity] | None = None,
        duration: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: (
            InlineKeyboardMarkup
            | ReplyKeyboardMarkup
            | ReplyKeyboardRemove
            | ForceReply
            | None
        ) = None,
    ) -> Message: ...

    async def send_video_note(
        self,
        chat_id: int | str,
        video_note: str | InputFile,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        duration: int | None = None,
        length: int | None = None,
        thumbnail: str | InputFile | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: (
            InlineKeyboardMarkup
            | ReplyKeyboardMarkup
            | ReplyKeyboardRemove
            | ForceReply
            | None
        ) = None,
    ) -> Message: ...
    async def send_paid_media(
        self,
        chat_id: int | str,
        star_count: int,
        media: list[InputPaidMedia],
        business_connection_id: str | None = None,
        payload: str | None = None,
        caption: str | None = None,
        parse_mode: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: (
            InlineKeyboardMarkup
            | ReplyKeyboardMarkup
            | ReplyKeyboardRemove
            | ForceReply
            | None
        ) = None,
    ) -> Message: ...

    async def send_media_group(
        self,
        chat_id: int | str,
        media: list[
            InputMediaAudio | InputMediaDocument | InputMediaPhoto | InputMediaVideo
        ],
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
    ) -> list[Message]: ...

    async def send_location(
        self,
        chat_id: int | str,
        latitude: float,
        longitude: float,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        horizontal_accuracy: float | None = None,
        live_period: int | None = None,
        heading: int | None = None,
        proximity_alert_radius: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: (
            InlineKeyboardMarkup
            | ReplyKeyboardMarkup
            | ReplyKeyboardRemove
            | ForceReply
            | None
        ) = None,
    ) -> Message: ...

    async def send_venue(
        self,
        chat_id: int | str,
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        foursquare_id: str | None = None,
        foursquare_type: str | None = None,
        google_place_id: str | None = None,
        google_place_type: str | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: (
            InlineKeyboardMarkup
            | ReplyKeyboardMarkup
            | ReplyKeyboardRemove
            | ForceReply
            | None
        ) = None,
    ) -> Message: ...

    async def send_contact(
        self,
        chat_id: int | str,
        phone_number: str,
        first_name: str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        last_name: str | None = None,
        vcard: str | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: (
            InlineKeyboardMarkup
            | ReplyKeyboardMarkup
            | ReplyKeyboardRemove
            | ForceReply
            | None
        ) = None,
    ) -> Message: ...

    async def send_poll(
        self,
        chat_id: int | str,
        question: str,
        options: list[InputPollOption],
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        question_parse_mode: Literal["MarkdownV2", "Markdown", "HTML"] | None = None,
        question_entities: list[MessageEntity] | None = None,
        is_anonymous: bool | None = None,
        type: Literal["quiz", "regular"] | None = None,
        allows_multiple_answers: bool | None = None,
        correct_option_id: int | None = None,
        explanation: str | None = None,
        explanation_parse_mode: Literal["MarkdownV2", "Markdown", "HTML"] | None = None,
        explanation_entities: list[MessageEntity] | None = None,
        open_period: int | None = None,
        close_date: int | None = None,
        is_closed: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: (
            InlineKeyboardMarkup
            | ReplyKeyboardMarkup
            | ReplyKeyboardRemove
            | ForceReply
            | None
        ) = None,
    ) -> Message: ...

    async def send_dice(
        self,
        chat_id: int | str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        emoji: Literal["🎲", "🎯", "🏀", "⚽", "🎳", "🎰"] | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: (
            InlineKeyboardMarkup
            | ReplyKeyboardMarkup
            | ReplyKeyboardRemove
            | ForceReply
            | None
        ) = None,
    ) -> Message: ...

    async def send_chat_action(
        self,
        chat_id: int | str,
        action: Literal[
            "typing",
            "upload_photo",
            "record_video",
            "upload_video",
            "record_voice",
            "upload_voice",
            "upload_document",
            "choose_sticker",
            "find_location",
            "record_video_note",
            "upload_video_note",
        ],
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
    ) -> Literal[True]: ...

    async def set_message_reaction(
        self,
        chat_id: int | str,
        message_id: int,
        reaction: list[ReactionType] | None = None,
        is_big: bool | None = None,
    ) -> Literal[True]: ...

    async def get_user_profile_photos(
        self, user_id: int, offset: int | None = None, limit: int | None = None
    ) -> UserProfilePhotos: ...

    async def get_file(self, file_id: str) -> File: ...

    async def ban_chat_member(
        self,
        chat_id: int | str,
        user_id: int,
        until_date: int | None = None,
        revoke_messages: bool | None = None,
    ) -> Literal[True]: ...

    async def unban_chat_member(
        self,
        chat_id: int | str,
        user_id: int,
        only_if_banned: bool | None = None,
    ) -> Literal[True]: ...

    async def restrict_chat_member(
        self,
        chat_id: int | str,
        user_id: int,
        permissions: ChatPermissions,
        use_independent_chat_permissions: bool | None = None,
        until_date: int | None = None,
    ) -> Literal[True]: ...

    async def promote_chat_member(
        self,
        chat_id: int | str,
        user_id: int,
        is_anonymous: bool | None = None,
        can_manage_chat: bool | None = None,
        can_delete_messages: bool | None = None,
        can_manage_video_chats: bool | None = None,
        can_restrict_members: bool | None = None,
        can_promote_members: bool | None = None,
        can_change_info: bool | None = None,
        can_invite_users: bool | None = None,
        can_post_stories: bool | None = None,
        can_edit_stories: bool | None = None,
        can_delete_stories: bool | None = None,
        can_post_messages: bool | None = None,
        can_edit_messages: bool | None = None,
        can_pin_messages: bool | None = None,
        can_manage_topics: bool | None = None,
    ) -> Literal[True]: ...

    async def set_chat_administrator_custom_title(
        self, chat_id: int | str, user_id: int, custom_title: str
    ) -> Literal[True]: ...

    async def ban_chat_sender_chat(
        self, chat_id: int | str, sender_chat_id: int
    ) -> Literal[True]: ...

    async def unban_chat_sender_chat(
        self, chat_id: int | str, sender_chat_id: int
    ) -> Literal[True]: ...

    async def set_chat_permissions(
        self,
        chat_id: int | str,
        permissions: ChatPermissions,
        use_independent_chat_permissions: bool | None = None,
    ) -> Literal[True]: ...

    async def export_chat_invite_link(self, chat_id: int | str) -> str: ...

    async def create_chat_invite_link(
        self,
        chat_id: int | str,
        name: str | None = None,
        expire_date: int | None = None,
        member_limit: int | None = None,
        creates_join_request: bool | None = None,
    ) -> ChatInviteLink: ...

    async def edit_chat_invite_link(
        self,
        chat_id: int | str,
        invite_link: str,
        name: str | None = None,
        expire_date: int | None = None,
        member_limit: int | None = None,
        creates_join_request: bool | None = None,
    ) -> ChatInviteLink: ...

    async def create_chat_subscription_invite_link(
        self,
        chat_id: int | str,
        subscription_period: int,
        subscription_price: int,
        name: str | None = None,
    ) -> ChatInviteLink: ...
    async def edit_chat_subscription_invite_link(
        self, chat_id: int | str, invite_link: str, name: str | None = None
    ) -> ChatInviteLink: ...
    async def revoke_chat_invite_link(
        self, chat_id: int | str, invite_link: str
    ) -> ChatInviteLink: ...

    async def approve_chat_join_request(
        self, chat_id: int | str, user_id: int
    ) -> Literal[True]: ...

    async def decline_chat_join_request(
        self, chat_id: int | str, user_id: int
    ) -> Literal[True]: ...

    async def set_chat_photo(
        self, chat_id: int | str, photo: InputFile
    ) -> Literal[True]: ...

    async def delete_chat_photo(self, chat_id: int | str) -> Literal[True]: ...

    async def set_chat_title(self, chat_id: int | str, title: str) -> Literal[True]: ...

    async def set_chat_description(
        self, chat_id: int | str, description: str | None = None
    ) -> Literal[True]: ...

    async def pin_chat_message(
        self,
        chat_id: int | str,
        message_id: int,
        business_connection_id: str | None = None,
        disable_notification: bool | None = None,
    ) -> Literal[True]: ...

    async def unpin_chat_message(
        self,
        chat_id: int | str,
        business_connection_id: str | None = None,
        message_id: int | None = None,
    ) -> Literal[True]: ...

    async def unpin_all_chat_messages(self, chat_id: int | str) -> Literal[True]: ...

    async def leave_chat(self, chat_id: int | str) -> Literal[True]: ...

    async def get_chat(self, chat_id: int | str) -> ChatFullInfo: ...

    async def get_chat_administrators(self, chat_id: int | str) -> list[ChatMember]: ...

    async def get_chat_member_count(self, chat_id: int | str) -> int: ...

    async def get_chat_member(self, chat_id: int | str, user_id: int) -> ChatMember: ...

    async def set_chat_sticker_set(
        self, chat_id: int | str, sticker_set_name: str
    ) -> Literal[True]: ...

    async def delete_chat_sticker_set(self, chat_id: int | str) -> Literal[True]: ...

    async def get_forum_topic_icon_stickers(self) -> list[Sticker]: ...

    async def create_forum_topic(
        self,
        chat_id: int | str,
        name: str,
        icon_color: int | None = None,
        icon_custom_emoji_id: str | None = None,
    ) -> ForumTopic: ...

    async def edit_forum_topic(
        self,
        chat_id: int | str,
        message_thread_id: int,
        name: str | None = None,
        icon_custom_emoji_id: str | None = None,
    ) -> Literal[True]: ...

    async def close_forum_topic(
        self, chat_id: int | str, message_thread_id: int
    ) -> Literal[True]: ...

    async def reopen_forum_topic(
        self, chat_id: int | str, message_thread_id: int
    ) -> Literal[True]: ...

    async def delete_forum_topic(
        self, chat_id: int | str, message_thread_id: int
    ) -> Literal[True]: ...

    async def unpin_all_forum_topic_messages(
        self, chat_id: int | str, message_thread_id: int
    ) -> Literal[True]: ...

    async def edit_general_forum_topic(
        self, chat_id: int | str, name: str
    ) -> Literal[True]: ...

    async def close_general_forum_topic(self, chat_id: int | str) -> Literal[True]: ...

    async def reopen_general_forum_topic(self, chat_id: int | str) -> Literal[True]: ...

    async def hide_general_forum_topic(self, chat_id: int | str) -> Literal[True]: ...

    async def unhide_general_forum_topic(self, chat_id: int | str) -> Literal[True]: ...

    async def unpin_all_general_forum_topic_messages(
        self, chat_id: int | str
    ) -> Literal[True]: ...

    async def answer_callback_query(
        self,
        callback_query_id: str,
        text: str | None = None,
        show_alert: bool | None = None,
        url: str | None = None,
        cache_time: int | None = None,
    ) -> Literal[True]: ...

    async def get_user_chat_boosts(
        self, chat_id: int | str, user_id: int
    ) -> UserChatBoosts: ...
    async def get_business_connection(
        self, business_connection_id: str
    ) -> BusinessConnection: ...

    async def set_my_commands(
        self,
        commands: list[BotCommand],
        scope: BotCommandScope | None = None,
        language_code: str | None = None,
    ) -> Literal[True]: ...

    async def delete_my_commands(
        self,
        scope: BotCommandScope | None = None,
        language_code: str | None = None,
    ) -> Literal[True]: ...

    async def get_my_commands(
        self,
        scope: BotCommandScope | None = None,
        language_code: str | None = None,
    ) -> list[BotCommand]: ...

    async def set_my_name(
        self, name: str | None = None, language_code: str | None = None
    ) -> Literal[True]: ...

    async def get_my_name(self, language_code: str | None = None) -> BotName: ...

    async def set_my_description(
        self, description: str | None = None, language_code: str | None = None
    ) -> Literal[True]: ...

    async def get_my_description(
        self, language_code: str | None = None
    ) -> BotDescription: ...

    async def set_my_short_description(
        self,
        short_description: str | None = None,
        language_code: str | None = None,
    ) -> Literal[True]: ...

    async def get_my_short_description(
        self, language_code: str | None = None
    ) -> BotShortDescription: ...

    async def set_chat_menu_button(
        self, chat_id: int | None = None, menu_button: MenuButton | None = None
    ) -> Literal[True]: ...

    async def get_chat_menu_button(self, chat_id: int | None = None) -> MenuButton: ...

    async def set_my_default_administrator_rights(
        self,
        rights: ChatAdministratorRights | None = None,
        for_channels: bool | None = None,
    ) -> Literal[True]: ...

    async def get_my_default_administrator_rights(
        self, for_channels: bool | None = None
    ) -> ChatAdministratorRights: ...

    async def edit_message_text(
        self,
        text: str,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        parse_mode: Literal["MarkdownV2", "Markdown", "HTML"] | None = None,
        entities: list[MessageEntity] | None = None,
        link_preview_options: LinkPreviewOptions | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | Literal[True]: ...

    async def edit_message_caption(
        self,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        caption: str | None = None,
        parse_mode: Literal["MarkdownV2", "Markdown", "HTML"] | None = None,
        caption_entities: list[MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | Literal[True]: ...

    async def edit_message_media(
        self,
        media: InputMedia,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | Literal[True]: ...

    async def edit_message_live_location(
        self,
        latitude: float,
        longitude: float,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        live_period: int | None = None,
        horizontal_accuracy: float | None = None,
        heading: int | None = None,
        proximity_alert_radius: int | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | Literal[True]: ...

    async def stop_message_live_location(
        self,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | Literal[True]: ...

    async def edit_message_reply_markup(
        self,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | Literal[True]: ...

    async def stop_poll(
        self,
        chat_id: int | str,
        message_id: int,
        business_connection_id: str | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Poll: ...

    async def delete_message(
        self, chat_id: int | str, message_id: int
    ) -> Literal[True]: ...

    async def delete_messages(
        self, chat_id: int | str, message_ids: list[int]
    ) -> Literal[True]: ...

    async def send_sticker(
        self,
        chat_id: int | str,
        sticker: str | InputFile,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        emoji: str | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: (
            InlineKeyboardMarkup
            | ReplyKeyboardMarkup
            | ReplyKeyboardRemove
            | ForceReply
            | None
        ) = None,
    ) -> Message: ...

    async def get_sticker_set(self, name: str) -> StickerSet: ...

    async def get_custom_emoji_stickers(
        self, custom_emoji_ids: list[str]
    ) -> list[Sticker]: ...

    async def upload_sticker_file(
        self,
        user_id: int,
        sticker: InputFile,
        sticker_format: Literal["static", "animated", "video"],
    ) -> File: ...

    async def create_new_sticker_set(
        self,
        user_id: int,
        name: str,
        title: str,
        stickers: list[InputSticker],
        sticker_type: str | None = None,
        needs_repainting: bool | None = None,
    ) -> Literal[True]: ...

    async def add_sticker_to_set(
        self,
        user_id: int,
        name: str,
        sticker: InputSticker,
    ) -> Literal[True]: ...

    async def set_sticker_position_in_set(
        self, sticker: str, position: int
    ) -> Literal[True]: ...

    async def delete_sticker_from_set(self, sticker: str) -> Literal[True]: ...
    async def replace_sticker_in_set(
        self, user_id: int, name: str, old_sticker: str, sticker: InputSticker
    ) -> Literal[True]: ...

    async def set_sticker_emoji_list(
        self, sticker: str, emoji_list: list[str]
    ) -> Literal[True]: ...

    async def set_sticker_keywords(
        self, sticker: str, keywords: list[str] | None = None
    ) -> Literal[True]: ...

    async def set_sticker_mask_position(
        self, sticker: str, mask_position: MaskPosition | None = None
    ) -> Literal[True]: ...

    async def set_sticker_set_title(self, name: str, title: str) -> Literal[True]: ...

    async def set_sticker_set_thumbnail(
        self,
        name: str,
        user_id: int,
        format: Literal["static", "animated", "video"],
        thumbnail: str | InputFile | None = None,
    ) -> Literal[True]: ...

    async def set_custom_emoji_sticker_set_thumbnail(
        self, name: str, custom_emoji_id: str | None = None
    ) -> Literal[True]: ...

    async def delete_sticker_set(self, name: str) -> Literal[True]: ...

    async def answer_inline_query(
        self,
        inline_query_id: str,
        results: list[InlineQueryResult],
        cache_time: int | None = None,
        is_personal: bool | None = None,
        next_offset: str | None = None,
        button: InlineQueryResultsButton | None = None,
    ) -> Literal[True]: ...

    async def answer_web_app_query(
        self, web_app_query_id: str, result: InlineQueryResult
    ) -> SentWebAppMessage: ...

    async def send_invoice(
        self,
        chat_id: int | str,
        title: str,
        description: str,
        payload: str,
        currency: str,
        prices: list[LabeledPrice],
        message_thread_id: int | None = None,
        provider_token: str | None = None,
        max_tip_amount: int | None = None,
        suggested_tip_amounts: list[int] | None = None,
        start_parameter: str | None = None,
        provider_data: str | None = None,
        photo_url: str | None = None,
        photo_size: int | None = None,
        photo_width: int | None = None,
        photo_height: int | None = None,
        need_name: bool | None = None,
        need_phone_number: bool | None = None,
        need_email: bool | None = None,
        need_shipping_address: bool | None = None,
        send_phone_number_to_provider: bool | None = None,
        send_email_to_provider: bool | None = None,
        is_flexible: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message: ...

    async def create_invoice_link(
        self,
        title: str,
        description: str,
        payload: str,
        currency: str,
        prices: list[LabeledPrice],
        provider_token: str | None = None,
        max_tip_amount: int | None = None,
        suggested_tip_amounts: list[int] | None = None,
        provider_data: str | None = None,
        photo_url: str | None = None,
        photo_size: int | None = None,
        photo_width: int | None = None,
        photo_height: int | None = None,
        need_name: bool | None = None,
        need_phone_number: bool | None = None,
        need_email: bool | None = None,
        need_shipping_address: bool | None = None,
        send_phone_number_to_provider: bool | None = None,
        send_email_to_provider: bool | None = None,
        is_flexible: bool | None = None,
    ) -> str: ...

    async def answer_shipping_query(
        self,
        shipping_query_id: str,
        ok: bool,
        shipping_options: list[ShippingOption] | None = None,
        error_message: str | None = None,
    ) -> Literal[True]: ...

    async def answer_pre_checkout_query(
        self, pre_checkout_query_id: str, ok: bool, error_message: str | None = None
    ) -> Literal[True]: ...
    async def get_star_transactions(
        self, offset: int | None = None, limit: int | None = None
    ) -> StarTransaction: ...
    async def refund_star_payment(
        self, user_id: int, telegram_payment_charge_id: str
    ) -> Literal[True]: ...

    async def set_passport_data_errors(
        self, user_id: int, errors: list[PassportElementError]
    ) -> Literal[True]: ...

    async def send_game(
        self,
        chat_id: int,
        game_short_name: str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message: ...

    async def set_game_score(
        self,
        user_id: int,
        score: int,
        force: bool | None = None,
        disable_edit_message: bool | None = None,
        chat_id: int | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
    ) -> Message | Literal[True]: ...

    async def get_game_high_scores(
        self,
        user_id: int,
        chat_id: int | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
    ) -> list[GameHighScore]: ...
