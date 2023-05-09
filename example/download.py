from pathlib import Path

from anyio import open_file
from httpx import AsyncClient

from nonebot import on_command
from nonebot.adapters.telegram import Bot
from nonebot.adapters.telegram.message import File
from nonebot.adapters.telegram.event import MessageEvent


@on_command("download").handle()
async def _(bot: Bot, event: MessageEvent):
    for seg in event.get_message() + (
        event.reply_to_message.get_message() if event.reply_to_message else []
    ):
        if isinstance(seg, File):
            file = await bot.get_file(file_id=seg.data["file"])
            url = f"https://api.telegram.org/file/bot{bot.bot_config.token}/{file.file_path}"
            async with AsyncClient() as c:
                async with await open_file(
                    Path(file.file_path).name, "wb"  # type:ignore
                ) as f:
                    await f.write((await c.get(url)).content)
