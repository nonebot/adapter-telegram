from nonebot import on_command
from nonebot.adapters.telegram import Bot
from nonebot.adapters.telegram.event import MessageEvent
from nonebot.adapters.telegram.message import MessageSegment


@on_command("photo").handle()
async def _(bot: Bot, event: MessageEvent):
    await bot.send(
        event,
        MessageSegment.photo(r"AgACAgUAAx0CZOoRWgADSGGPcupLE635AAGDe6YZn9LoRj3ygQAC8K0xG2AogFQlHXeB6GYblgEAAwIAA3MAAyIE"),
    )
