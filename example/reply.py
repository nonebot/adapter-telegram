"""回复消息的示例"""

from nonebot import on_command
from nonebot.adapters.telegram import Bot
from nonebot.adapters.telegram.message import Reply
from nonebot.adapters.telegram.event import MessageEvent


@on_command("reply").handle()
async def _(bot: Bot, event: MessageEvent):
    await bot.send(event, "Reply to message" + Reply.reply(event.message_id))
