from typing import Any, Dict, Literal, Union, Tuple, Mapping, Iterable, Optional

from nonebot.typing import overrides
from nonebot.adapters import (
    Message as BaseMessage,
    MessageSegment as BaseMessageSegment,
)


class MessageSegment(BaseMessageSegment):
    """
    telegram 协议 MessageSegment 适配。具体方法参考协议消息段类型或源码。
    """

    @overrides(BaseMessageSegment)
    def __init__(self, type: str, data: Dict[str, Any]) -> None:
        super().__init__(type=type, data=data)

    @overrides(BaseMessageSegment)
    def get_message_class(cls) -> "MessageSegment":
        return MessageSegment

    @overrides(BaseMessageSegment)
    def __str__(self) -> str:
        if self.type == "text":
            return self.data.get("text")

    @overrides(BaseMessageSegment)
    def __add__(self, other) -> "Message":
        return Message(self) + other

    @overrides(BaseMessageSegment)
    def __radd__(self, other) -> "Message":
        return (
            MessageSegment.text(other) if isinstance(other, str) else Message(other)
        ) + self

    @overrides(BaseMessageSegment)
    def is_text(self) -> bool:
        return self.type == "text"

    @staticmethod
    def text(text: str) -> "MessageSegment":
        return MessageSegment("text", {"text": text})


class Message(BaseMessage):
    @staticmethod
    @overrides(BaseMessage)
    def _construct(
        msg: Union[str, Mapping, Iterable[Mapping]]
    ) -> Iterable[MessageSegment]:
        if isinstance(msg, Mapping):
            for key in msg:
                if key == "text":
                    yield MessageSegment(key, {"text": msg[key]})
            return
        elif isinstance(msg, Iterable) and not isinstance(msg, str):
            for seg in msg:
                yield MessageSegment(seg.type, seg.data or {})
            return
        elif isinstance(msg, str):
            def _iter_message(msg: str) -> Iterable[Tuple[str, str]]:
                text_begin = 0
                yield "text", msg[text_begin:]

            for type_, data in _iter_message(msg):
                if type_ == "text":
                    if data:
                        yield MessageSegment(type_, {"text": data})
                else:
                    data = {
                        k: v
                        for k, v in map(
                            lambda x: x.split("=", maxsplit=1),
                            filter(lambda x: x, (x.lstrip() for x in data.split(","))),
                        )
                    }
                    yield MessageSegment(type_, data)
