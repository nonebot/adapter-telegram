from typing import Any, Dict, List, Union, Optional, Required

from .model import (
    File,
    Poll,
    User,
    Sticker,
    Message_,
    InputFile,
    MessageId,
    PhotoSize,
    BotCommand,
    ChatMember,
    ForceReply,
    ForumTopic,
    InputMedia,
    MenuButton,
    MaskPosition,
    MessageEntity,
    ChatInviteLink,
    BotCommandScope,
    ChatPermissions,
    UserProfilePhotos,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    BotCommandScopeDefault,
    ChatAdministratorRights,
)


def getMe() -> "User":
    pass


def logOut():
    pass


def close():
    pass


def sendMessage(
    chat_id: Union[str, int],
    message_thread_id: Optional[int],
    text: str,
    parse_mode: Optional[str],
    entities: Optional[List[MessageEntity]],
    disable_web_page_preview: Optional[bool],
    disable_notification: Optional[bool],
    protect_content: Optional[bool],
    reply_to_message_id: Optional[int],
    allow_sending_without_reply: Optional[bool],
    reply_markup: Optional[
        Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
        ]
    ],
) -> "Message_":
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[str, int]): [description]
        message_thread_id (Optional[int]): [description]
        text (str): [description]
        parse_mode (Optional[str]): [description]
        entities (Optional[List[MessageEntity]]): [description]
        disable_web_page_preview (Optional[bool]): [description]
        disable_notification (Optional[bool]): [description]
        protect_content (Optional[bool]): [description]
        reply_to_message_id (Optional[int]): [description]
        allow_sending_without_reply (Optional[bool]): [description]
        reply_markup (Optional[ Union[ InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply ] ]): [description]
    """
    pass


def forwardMessage(
    char_id: Union[int, str],
    message_thread_id: Optional[int],
    form_chat_id: Union[int, str],
    disable_notification: Optional[bool],
    protect_content: Optional[bool],
    message_id: int,
) -> "Message_":
    """[summary]
    
    [description]
    
    Args:
        char_id (Union[int, str]): [description]
        message_thread_id (Optional[int]): [description]
        form_chat_id (Union[int, str]): [description]
        disable_notification (Optional[bool]): [description]
        protect_content (Optional[bool]): [description]
        message_id (int): [description]
    """
    pass


def copyMessage(
    chat_id: Union[int, str],
    message_thread_id: Optional[int],
    from_chat_id: Union[int, str],
    message_id: int,
    caption: Optional[str],
    parse_mode: Optional[str],
    caption_entities: Optional[List[MessageEntity]],
    disable_notification: Optional[bool],
    protect_content: Optional[bool],
    reply_to_message_id: Optional[int],
    allow_sending_without_reply: Optional[bool],
    reply_markup: Optional[
        Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
        ]
    ],
) -> "MessageId":
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
        message_thread_id (Optional[int]): [description]
        from_chat_id (Union[int, str]): [description]
        message_id (int): [description]
        caption (Optional[str]): [description]
        parse_mode (Optional[str]): [description]
        caption_entities (Optional[List[MessageEntity]]): [description]
        disable_notification (Optional[bool]): [description]
        protect_content (Optional[bool]): [description]
        reply_to_message_id (Optional[int]): [description]
        allow_sending_without_reply (Optional[bool]): [description]
        reply_markup (Optional[ Union[ InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply ] ]): [description]
    """
    pass


def sendPhoto(
    chat_id: Union[int, str],
    message_thread_id: Optional[int],
    from_chat_id: Union[int, str],
    message_id: int,
    caption: Optional[str],
    parse_mode: Optional[str],
    caption_entities: Optional[List[MessageEntity]],
    disable_notification: Optional[bool],
    protect_content: Optional[bool],
    reply_to_message_id: Optional[int],
    allow_sending_without_reply: Optional[bool],
    reply_markup: Optional[
        Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
        ]
    ],
) -> "Message_":
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
        message_thread_id (Optional[int]): [description]
        from_chat_id (Union[int, str]): [description]
        message_id (int): [description]
        caption (Optional[str]): [description]
        parse_mode (Optional[str]): [description]
        caption_entities (Optional[List[MessageEntity]]): [description]
        disable_notification (Optional[bool]): [description]
        protect_content (Optional[bool]): [description]
        reply_to_message_id (Optional[int]): [description]
        allow_sending_without_reply (Optional[bool]): [description]
        reply_markup (Optional[ Union[ InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply ] ]): [description]
    """
    pass


# Your audio must be in the .MP3 or .M4A format.
def sendAudio(
    chat_id: Union[int, str],
    message_thread_id: Optional[int],
    audio: Union[InputFile, str],
    caption: Optional[str],
    parse_mod: Optional[str],
    caption_entities: Optional[List[MessageEntity]],
    duration: Optional[int],
    performer: Optional[str],
    title: Optional[str],
    thumb: Optional[Union[InputFile, str]],
    disable_notification: Optional[bool],
    protect_content: Optional[bool],
    reply_to_message_id: Optional[int],
    allow_sending_without_reply: Optional[bool],
    reply_markup: Optional[
        Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
        ]
    ],
) -> "Message_":
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
        message_thread_id (Optional[int]): [description]
        audio (Union[InputFile, str]): [description]
        caption (Optional[str]): [description]
        parse_mod (Optional[str]): [description]
        caption_entities (Optional[List[MessageEntity]]): [description]
        duration (Optional[int]): [description]
        performer (Optional[str]): [description]
        title (Optional[str]): [description]
        thumb (Optional[Union[InputFile, str]]): [description]
        disable_notification (Optional[bool]): [description]
        protect_content (Optional[bool]): [description]
        reply_to_message_id (Optional[int]): [description]
        allow_sending_without_reply (Optional[bool]): [description]
        reply_markup (Optional[ Union[ InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply ] ]): [description]
    """
    pass


