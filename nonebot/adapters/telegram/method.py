from typing import (
    Union,
    Dict,
    Optional,
    List,
    Any,
    Required
    
)
from .model import (
    User,
    MessageEntity,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply,
    Message_,
    MessageId,
    InputFile,
    File,
    ChatPermissions,
    UserProfilePhotos,
    ChatInviteLink,
    ChatMember,
    Sticker,
    ForumTopic,
    BotCommand,
    BotCommandScope,
    BotCommandScopeDefault,
    MenuButton,
    ChatAdministratorRights,
    InputMedia,
    Poll
)


def getMe()->'User':
    pass
def logOut():
    pass
def close():
    pass

def sendMessage(
    chat_id:Union[str,int],
    message_thread_id:Optional[int],
    text:str,
    parse_mode:Optional[str],
    entities:Optional[List[MessageEntity]],
    disable_web_page_preview:Optional[bool],
    disable_notification:Optional[bool],
    protect_content:Optional[bool],
    reply_to_message_id:Optional[int],
    allow_sending_without_reply:Optional[bool],
    reply_markup:Optional[Union[InlineKeyboardMarkup,ReplyKeyboardMarkup,ReplyKeyboardRemove,ForceReply]]
)->'Message_':
    """
    """
    pass
def forwardMessage(
    char_id:Union[int,str],
    message_thread_id:Optional[int],
    form_chat_id:Union[int,str],
    disable_notification:Optional[bool],
    protect_content:Optional[bool],
    message_id:int
)->'Message_':
    pass

def copyMessage(
    chat_id:Union[int,str],
    message_thread_id:Optional[int],
    from_chat_id:Union[int,str],
    message_id:int,
    caption:Optional[str],
    parse_mode:Optional[str],
    caption_entities:Optional[List[MessageEntity]],
    disable_notification:Optional[bool],
    protect_content:Optional[bool],
    reply_to_message_id:Optional[int],
    allow_sending_without_reply:Optional[bool],
    reply_markup:Optional[Union[InlineKeyboardMarkup,ReplyKeyboardMarkup,ReplyKeyboardRemove,ForceReply]]
)->'MessageId':
    pass
def sendPhoto(
    chat_id:Union[int,str],
    message_thread_id:Optional[int],
    from_chat_id:Union[int,str],
    message_id:int,
    caption:Optional[str],
    parse_mode:Optional[str],
    caption_entities:Optional[List[MessageEntity]],
    disable_notification:Optional[bool],
    protect_content:Optional[bool],
    reply_to_message_id:Optional[int],
    allow_sending_without_reply:Optional[bool],
    reply_markup:Optional[Union[InlineKeyboardMarkup,ReplyKeyboardMarkup,ReplyKeyboardRemove,ForceReply]]
)->'Message_':
    pass
# Your audio must be in the .MP3 or .M4A format.
def sendAudio(
    chat_id:Union[int,str],
    message_thread_id:Optional[int],
    audio:Union[InputFile,str],
    caption:Optional[str],
    parse_mod:Optional[str],
    caption_entities:Optional[List[MessageEntity]],
    duration:Optional[int],
    performer:Optional[str],
    title:Optional[str],
    thumb:Optional[Union[InputFile,str]],
    disable_notification:Optional[bool],
    protect_content:Optional[bool],
    reply_to_message_id:Optional[int],
    allow_sending_without_reply:Optional[bool],
    reply_markup:Optional[Union[InlineKeyboardMarkup,ReplyKeyboardMarkup,ReplyKeyboardRemove,ForceReply]]
)->'Message_':
    
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
def sendChatAction()->bool:
    pass

def getUserProfilePhotos()->'UserProfilePhotos':
    pass
def getFile()->'File':
    pass
def banChatMember():
    pass
def unbanChatMember(
    chat_id:Union[str,int],
    user_id:int,
    only_if_banned:Optional[bool]
)->bool:
    pass
def restrictChatMember(
    chat_id:Union[int,str],
    user_id:int,
    permissions:'ChatPermissions',
    until_date:Optional[int]
)->bool:
    pass

def promoteChatMember(
    chat_id:Union[int,str],
    user_id:int,
    is_anonymous:Optional[bool],
    can_manage_chat:Optional[bool],
    can_post_messages:Optional[bool],
    can_edit_messages:Optional[bool],
    can_delete_messages:Optional[bool],
    can_manage_video_chats:Optional[bool],
    can_restrict_members:Optional[bool],
    can_promote_members:Optional[bool],
    can_change_info:Optional[bool],
    can_invite_users:Optional[bool],
    can_pin_messages:Optional[bool],
    can_manage_topics:Optional[bool],
)->bool:
    pass
def setChatAdministratorCustomTitle(
    chat_id:Union[int,str],
    user_id:int,
    custom_title:str
)->bool:
    pass
def banChatSenderChat():
    pass
def unbanChatSenderChat():
    pass
def setChatPermissions():
    pass

def exportChatInviteLink(chat_id:Union[int,str])->str:
    pass
def createChatInviteLink(
    chat_id:Union[int,str],
    name:Optional[str],
    expire_date:Optional[bool],
    member_limit:Optional[bool],
    creates_join_request:Optional[bool]
)->'ChatInviteLink':
    pass

