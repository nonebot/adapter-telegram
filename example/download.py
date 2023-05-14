from pathlib import Path

import anyio
from httpx import AsyncClient

from nonebot import on_command
from nonebot.adapters.telegram import Bot
from nonebot.adapters.telegram.message import File
from nonebot.adapters.telegram.event import MessageEvent

DATA_PATH = Path.cwd() / "download"
if not DATA_PATH.exists():
    DATA_PATH.mkdir(parents=True)


async def download_file(bot: Bot, file_id: str):
    file = await bot.get_file(file_id=file_id)
    file_path = file.file_path
    if not file_path:
        return

    if Path(file_path).exists():
        # 本地搭建的 Telegram Bot API 会传给你本地的文件路径
        data = await anyio.Path(file_path).read_bytes()

    else:
        url = f"https://api.telegram.org/file/bot{bot.bot_config.token}/{file_path}"
        async with AsyncClient() as c:
            data = (await c.get(url)).content

    await anyio.Path(DATA_PATH / file_path).write_bytes(data)


@on_command("download").handle()
async def _(bot: Bot, event: MessageEvent):
    for seg in event.get_message() + (
        event.reply_to_message.get_message() if event.reply_to_message else []
    ):
        if isinstance(seg, File):
            await download_file(bot, seg.data["file"])
