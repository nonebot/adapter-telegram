"""@某个用户的示例"""

# [重构提醒]:该实例涉及的Entity在将会会进行重构,本示例可能会过时
# 所以使用"""~"""来代表可能会过时的注释,请注意分辨

from nonebot import on_command
from nonebot.adapters.telegram import Bot
from nonebot.adapters.telegram.event import MessageEvent
from nonebot.adapters.telegram.message import Entity, Message

mention = on_command("mention1")


@mention.handle()
async def _(event: MessageEvent):
    user = event.telegram_model.message.from_
    # 获取一个User对象,这里采用event获取发送mention命令的用户User对象

    if user is None:
        return
    # ChannelPostEvent没有from字段

    username = user.username
    # 获取用户名

    await mention.send(Entity.mention("@" + username))
    """要注意的是使用Entity.mention必须保证@存在,以及username的正确"""
    # [重构提醒]:将来会自动添加@

    await mention.send(
        Message(["first part", " ", Entity.mention("@" + username), " ", "second_part"])
    )
    # 你当然也可以在消息片段发送@某人

    """
    还要注意的是Entity.mention不能与其它消息直接相连,要用空格间隔开
    如await mention.send(Message(['first_part',Entity.mention("@"+username),'second']))是绝对不允许的!
    @前面若存在其他消息,则telegrame不会识别该mention
    @后面若有其他消息,则telegrame会将后面的消息也识别为username的一部分
    """
    # [重构提醒]将来会自动加空格


mention2 = on_command("mention2")


@mention2.handle()
async def _(event: MessageEvent):
    user = event.telegram_model.message.from_
    if user is None:
        return
    username = user.username

    await mention.send(Entity.text_mention("@" + username, user))
    # 你可以使用Entity.text_mention来达到与Entity.mention相近的效果
    await mention.send(Entity.text_mention("anytext", user))
    # 与mention不同的是,text_mention的文本可以为自己定义,且不影响mention链接

    await mention.send(
        Message(
            [
                "first part",
                " ",
                Entity.text_mention("anytext", user),
                " ",
                "second_part",
            ]
        )
    )
    # 使用方法与mention类似
    """也是注意消息不能粘连"""
    # [重构提醒]将来会自动加空格
