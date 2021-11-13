from nonebot import on_command
from nonebot_adapter_telegram import Bot
from nonebot_adapter_telegram.event import MessageEvent
from nonebot_adapter_telegram.message import MessageSegment


@on_command("photo").handle()
async def _(bot: Bot, event: MessageEvent):
    await bot.send(
        event,
        MessageSegment.photo(r"AgACAgUAAx0CZOoRWgADSGGPcupLE635AAGDe6YZn9LoRj3ygQAC8K0xG2AogFQlHXeB6GYblgEAAwIAA3MAAyIE"),
    )
