"""
@某个用户的示例
"""

from typing import Union

from nonebot import on_command
from nonebot.adapters.telegram import Bot
from nonebot.adapters.telegram.message import Entity
from nonebot.adapters.telegram.event import GroupMessageEvent, PrivateMessageEvent

# ChannelPostEvent 没有 from 字段
MessageEventHasUser = Union[PrivateMessageEvent, GroupMessageEvent]


@on_command("mention").handle()
async def _(bot: Bot, event: MessageEventHasUser):
    # 获取一个 User 对象，这里从 event 获取用户的 User 对象
    user = event.from_

    # 获取用户名
    username = user.username

    if username:
        # 要注意的是使用 Entity.mention 需要该用户有 username
        await bot.send(event, Entity.mention(f"@{username}"))

        # 还要注意 Entity.mention 不能与其它消息直接相连，要用空格间隔开
        # @ 之前若与其他消息相连，则 Telegram 不会识别其为 mention
        # @ 之后若有其他消息相连，则 Telegram 会将后面的消息也识别为 username 的一部分
        await bot.send(
            event, "first part " + Entity.mention(f"@{username}") + " second_part"
        )

    else:
        # 当用户没有用户名时，请使用 text_link 或 text_mention 进行 @
        lastname = f" {user.last_name}" if user.last_name else ""
        nick = f"{user.first_name}{lastname}"

        # text_link
        await bot.send(
            event,
            "Hello, " + Entity.text_link(nick, f"tg://user?id={user.id}") + "!",
        )

        # text_mention
        await bot.send(event, Entity.text_mention(nick, user) + ", How are you?")
        # 与 mention 不同的是，text_mention 的文本可以自定义
        await bot.send(event, Entity.text_mention("anytext", user))
