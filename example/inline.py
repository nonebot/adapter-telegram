"""
Inline Bots：https://core.telegram.org/bots/inline
"""

from nonebot import on, on_command
from nonebot.adapters.telegram import Bot
from nonebot.adapters.telegram.event import (
    MessageEvent,
    InlineQueryEvent,
    CallbackQueryEvent,
)
from nonebot.adapters.telegram.model import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputTextMessageContent,
    InlineQueryResultArticle,
)


@on("inline").handle()
async def _(bot: Bot, event: InlineQueryEvent):
    await bot.answer_inline_query(
        inline_query_id=event.id,
        results=[
            InlineQueryResultArticle(
                id="hello1",
                title="Hello",
                input_message_content=InputTextMessageContent(
                    message_text="Hello InlineQuery !"
                ),
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
                        [
                            InlineKeyboardButton(
                                text="Say hello to me",
                                callback_data="hello",
                            )
                        ],
                    ]
                ),
            ),
        ],
    )


@on("inline").handle()
async def _(bot: Bot, event: CallbackQueryEvent):
    if event.message:
        await bot.edit_message_text(
            "Hello CallbackQuery!", event.message.chat.id, event.message.message_id
        )
        await bot.answer_callback_query(event.id, text="Hello CallbackQuery!")
