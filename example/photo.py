"""发送图片的示例，其他上传文件的操作同理"""


from anyio import open_file

from nonebot import on_command
from nonebot.adapters.telegram import Bot
from nonebot.adapters.telegram.message import File
from nonebot.adapters.telegram.event import MessageEvent
from nonebot.adapters.telegram.model import InputMediaPhoto


cmd_photo1 = on_command("photo1")


# 用 bytes 发送图片
@cmd_photo1.handle()
async def _(bot: Bot, event: MessageEvent):
    async with await open_file("./docs/logo.png", "rb") as f:
        await bot.send(
            event,
            File.photo(await f.read()),
        )


cmd_photo2 = on_command("photo2")


# 用路径发送图片
@cmd_photo2.handle()
async def _(bot: Bot, event: MessageEvent):
    await bot.send(
        event,
        File.photo("./docs/logo.png"),
    )


cmd_photo3 = on_command("photo3")


# 带有注释的图片
@cmd_photo3.handle()
async def _(bot: Bot, event: MessageEvent):
    await bot.send(
        event,
        File.photo("./docs/logo.png") + "NoneBot",
    )


cmd_photo4 = on_command("photo4")


# 多张图片
@cmd_photo4.handle()
async def _(bot: Bot, event: MessageEvent):
    await bot.send(
        event,
        File.photo("./docs/logo.png") + File.photo("./docs/logo.png"),
    )


cmd_photo5 = on_command("photo5")


# 使用原生 API 发送图片
@cmd_photo5.handle()
async def _(bot: Bot, event: MessageEvent):
    await bot.send_photo(
        chat_id=event.chat.id, photo="./docs/logo.png", caption="NoneBot"
    )


cmd_photo6 = on_command("photo6")


# 使用原生 API 发送多张图片
@cmd_photo6.handle()
async def _(bot: Bot, event: MessageEvent):
    await bot.send_media_group(
        chat_id=event.chat.id,
        media=[
            InputMediaPhoto(media="./docs/logo.png"),
            InputMediaPhoto(media="./docs/logo.png"),
        ],
    )
