import asyncio

from nonebot import on_command
from nonebot.adapters.telegram import Bot
from nonebot.adapters.telegram.event import MessageEvent
from nonebot.adapters.telegram.message import Message, MessageSegment


@on_command("location").handle()
async def _(bot: Bot, event: MessageEvent):
    await bot.send(event, MessageSegment.location(31.2001033, 121.4326496))


@on_command("venue").handle()
async def _(bot: Bot, event: MessageEvent):
    await bot.send(
        event,
        MessageSegment.venue(31.2001033, 121.4326496, "NoneBot 研讨会", "上海交通大学"),
    )


@on_command("poll").handle()
async def _(bot: Bot, event: MessageEvent):
    await bot.send(
        event,
        MessageSegment.poll("NoneBot 3.0？", ["Breaking!", "No!", "DDL!DDL!DDL!"]),
    )


@on_command("dice").handle()
async def _(bot: Bot, event: MessageEvent):
    await bot.send(event, MessageSegment.dice())


@on_command("chat_action").handle()
async def _(bot: Bot, event: MessageEvent):
    await bot.send(event, MessageSegment.chat_action("typing"))
    await asyncio.sleep(1)
    await bot.send(event, "Typing complete!")
