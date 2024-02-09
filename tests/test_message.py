import json
from pathlib import Path

import pytest

from nonebot.adapters.telegram.event import Event, PrivateMessageEvent


@pytest.mark.asyncio
async def test_message_model_validate():
    with (Path(__file__).parent / "updates.json").open("r", encoding="utf8") as f:
        test_updates = json.load(f)

    update_data = test_updates[5]
    event = Event.parse_event(update_data)
    assert isinstance(event, PrivateMessageEvent)
    assert event.message[0].type == "bold"
    assert event.message[1].type == "text"
    assert event.message[2].type == "italic"

    update_data = test_updates[6]
    event = Event.parse_event(update_data)
    assert isinstance(event, PrivateMessageEvent)
    assert event.message[0].type == "audio"

    update_data = test_updates[7]
    event = Event.parse_event(update_data)
    assert isinstance(event, PrivateMessageEvent)
    assert event.message[0].type == "voice"

    update_data = test_updates[8]
    event = Event.parse_event(update_data)
    assert isinstance(event, PrivateMessageEvent)
    assert event.message[0].type == "document"
