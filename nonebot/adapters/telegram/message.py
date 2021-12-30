from typing import Any, Type, Union, Mapping, Iterable, Optional, cast

from nonebot.typing import overrides

from nonebot.adapters import Message as BaseMessage
from nonebot.adapters import MessageSegment as BaseMessageSegment


class MessageSegment(BaseMessageSegment):
    """
    telegram 协议 MessageSegment 适配。具体方法参考协议消息段类型或源码。
    """

    @classmethod
    @overrides(BaseMessageSegment)
    def get_message_class(cls) -> Type["Message"]:
        return Message

    @overrides(BaseMessageSegment)
    def __str__(self) -> str:
        if self.type == "text":
            return self.data["text"]
        return ""

    @overrides(BaseMessageSegment)
    def is_text(self) -> bool:
        return self.type == "text"

    @staticmethod
    def text(text: str) -> "MessageSegment":
        return MessageSegment("text", {"text": text})

    @staticmethod
    def photo(file: str, caption: Optional[str] = None) -> "MessageSegment":
        return MessageSegment("photo", {"file": file, "caption": caption})

    @staticmethod
    def voice(file: str, caption: Optional[str] = None) -> "MessageSegment":
        return MessageSegment("voice", {"file": file, "caption": caption})

    @staticmethod
    def animation(
        file: str, thumb: Optional[str] = None, caption: Optional[str] = None
    ) -> "MessageSegment":
        return MessageSegment(
            "animation", {"file": file, "thumb": thumb, "caption": caption}
        )

    @staticmethod
    def audio(
        file: str, thumb: Optional[str] = None, caption: Optional[str] = None
    ) -> "MessageSegment":
        return MessageSegment(
            "audio", {"file": file, "thumb": thumb, "caption": caption}
        )

    @staticmethod
    def document(
        file: str, thumb: Optional[str] = None, caption: Optional[str] = None
    ) -> "MessageSegment":
        return MessageSegment(
            "document", {"file": file, "thumb": thumb, "caption": caption}
        )

    @staticmethod
    def video(
        file: str, thumb: Optional[str] = None, caption: Optional[str] = None
    ) -> "MessageSegment":
        return MessageSegment(
            "video", {"file": file, "thumb": thumb, "caption": caption}
        )


class Message(BaseMessage[MessageSegment]):
    @classmethod
    @overrides(BaseMessage)
    def get_segment_class(cls) -> Type["MessageSegment"]:
        return MessageSegment

    @staticmethod
    @overrides(BaseMessage)
    def _construct(
        msg: Union[str, Mapping, Iterable[Mapping]]
    ) -> Iterable[MessageSegment]:
        # TODO
        if isinstance(msg, Mapping):
            msg = cast(Mapping[str, Any], msg)
            for key in msg:
                if key == "text":
                    yield MessageSegment(
                        key, {key: msg[key], "entities": msg.get("entities")}
                    )
                elif key == "photo":
                    yield MessageSegment(
                        key,
                        {
                            "file": msg[key][0]["file_id"],
                            "caption": msg.get("caption"),
                            "caption_entities": msg.get("caption_entities"),
                        },
                    )
                elif key in [
                    "animation",
                    "audio",
                    "document",
                    "video",
                    "voice",
                ]:
                    yield MessageSegment(
                        key,
                        {
                            key: msg[key],
                            "caption": msg.get("caption"),
                            "caption_entities": msg.get("caption_entities"),
                        },
                    )
                elif key in ["sticker", "video_note", "dice", "poll"]:
                    yield MessageSegment(key, {key: msg[key]})
            return
        elif isinstance(msg, Iterable) and not isinstance(msg, str):
            for seg in msg:
                yield MessageSegment(seg["type"], seg.get("data") or {})
            return
        elif isinstance(msg, str):
            yield MessageSegment.text(msg)
