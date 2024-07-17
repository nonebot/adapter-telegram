from typing_extensions import override
from typing import Any, Union, Literal, TypeVar, Iterable, Optional

from nonebot.adapters import Message as BaseMessage
from nonebot.adapters import MessageSegment as BaseMessageSegment

from .model import User, MessageEntity

TMS = TypeVar("TMS", bound="MessageSegment")


class MessageSegment(BaseMessageSegment):
    """
    telegram 协议 MessageSegment 适配。具体方法参考协议消息段类型或源码。
    """

    @classmethod
    @override
    def get_message_class(cls) -> type["Message"]:
        return Message

    @override
    def __str__(self) -> str:
        if self.is_text():
            return self.data.get("text", "")
        return ""

    def __repr__(self) -> str:
        if self.is_text():
            return self.data.get("text", "")
        params = ", ".join(
            [
                f"{k}={f'<file {v[0]}>' if isinstance(v, tuple) else ('<bytes>' if isinstance(v, bytes) else v)}"
                for k, v in self.data.items()
                if v is not None
            ]
        )
        return f"[{self.type}{':' if params else ''}{params}]"

    @override
    def is_text(self) -> bool:
        return False

    @staticmethod
    def location(
        latitude: float,
        longitude: float,
        horizontal_accuracy: Optional[float] = None,
        live_period: Optional[int] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
    ) -> "MessageSegment":
        return MessageSegment(
            "location",
            {
                "latitude": latitude,
                "longitude": longitude,
                "horizontal_accuracy": horizontal_accuracy,
                "live_period": live_period,
                "heading": heading,
                "proximity_alert_radius": proximity_alert_radius,
            },
        )

    @staticmethod
    def venue(
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        foursquare_id: Optional[str] = None,
        foursquare_type: Optional[str] = None,
        google_place_id: Optional[str] = None,
        google_place_type: Optional[str] = None,
    ) -> "MessageSegment":
        return MessageSegment(
            "venue",
            {
                "latitude": latitude,
                "longitude": longitude,
                "title": title,
                "address": address,
                "foursquare_id": foursquare_id,
                "foursquare_type": foursquare_type,
                "google_place_id": google_place_id,
                "google_place_type": google_place_type,
            },
        )

    @staticmethod
    def poll(
        question: str,
        options: list[str],
        is_anonymous: Optional[bool] = None,
        type: Optional[str] = None,
        allows_multiple_answers: Optional[bool] = None,
        correct_option_id: Optional[int] = None,
        explanation: Optional[str] = None,
        open_period: Optional[int] = None,
        close_date: Optional[int] = None,
    ) -> "MessageSegment":
        return MessageSegment(
            "poll",
            {
                "question": question,
                "options": options,
                "is_anonymous": is_anonymous,
                "type": type,
                "allows_multiple_answers": allows_multiple_answers,
                "correct_option_id": correct_option_id,
                "explanation": explanation,
                "open_period": open_period,
                "close_date": close_date,
            },
        )

    @staticmethod
    def dice(
        emoji: Literal["🎲", "🎯", "🏀", "⚽", "🎳", "🎰"] = "🎲",
    ) -> "MessageSegment":
        return MessageSegment("dice", {"emoji": emoji})

    @staticmethod
    def chat_action(
        action: Literal[
            "typing",
            "upload_photo",
            "record_video",
            "upload_video",
            "record_voice",
            "upload_voice",
            "upload_document",
            "choose_sticker",
            "find_location",
            "record_video_note",
            "upload_video_note",
        ],
    ) -> "MessageSegment":
        """
        仅发送，用于提醒用户机器人正在准备什么
        """
        return MessageSegment("chat_action", {"action": action})

    # TODO NEVER
    @staticmethod
    def invoice():
        raise NotImplementedError

    # TODO NEVER
    @staticmethod
    def contact():
        raise NotImplementedError

    # TODO DELAY
    @staticmethod
    def game():
        raise NotImplementedError


class Reply(MessageSegment):
    @staticmethod
    def reply(
        message_id: int,
        chat_id: Optional[Union[int, str]] = None,
        allow_sending_without_reply: Optional[bool] = None,
        quote: Optional[str] = None,
        quote_position: Optional[int] = None,
    ):
        return Reply(
            "reply",
            {
                "message_id": message_id,
                "chat_id": chat_id,
                "allow_sending_without_reply": allow_sending_without_reply,
                "quote": quote,
                "quote_position": quote_position,
            },
        )

    @staticmethod
    def markup():
        pass


