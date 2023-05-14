"""回复消息的示例"""

from nonebot import on_command
from nonebot.adapters.telegram import Bot
from nonebot.adapters.telegram.event import MessageEvent

cmd_reply = on_command("reply")


@cmd_reply.handle()
async def _(bot: Bot, event: MessageEvent):
    await bot.send(event, "Reply to message", reply_to_message_id=event.message_id)
