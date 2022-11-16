from typing import Any, Dict, List, Union, Literal, Optional, Required

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
    """
    A simple method for testing your bot's authentication token.
    Requires no parameters. Returns basic information about the bot in form of a User object.
    """
    pass


def logOut():
    """
    Use this method to log out from the cloud Bot API server before launching the bot locally.
    You must log out the bot before running it locally,
    otherwise there is no guarantee that the bot will receive updates. After a successful call,
    you can immediately log in on a local server,
    but will not be able to log in back to the cloud Bot API server for 10 minutes.
    Returns True on success. Requires no parameters
    """
    pass


def close():
    """
    Use this method to close the bot instance before moving it from one local server to another.
    You need to delete the webhook before calling this method to ensure that the bot isn't launched again after server restart.
    The method will return error 429 in the first 10 minutes after the bot is launched.
    Returns True on success. Requires no parameters.
    """
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

    Use this method to send text messages. On success, the sent `Message` is returned.

    :Params:
        chat_id (Union[str, int]): Unique identifier for the target chat or username of the target channel (in the format `@channelusername`)
        message_thread_id (Optional[int]): Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        text (str): Text of the message to be sent, 1-4096 characters after entities parsing
        parse_mode (Optional[str]): Mode for parsing entities in the message text. See formatting options for more details.
        entities (Optional[List[MessageEntity]]): A JSON-serialized list of special entities that appear in message text, which can be specified instead of `parse_mode`
        disable_web_page_preview (Optional[bool]): Disables link previews for links in this message
        disable_notification (Optional[bool]): Sends the message silently. Users will receive a notification with no sound.
        protect_content (Optional[bool]): Protects the contents of the sent message from forwarding and saving
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
    """

    Use this method to copy messages of any kind. Service messages and invoice messages can't be copied.
    A quiz poll can be copied only if the value of the field correct_option_id is known to the bot.
    The method is analogous to the method forwardMessage,
    but the copied message doesn't have a link to the original message.
    Returns the MessageId of the sent message on success.

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
    """

    Use this method to send photos. On success, the sent Message is returned.

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
    """

    Use this method to send audio files, if you want Telegram clients to display them in the music player.
    Your audio must be in the .MP3 or .M4A format. On success, the sent `Message` is returned.
    Bots can currently send audio files of up to 50 MB in size, this limit may be changed in the future.

    For sending voice messages, use the `sendVoice` method instead.

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
    """
        Use this method to send general files. On success, the sent Message is returned.
        Bots can currently send files of any type of up to 50 MB in size, this limit may be changed in the future.
    :see https://core.telegram.org/bots/api#sendDocument
    """
    pass


def sendVideo():
    """
        Use this method to send video files, Telegram clients support MPEG4 videos (other formats may be sent as Document).
        On success, the sent `Message` is returned.
        Bots can currently send video files of up to 50 MB in size, this limit may be changed in the future.
    :see https://core.telegram.org/bots/api#sendVideo
    """
    pass


def sendVoice():
    """
        Use this method to send audio files, if you want Telegram clients to display the file as a playable voice message. For this to work,
        your audio must be in an .OGG file encoded with OPUS (other formats may be sent as Audio or Document).
        On success, the sent `Message` is returned. Bots can currently send voice messages of up to 50 MB in size,
        this limit may be changed in the future.

    :see https://core.telegram.org/bots/api#sendVoice
    """
    pass


def sendAnimation():
    """
        Use this method to send animation files (GIF or H.264/MPEG-4 AVC video without sound).
        On success, the sent Message is returned.
        Bots can currently send animation files of up to 50 MB in size, this limit may be changed in the future.

    :see https://core.telegram.org/bots/api#sendanimation

    """
    pass


def sendVideoNote():
    """
        As of v.4.0, Telegram clients support rounded square MPEG4 videos of up to 1 minute long.
        Use this method to send video messages. On success, the sent Message is returned.
    :see https://core.telegram.org/bots/api#sendVideoNote
    """
    pass


def sendMediaGroup():
    """
        Use this method to send a group of photos, videos, documents or audios as an album.
        Documents and audio files can be only grouped in an album with messages of the same type.
        On success, an array of Messages that were sent is returned.
    :see https://core.telegram.org/bots/api#sendMediaGroup
    """
    pass


def sendLocation():
    """
        Use this method to send point on the map. On success, the sent Message is returned.
    :see https://core.telegram.org/bots/api#sendLocation
    """
    pass


def editMessageLiveLocation():
    """
        Use this method to edit live location messages.
        A location can be edited until its live_period expires or editing is explicitly disabled by a call to stopMessageLiveLocation.
        On success, if the edited message is not an inline message, the edited `Message` is returned, otherwise True is returned.

    :see https://core.telegram.org/bots/api#editMessageLiveLocation
    """
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


List


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
