from nonebot.permission import Permission

from .bot import Bot
from .event import GroupMessageEvent, PrivateMessageEvent


async def _private(event: PrivateMessageEvent) -> bool:
    return True


PRIVATE: Permission = Permission(_private)
""" 匹配任意私聊消息类型事件"""


async def _group(event: GroupMessageEvent) -> bool:
    return True


async def _group_member(bot: Bot, event: GroupMessageEvent) -> bool:
    return (await bot.get_chat_member(event.chat.id, event.from_.id)).status == "member"


async def _group_admin(bot: Bot, event: GroupMessageEvent) -> bool:
    return (
        await bot.get_chat_member(event.chat.id, event.from_.id)
    ).status == "administrator"


async def _group_creator(bot: Bot, event: GroupMessageEvent) -> bool:
    return (
        await bot.get_chat_member(event.chat.id, event.from_.id)
    ).status == "creator"


GROUP: Permission = Permission(_group)
"""匹配任意群聊消息类型事件"""
GROUP_MEMBER: Permission = Permission(_group_member)
"""匹配任意群员群聊消息类型事件

:::warning 警告
该权限通过 event.sender 进行判断且不包含管理员以及群创建者！
:::
"""
GROUP_ADMIN: Permission = Permission(_group_admin)
"""匹配任意群管理员群聊消息类型事件"""
GROUP_CREATOR: Permission = Permission(_group_creator)
"""匹配任意群创建者群聊消息类型事件"""