def sendDocument():
    pass


def sendVideo():
    pass


def sendVoice():
    pass


def sendAnimation():
    pass


def sendVideoNote():
    pass


def sendMediaGroup():
    pass


def sendLocation():
    pass


def editMessageLiveLocation():
    pass


def stopMessageLiveLocation():
    pass


def sendVenue():
    pass


def sendContact():
    pass


def sendPoll():
    pass


def sendDice():

    pass


def sendChatAction() -> bool:
    pass


def getUserProfilePhotos() -> "UserProfilePhotos":
    pass


def getFile() -> "File":
    pass


def banChatMember():
    pass


def unbanChatMember(
    chat_id: Union[str, int], user_id: int, only_if_banned: Optional[bool]
) -> bool:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[str, int]): [description]
        user_id (int): [description]
        only_if_banned (Optional[bool]): [description]
    """
    pass


def restrictChatMember(
    chat_id: Union[int, str],
    user_id: int,
    permissions: "ChatPermissions",
    until_date: Optional[int],
) -> bool:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
        user_id (int): [description]
        permissions ("ChatPermissions"): [description]
        until_date (Optional[int]): [description]
    """
    pass


def promoteChatMember(
    chat_id: Union[int, str],
    user_id: int,
    is_anonymous: Optional[bool],
    can_manage_chat: Optional[bool],
    can_post_messages: Optional[bool],
    can_edit_messages: Optional[bool],
    can_delete_messages: Optional[bool],
    can_manage_video_chats: Optional[bool],
    can_restrict_members: Optional[bool],
    can_promote_members: Optional[bool],
    can_change_info: Optional[bool],
    can_invite_users: Optional[bool],
    can_pin_messages: Optional[bool],
    can_manage_topics: Optional[bool],
) -> bool:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
        user_id (int): [description]
        is_anonymous (Optional[bool]): [description]
        can_manage_chat (Optional[bool]): [description]
        can_post_messages (Optional[bool]): [description]
        can_edit_messages (Optional[bool]): [description]
        can_delete_messages (Optional[bool]): [description]
        can_manage_video_chats (Optional[bool]): [description]
        can_restrict_members (Optional[bool]): [description]
        can_promote_members (Optional[bool]): [description]
        can_change_info (Optional[bool]): [description]
        can_invite_users (Optional[bool]): [description]
        can_pin_messages (Optional[bool]): [description]
        can_manage_topics (Optional[bool]): [description]
    """
    pass


def setChatAdministratorCustomTitle(
    chat_id: Union[int, str], user_id: int, custom_title: str
) -> bool:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
        user_id (int): [description]
        custom_title (str): [description]
    """
    pass


def banChatSenderChat():

    pass


def unbanChatSenderChat():
    pass


def setChatPermissions():
    pass


def exportChatInviteLink(chat_id: Union[int, str]) -> str:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
    """
    pass


def createChatInviteLink(
    chat_id: Union[int, str],
    name: Optional[str],
    expire_date: Optional[bool],
    member_limit: Optional[bool],
    creates_join_request: Optional[bool],
) -> "ChatInviteLink":
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
        name (Optional[str]): [description]
        expire_date (Optional[bool]): [description]
        member_limit (Optional[bool]): [description]
        creates_join_request (Optional[bool]): [description]
    """
    pass


def editChatInviteLink() -> "ChatInviteLink":
    """[summary]
    
    [description]
    """
    pass


def revokeChatInviteLink(
    chat_id: Union[int, str], invite_link: str
) -> "ChatInviteLink":
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
        invite_link (str): [description]
    """
    pass


def approveChatJoinRequest(
    chat_id: Union[int, str],
    user_id: int,
) -> bool:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
        user_id (int): [description]
    """
    pass


