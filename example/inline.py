"""Inline Mode 的示例，未来可能会有较大改动"""

from nonebot import on, on_command
from nonebot.adapters.telegram import Bot
from nonebot.adapters.telegram.event import InlineQueryEvent, MessageEvent

from nonebot.adapters.telegram.model import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

# InlineKeyboard：https://core.telegram.org/bots#inline-keyboards-and-on-the-fly-updating
@on_command("inline1").handle()
async def _(bot: Bot, event: MessageEvent):
    await bot.send(
        event,
        "Hello InlineKeyboard !",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Nonebot Adapter Telegram",
                        url="https://github.com/nonebot/adapter-telegram",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Telegram Bot API",
                        url="https://core.telegram.org/bots/api",
                    )
                ],
            ]
        ).json(),
    )


# InlineQuery：https://core.telegram.org/bots/inline
@on("").handle()  # 由于我还未给 InlineQueryEvent 分配 event_name，目前只能使用 on("") 来匹配
async def _(bot: Bot, event: InlineQueryEvent):
    await bot.answer_inline_query(
        inline_query_id=event.id,
        results=[
            InlineQueryResultArticle(
                id="hello",
                title="Hello InlineMode !",
                input_message_content=InputTextMessageContent(
                    message_text="Hello InlineMode !"
                ),
            )
        ],
    )
