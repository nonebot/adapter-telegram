from nonebot import on_command
from nonebot.rule import to_me
from nonebot_adapter_telegram import Bot
from nonebot_adapter_telegram.event import MessageEvent


@on_command("echo", rule=to_me()).handle()
async def _(bot: Bot, event: MessageEvent):
    if event.get_message():
        await bot.send(event, event.get_message())
