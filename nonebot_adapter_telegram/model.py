from typing import Any, Literal, Optional, get_type_hints
from nonebot.typing import overrides
from pydantic import BaseModel, Field

from .message import Message

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

    class Config:
        extra = "allow"


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
    photo: Optional[Any]
    """
    TODO

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
    pinned_message: Optional[Message]
    """
    :说明: 置顶消息，仅在使用 get_chat 方法时返回

    :类型: ``Optional[Message]``
    """
    permissions: Optional[Any]
    """
    TODO
    
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
    location: Optional[Any]
    """
    TODO Maybe Never Done

    :说明: 聊天地址，仅在使用 get_chat 方法时返回

    :类型: ``Optional[ChatLocation]``
    """

    class Config:
        extra = "allow"