def declineChatJoinRequest(
    chat_id: Union[int, str],
    user_id: int,
) -> bool:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
        user_id (int): [description]
    """
    pass


def setChatPhoto(chat_id: Union[int, str], photo: "InputFile"):
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
        photo ("InputFile"): [description]
    """
    pass


def deleteChatPhoto(
    chat_id: Union[int, str],
) -> bool:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
    """
    pass


def setChatTitle(chat_id: Union[int, str], title: str) -> bool:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
        title (str): [description]
    """
    pass


def setChatDescription(chat_id: Union[int, str], description: Optional[str]) -> bool:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
        description (Optional[str]): [description]
    """
    pass


def pinChatMessage(
    chat_id: Union[int, str], message_id: int, disable_notification: Optional[bool]
):
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
        message_id (int): [description]
        disable_notification (Optional[bool]): [description]
    """
    pass


def unpinAllChatMessages(chat_id: Union[int, str]) -> bool:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
    """
    pass


def leaveChat(chat_id: Union[int, str]) -> bool:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
    """
    pass


def getChat(chat_id: Union[int, str]) -> bool:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
    """
    pass


def getChatAdministrators(chat_id: Union[int, str]) -> List[ChatMember]:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
    """
    pass


def getChatMemberCount(chat_id: Union[int, str]) -> bool:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
    """
    pass


def getChatMember(
    chat_id: Union[int, str],
    user_id: int,
) -> "ChatMember":
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
        user_id (int): [description]
    """
    pass


def setChatStickerSet(chat_id: Union[int, str], sticker_set_name: str) -> bool:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
        sticker_set_name (str): [description]
    """
    pass


def deleteChatStickerSet(
    chat_id: Union[int, str],
) -> bool:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
    """
    pass


def getForumTopicIconStickers() -> List[Sticker]:
    """[summary]
    
    [description]
    """
    pass


def createForumTopic(
    chat_id: Union[int, str],
    name: str,
    icon_color: Optional[int],
    icon_custom_emoji_id: Optional[str],
) -> "ForumTopic":
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
        name (str): [description]
        icon_color (Optional[int]): [description]
        icon_custom_emoji_id (Optional[str]): [description]
    """
    pass


def editForumTopic(
    chat_id: Union[int, str],
    name: str,
    message_thread_id: int,
    icon_custom_emoji_id: str,
) -> bool:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
        name (str): [description]
        message_thread_id (int): [description]
        icon_custom_emoji_id (str): [description]
    """
    pass


def closeForumTopic(
    chat_id: Union[int, str],
    message_thread_id: int,
) -> bool:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
        message_thread_id (int): [description]
    """
    pass


def reopenForumTopic(
    chat_id: Union[int, str],
    message_thread_id: int,
) -> bool:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
        message_thread_id (int): [description]
    """
    pass


def deleteForumTopic(
    chat_id: Union[int, str],
    message_thread_id: int,
) -> bool:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
        message_thread_id (int): [description]
    """
    pass


def unpinAllForumTopicMessages(
    chat_id: Union[int, str],
    message_thread_id: int,
) -> bool:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
        message_thread_id (int): [description]
    """
    pass


def answerCallbackQuery(
    callback_query_id: str,
    text: Optional[str],
    show_alert: Optional[bool],
    url: Optional[str],
    cache_time: Optional[int],
) -> bool:
    """[summary]
    
    [description]
    
    Args:
        callback_query_id (str): [description]
        text (Optional[str]): [description]
        show_alert (Optional[bool]): [description]
        url (Optional[str]): [description]
        cache_time (Optional[int]): [description]
    """
    pass


def setMyCommands(
    commands: List[BotCommand],
    scope: Optional[BotCommandScope],
    language_code: Optional[str],
) -> bool:
    """[summary]
    
    [description]
    
    Args:
        commands (List[BotCommand]): [description]
        scope (Optional[BotCommandScope]): [description]
        language_code (Optional[str]): [description]
    """
    pass


def deleteMyCommands(commands: List[BotCommand], language_code: Optional[str]) -> bool:
    """[summary]
    
    [description]
    
    Args:
        commands (List[BotCommand]): [description]
        language_code (Optional[str]): [description]
    """
    pass


def getMyCommands(
    commands: List[BotCommand], language_code: Optional[str]
) -> List[Union[BotCommand, None]]:
    """[summary]
    
    [description]
    
    Args:
        commands (List[BotCommand]): [description]
        language_code (Optional[str]): [description]
    """
    pass


