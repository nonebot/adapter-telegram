import pytest
from nonebug import App

from nonebot.adapters.telegram import Event, Adapter
from nonebot.adapters.telegram.config import BotConfig
from nonebot.adapters.telegram.event import GroupMessageEvent

bot_config = BotConfig(token="1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHI")


import json
from pathlib import Path


@pytest.mark.asyncio
async def test_check_tome(app: App):
    from nonebot.adapters.telegram.bot import Bot

    with (Path(__file__).parent / "updates.json").open("r", encoding="utf8") as f:
        test_updates = json.load(f)
    test_update = test_updates[0]
    test_update["message"]["chat"]["type"] = "group"
    test_update["message"]["text"] = "@test"
    test_update["message"]["entities"] = [{"type": "mention", "offset": 0, "length": 5}]
    event = Event.parse_event(test_update)
    assert isinstance(event, GroupMessageEvent)

    async with app.test_api() as ctx:
        bot = Bot(
            ctx.create_adapter(base=Adapter),
            Bot.get_bot_id_by_token(bot_config.token),
            config=bot_config,
        )
        bot.username = "test"
        bot._check_tome(event)
        assert event._tome

@pytest.mark.asyncio
async def test_send_to(app: App):
    from nonebot.adapters.telegram.bot import Bot
    from nonebot.adapters.telegram.message import File, Message
    from nonebot.adapters.telegram.model import InputMediaPhoto, InputMediaAudio, Chat, Message as ReturnMessage

    Chat.update_forward_refs()

    with (Path(__file__).parent / "updates.json").open("r", encoding="utf8") as f:
        test_updates = json.load(f)
    test_update = test_updates[0]
    test_update["message"]["chat"]["type"] = "group"
    test_update["message"]["text"] = "@test"
    test_update["message"]["entities"] = [{"type": "mention", "offset": 0, "length": 5}]
    event = Event.parse_event(test_update)
    assert isinstance(event, GroupMessageEvent)

    async with app.test_api() as ctx:
        bot = Bot(
            ctx.create_adapter(base=Adapter),
            Bot.get_bot_id_by_token(bot_config.token),
            config=bot_config,
        )
        bot.username = "test"
        ctx.should_call_api(
            "send_media_group",
            {
                "chat_id": 1234567890,
                "message_thread_id": None,
                "media": [
                    InputMediaPhoto(
                        media="test.jpg",
                        has_spoiler=True,
                    ),
                    InputMediaAudio(
                        media="test.ogg",
                    ),
                ],
                "reply_parameters": None,
                "disable_notification": None,
                "protect_content": None,
                "reply_to_message_id": None,
                "allow_sending_without_reply": None,
            },
            [
                ReturnMessage(
                    message_id=1,
                    date=111,
                    chat=Chat(id=1, type="group")
                ).dict(),
                ReturnMessage(
                    message_id=2,
                    date=222,
                    chat=Chat(id=2, type="group")
                ).dict(),
            ]
        )
        await bot.send_to(chat_id=1234567890, message=Message([File.photo("test.jpg", has_spoiler=True), File.audio("test.ogg")]))