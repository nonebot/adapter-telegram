import json
from pathlib import Path

import pytest


@pytest.mark.asyncio
async def test_event():
    from nonebot.adapters.telegram import Event
    from nonebot.adapters.telegram.event import (
        InlineQueryEvent,
        CallbackQueryEvent,
        PrivateMessageEvent,
        ChosenInlineResultEvent,
        PrivateEditedMessageEvent,
    )

    with (Path(__file__).parent / "updates.json").open("r", encoding="utf8") as f:
        test_updates = json.load(f)

    update_data = test_updates[0]
    event = Event.parse_event(update_data)
    assert isinstance(event, PrivateMessageEvent)

    update_data = test_updates[1]
    event = Event.parse_event(update_data)
    assert isinstance(event, PrivateMessageEvent)

    update_data = test_updates[2]
    event = Event.parse_event(update_data)
    assert isinstance(event, PrivateMessageEvent)

    update_data = test_updates[3]
    event = Event.parse_event(update_data)
    assert isinstance(event, PrivateMessageEvent)

    update_data = test_updates[4]
    event = Event.parse_event(update_data)
    assert isinstance(event, PrivateEditedMessageEvent)

    update_data = test_updates[9]
    event = Event.parse_event(update_data)
    assert isinstance(event, InlineQueryEvent)

    update_data = test_updates[10]
    event = Event.parse_event(update_data)
    assert isinstance(event, ChosenInlineResultEvent)

    update_data = test_updates[11]
    event = Event.parse_event(update_data)
    assert isinstance(event, CallbackQueryEvent)