def getChatMenuButton(
    chat_id: Union[int, str], language_code: Optional[str]
) -> "MenuButton":
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
        language_code (Optional[str]): [description]
    """
    pass


def setMyDefaultAdministratorRights(
    right: Optional[ChatAdministratorRights], for_channels: Optional[bool]
) -> bool:
    """[summary]
    
    [description]
    
    Args:
        right (Optional[ChatAdministratorRights]): [description]
        for_channels (Optional[bool]): [description]
    """
    pass


def getMyDefaultAdministratorRights(
    right: Optional[ChatAdministratorRights], for_channels: Optional[bool]
) -> "ChatAdministratorRights":
    """[summary]
    
    [description]
    
    Args:
        right (Optional[ChatAdministratorRights]): [description]
        for_channels (Optional[bool]): [description]
    """
    pass


def editMessageText(
    chat_id: Union[int, str],
    message_id: Optional[int],
    inline_message_id: Optional[int],
    text: Optional[int],
    parse_mode: Optional[int],
    entities: Optional[List[MessageEntity]],
    disable_web_page_preview: Optional[bool],
    reply_markup: Optional[InlineKeyboardMarkup],
) -> Union[Message_, True]:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
        message_id (Optional[int]): [description]
        inline_message_id (Optional[int]): [description]
        text (Optional[int]): [description]
        parse_mode (Optional[int]): [description]
        entities (Optional[List[MessageEntity]]): [description]
        disable_web_page_preview (Optional[bool]): [description]
        reply_markup (Optional[InlineKeyboardMarkup]): [description]
    """
    pass


def editMessageCaption(
    chat_id: Union[int, str],
    message_id: Optional[int],
    inline_message_id: Optional[int],
    caption: Optional[str],
    parse_mode: Optional[int],
    caption_entities: Optional[List[MessageEntity]],
    reply_markup: Optional[InlineKeyboardMarkup],
) -> Union[Message_, True]:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Union[int, str]): [description]
        message_id (Optional[int]): [description]
        inline_message_id (Optional[int]): [description]
        caption (Optional[str]): [description]
        parse_mode (Optional[int]): [description]
        caption_entities (Optional[List[MessageEntity]]): [description]
        reply_markup (Optional[InlineKeyboardMarkup]): [description]
    """
    pass


def editMessageMedia(
    chat_id: Optional[Union[int, str]],
    message_id: Optional[int],
    inline_message_id: Optional[int],
    media: InputMedia,
    reply_markup: Optional[InlineKeyboardMarkup],
) -> Union[Message_, True]:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Optional[Union[int, str]]): [description]
        message_id (Optional[int]): [description]
        inline_message_id (Optional[int]): [description]
        media (InputMedia): [description]
        reply_markup (Optional[InlineKeyboardMarkup]): [description]
    """
    pass


def editMessageReplyMarkup(
    chat_id: Optional[Union[int, str]],
    message_id: Optional[int],
    inline_message_id: Optional[int],
    reply_markup: Optional[InlineKeyboardMarkup],
) -> Union[Message_, True]:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Optional[Union[int, str]]): [description]
        message_id (Optional[int]): [description]
        inline_message_id (Optional[int]): [description]
        reply_markup (Optional[InlineKeyboardMarkup]): [description]
    """
    pass


def stopPoll(
    chat_id: Optional[Union[int, str]],
    message_id: Optional[int],
    inline_message_id: Optional[int],
    reply_markup: Optional[InlineKeyboardMarkup],
) -> "Poll":
    """[summary]
    
    [description]
    
    Args:
        chat_id (Optional[Union[int, str]]): [description]
        message_id (Optional[int]): [description]
        inline_message_id (Optional[int]): [description]
        reply_markup (Optional[InlineKeyboardMarkup]): [description]
    """
    pass


def deleteMessage(
    chat_id: Optional[Union[int, str]],
    message_id: Optional[int],
) -> bool:
    """[summary]
    
    [description]
    
    Args:
        chat_id (Optional[Union[int, str]]): [description]
        message_id (Optional[int]): [description]
    """
    pass


def sendGame(
    chat_id: int,
    message_thread_id: Optional[int],
    game_short_name: str,
    disable_notification: Optional[bool],
    protect_content: Optional[bool],
    reply_to_message_id: Optional[bool],
    allow_sending_without_reply: Optional[bool],
    reply_markup: Optional[InlineKeyboardMarkup],
) -> "Message_":
    """[summary]
    
    [description]
    
    Args:
        chat_id (int): [description]
        message_thread_id (Optional[int]): [description]
        game_short_name (str): [description]
        disable_notification (Optional[bool]): [description]
        protect_content (Optional[bool]): [description]
        reply_to_message_id (Optional[bool]): [description]
        allow_sending_without_reply (Optional[bool]): [description]
        reply_markup (Optional[InlineKeyboardMarkup]): [description]
    """
    pass