class Entity(MessageSegment):
    def __init__(self, type: str, data: dict[str, Any], _length: int = 0):
        super().__init__(type, data)
        self._length = _length
        if _length == 0:
            self._length = len(self.data["text"].encode("utf-16-le")) // 2

    @override
    def is_text(self) -> bool:
        return True

    @staticmethod
    def text(text: str):
        """
        纯文本
        """
        return Entity("text", {"text": text})

    @staticmethod
    def mention(text: str):
        return Entity("mention", {"text": text})

    @staticmethod
    def hashtag(text: str):
        return Entity("hashtag", {"text": text})

    @staticmethod
    def cashtag(text: str):
        return Entity("cashtag", {"text": text})

    @staticmethod
    def bot_command(text: str):
        return Entity("bot_command", {"text": text})

    @staticmethod
    def url(text: str):
        return Entity("url", {"text": text})

    @staticmethod
    def email(text: str):
        return Entity("email", {"text": text})

    @staticmethod
    def phone_number(text: str):
        return Entity("phone_number", {"text": text})

    @staticmethod
    def bold(text: str):
        return Entity("bold", {"text": text})

    @staticmethod
    def italic(text: str):
        return Entity("italic", {"text": text})

    @staticmethod
    def underline(text: str):
        return Entity("underline", {"text": text})

    @staticmethod
    def strikethrough(text: str):
        return Entity("strikethrough", {"text": text})

    @staticmethod
    def spoiler(text: str):
        return Entity("spoiler", {"text": text})

    @staticmethod
    def blockquote(text: str):
        return Entity("blockquote", {"text": text})

    @staticmethod
    def code(text: str):
        return Entity("code", {"text": text})

    @staticmethod
    def pre(text: str, language: str) -> "Entity":
        return Entity("pre", {"text": text, "language": language})

    @staticmethod
    def text_link(text: str, url: str) -> "Entity":
        return Entity("text_link", {"text": text, "url": url})

    @staticmethod
    def text_mention(text: str, user: User) -> "Entity":
        return Entity("text_mention", {"text": text, "user": user})

    @staticmethod
    def custom_emoji(text: str, custom_emoji_id: str) -> "Entity":
        return Entity(
            "custom_emoji", {"text": text, "custom_emoji_id": custom_emoji_id}
        )

    @staticmethod
    def from_telegram_entities(text, entities: list[dict[str, Any]]) -> list["Entity"]:
        nb_entites = []
        offset = 0
        text = text.encode("utf-16-le")
        for entity in entities:
            if entity["offset"] > offset:
                nb_entites.append(
                    Entity(
                        "text",
                        {
                            "text": text[offset * 2 : entity["offset"] * 2].decode(
                                "utf-16-le"
                            )
                        },
                        entity["offset"] - offset,
                    )
                )
            nb_entity = Entity(
                entity["type"],
                {
                    "text": text[
                        entity["offset"] * 2 : (entity["offset"] + entity["length"]) * 2
                    ].decode("utf-16-le")
                },
                entity["length"],
            )
            if "language" in entity:
                nb_entity.data["language"] = entity["language"]
            if "url" in entity:
                nb_entity.data["url"] = entity["url"]
            if "user" in entity:
                nb_entity.data["user"] = User(**entity["user"])
            if "custom_emoji_id" in entity:
                nb_entity.data["custom_emoji_id"] = entity["custom_emoji_id"]
            nb_entites.append(nb_entity)
            offset = entity["offset"] + entity["length"]
        if offset < len(text):
            nb_entites.append(
                Entity(
                    "text",
                    {"text": text[offset * 2 :].decode("utf-16-le")},
                    (len(text) - offset * 2) // 2,
                )
            )
        return nb_entites

    @staticmethod
    def build_telegram_entities(entities: list["Entity"]) -> list[MessageEntity]:
        return (
            (
                [
                    MessageEntity(
                        type=entity.type,  # type: ignore
                        offset=sum(map(lambda _: _._length, entities[:i])),
                        length=entity._length,
                        url=entity.data.get("url"),
                        user=entity.data.get("user"),
                        language=entity.data.get("language"),
                        custom_emoji_id=entity.data.get("custom_emoji_id"),
                    )
                    for i, entity in enumerate(entities)
                    if entity.is_text() and entity.type != "text"
                ]
                or None
            )
            if entities
            else None
        )


