"""
@某个用户的示例

本示例所涉及的 Entity 在将在下个版本重构
"""

from nonebot import on_command
from nonebot.adapters.telegram import Bot
from nonebot.adapters.telegram.message import Entity
from nonebot.adapters.telegram.event import MessageEvent

cmd_mention1 = on_command("mention1")


@cmd_mention1.handle()
async def _(bot: Bot, event: MessageEvent):
    user = event.telegram_model.message.from_
    # 获取一个 User 对象，这里从 event 获取用户的 User 对象

    if user is None:
        return
    # ChannelPostEvent 没有 from 字段

    username = user.username
    # 获取用户名

    await bot.send(event, Entity.mention("@" + username))
    """要注意的是使用 Entity.mention 需要该用户有 username"""

    await bot.send(
        event, "first part " + Entity.mention("@" + username) + " second_part"
    )
    """
    还要注意 Entity.mention 不能与其它消息直接相连，要用空格间隔开
    @之前若与其他消息相连，则 Telegram 不会识别其为 mention
    @之后若有其他消息相连，则 Telegram 会将后面的消息也识别为 username 的一部分
    """


cmd_mention2 = on_command("mention2")


@cmd_mention2.handle()
async def _(bot: Bot, event: MessageEvent):
    if (user := event.telegram_model.message.from_) is None:
        return

    await bot.send(event, Entity.text_mention("anytext", user))
    # 与 mention 不同的是，text_mention 的文本可以自定义
