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
        bot = Bot(ctx.create_adapter(base=Adapter), bot_config)
        bot.username = "test"
        bot._check_tome(event)
        assert event._tome