class File(MessageSegment):
    @staticmethod
    def photo(
        file: Union[str, bytes, tuple[str, bytes]], has_spoiler: Optional[bool] = None
    ) -> "MessageSegment":
        return File("photo", {"file": file, "has_spoiler": has_spoiler})

    @staticmethod
    def voice(file: Union[str, bytes, tuple[str, bytes]]) -> "MessageSegment":
        return File("voice", {"file": file})

    @staticmethod
    def animation(
        file: Union[str, bytes, tuple[str, bytes]],
        thumbnail: Union[None, str, bytes] = None,
        has_spoiler: Optional[bool] = None,
    ) -> "MessageSegment":
        return File(
            "animation",
            {"file": file, "thumbnail": thumbnail, "has_spoiler": has_spoiler},
        )

    @staticmethod
    def audio(
        file: Union[str, bytes, tuple[str, bytes]],
        thumbnail: Union[None, str, bytes] = None,
    ) -> "MessageSegment":
        return File("audio", {"file": file, "thumbnail": thumbnail})

    @staticmethod
    def document(
        file: Union[str, bytes, tuple[str, bytes]],
        thumbnail: Union[None, str, bytes] = None,
    ) -> "MessageSegment":
        return File("document", {"file": file, "thumbnail": thumbnail})

    @staticmethod
    def video(
        file: Union[str, bytes, tuple[str, bytes]],
        thumbnail: Union[None, str, bytes] = None,
        has_spoiler: Optional[bool] = None,
    ) -> "MessageSegment":
        return File(
            "video",
            {"file": file, "thumbnail": thumbnail, "has_spoiler": has_spoiler},
        )


class UnCombinFile(File):
    @staticmethod
    def sticker(file: Union[str, bytes, tuple[str, bytes]]) -> "MessageSegment":
        return File("sticker", {"file": file})

    @staticmethod
    def video_note(
        file: Union[str, bytes, tuple[str, bytes]],
        thumbnail: Union[None, str, bytes] = None,
    ) -> "MessageSegment":
        """
        不支持 URL
        """
        return File("video_note", {"file": file, "thumbnail": thumbnail})


class Message(BaseMessage[TMS]):
    def __repr__(self) -> str:
        return "".join(repr(seg) for seg in self)

    @classmethod
    @override
    def get_segment_class(cls) -> type["MessageSegment"]:
        return MessageSegment

    @staticmethod
    @override
    def _construct(msg: str) -> Iterable[MessageSegment]:
        yield Entity.text(msg)

    @classmethod
    def model_validate(cls, obj: dict[str, Any]) -> "Message":
        msg = []
        if "text" in obj or "caption" in obj:
            key, entities_key = (
                ("text", "entities")
                if "text" in obj
                else ("caption", "caption_entities")
            )
            msg.extend(
                Entity.from_telegram_entities(obj[key], obj.get(entities_key, ()))
            )
            del obj[key]
            obj.pop(entities_key, None)
        kargs = {}
        if obj.get("has_media_spoiler", None):
            kargs["has_spoiler"] = True
        obj.pop("has_media_spoiler", None)
        if "animation" in obj:
            del obj["document"]
        for key in tuple(obj.keys()):
            if key == "photo":
                seg = File("photo", {"file": obj[key][-1]["file_id"]})
            elif key in ("voice", "audio", "animation", "document", "video"):
                seg = File(key, {"file": obj[key]["file_id"]})
            elif key in ("sticker", "video_note"):
                seg = UnCombinFile(key, {"file": obj[key]["file_id"]})
            elif key in ("dice", "poll", "location"):
                seg = MessageSegment(key, obj[key])
            elif key == "venue":
                location = obj[key].pop("location")
                seg = MessageSegment(
                    key,
                    {
                        "latitude": location["latitude"],
                        "longitude": location["longitude"],
                        **obj[key],
                    },
                )
            else:
                continue
            if isinstance(obj[key], dict) and obj[key].get("thumbnail", None):
                kargs["thumbnail"] = obj[key]["thumbnail"]["file_id"]
            seg.data.update(kargs)
            msg.append(seg)
            del obj[key]
        return cls(msg)