def editChatInviteLink()->'ChatInviteLink':
    pass
def revokeChatInviteLink(
    chat_id:Union[int,str],
    invite_link:str
)->'ChatInviteLink':
    pass
def approveChatJoinRequest(
    chat_id:Union[int,str],
    user_id:int,
)->bool:
    pass

def declineChatJoinRequest(
    chat_id:Union[int,str],
    user_id:int,
)->bool:
    pass
def setChatPhoto(
    chat_id:Union[int,str],
    photo:'InputFile'
):
    pass
def deleteChatPhoto(
    chat_id:Union[int,str],
)->bool:
    pass
def setChatTitle(
    chat_id:Union[int,str],
    title:str
)->bool:
    pass

def setChatDescription(
    chat_id:Union[int,str],
    description:Optional[str]
)->bool:
    pass

def pinChatMessage(
    chat_id:Union[int,str],
    message_id:int,
    disable_notification:Optional[bool]
):
    pass
def unpinAllChatMessages(
    chat_id:Union[int,str]
)->bool:
    pass

def leaveChat(
    chat_id:Union[int,str]
)->bool:
    pass

def getChat(
    chat_id:Union[int,str]
)->bool:
    pass

def getChatAdministrators(
    chat_id:Union[int,str]
)->List[ChatMember]:
    pass

def getChatMemberCount(
    chat_id:Union[int,str]
)->bool:
    pass

def getChatMember(
    chat_id:Union[int,str],
    user_id:int,
)->'ChatMember':
    pass
def setChatStickerSet(
    chat_id:Union[int,str],
    sticker_set_name:str
)->bool:
    pass
def deleteChatStickerSet(
    chat_id:Union[int,str],
)->bool:
    pass
def getForumTopicIconStickers(
)->List[Sticker]:
    pass
def createForumTopic(
    chat_id:Union[int,str],
    name:str,
    icon_color:Optional[int],
    icon_custom_emoji_id:Optional[str]
)->'ForumTopic':
    pass

def editForumTopic(
    chat_id:Union[int,str],
    name:str,
    message_thread_id:int,
    icon_custom_emoji_id:str
)->bool:
    pass
def closeForumTopic(
    chat_id:Union[int,str],
    message_thread_id:int,
)->bool:
    pass
def reopenForumTopic(
    chat_id:Union[int,str],
    message_thread_id:int,
)->bool:
    pass
def deleteForumTopic(
    chat_id:Union[int,str],
    message_thread_id:int,
)->bool:
    pass
def unpinAllForumTopicMessages(
    chat_id:Union[int,str],
    message_thread_id:int,
)->bool:
    pass
def answerCallbackQuery(
    callback_query_id:str,
    text:Optional[str],
    show_alert:Optional[bool],
    url:Optional[str],
    cache_time:Optional[int],
)->bool:
    pass
def setMyCommands(
    commands:List[BotCommand],
    scope:Optional[BotCommandScope],
    language_code:Optional[str]
)->bool:
    pass
def deleteMyCommands(
    commands:List[BotCommand],
    language_code:Optional[str]
)->bool:
    pass
def getMyCommands(
    commands:List[BotCommand],
    language_code:Optional[str]
)->List[Union[BotCommand,None]]:
    pass
def getChatMenuButton(
    chat_id:Union[int,str],
    language_code:Optional[str]
)->'MenuButton':
    pass
def setMyDefaultAdministratorRights(
    right:Optional[ChatAdministratorRights],
    for_channels:Optional[bool]
)->bool:
    pass
def getMyDefaultAdministratorRights(
    right:Optional[ChatAdministratorRights],
    for_channels:Optional[bool]
)->'ChatAdministratorRights':
    pass
def editMessageText(
    chat_id:Union[int,str],
    message_id:Optional[int],
    inline_message_id:Optional[int],
    text:Optional[int],
    parse_mode:Optional[int],
    entities:Optional[List[MessageEntity]],
    disable_web_page_preview:Optional[bool],
    reply_markup:Optional[InlineKeyboardMarkup],
)->Union[Message_,True]:
    pass
def editMessageCaption(
    chat_id:Union[int,str],
    message_id:Optional[int],
    inline_message_id:Optional[int],
    caption:Optional[str],
    parse_mode:Optional[int],
    caption_entities:Optional[List[MessageEntity]],
    reply_markup:Optional[InlineKeyboardMarkup],
)->Union[Message_,True]:
    pass
def editMessageMedia(
    chat_id:Optional[Union[int,str]],
    message_id:Optional[int],
    inline_message_id:Optional[int],
    media:InputMedia,
    reply_markup:Optional[InlineKeyboardMarkup],
)->Union[Message_,True]:
    pass
def editMessageReplyMarkup(
    chat_id:Optional[Union[int,str]],
    message_id:Optional[int],
    inline_message_id:Optional[int],
    reply_markup:Optional[InlineKeyboardMarkup],
)->Union[Message_,True]:
    pass
def stopPoll(
    chat_id:Optional[Union[int,str]],
    message_id:Optional[int],
    inline_message_id:Optional[int],
    reply_markup:Optional[InlineKeyboardMarkup],
)->'Poll':
    pass
def deleteMessage(
    chat_id:Optional[Union[int,str]],
    message_id:Optional[int],
)->bool:
    pass
