from typing import Any, Dict, List, Type, Union, Iterable

from nonebot.typing import overrides

from nonebot.adapters import Message as BaseMessage
from nonebot.adapters import MessageSegment as BaseMessageSegment

from .model import User, LabeledPrice


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
        return ""

    @overrides(BaseMessageSegment)
    def is_text(self) -> bool:
        return False

    @staticmethod
    def location(latitude: float, longitude: float) -> "MessageSegment":
        return MessageSegment(
            "location", {"latitude": latitude, "longitute": longitude}
        )

    @staticmethod
    def venue(
        latitude: float, longitude: float, title: str, address: str
    ) -> "MessageSegment":
        return MessageSegment("venue", {"latitude": latitude, "longitute": longitude})

    @staticmethod
    def contact():
        pass

    @staticmethod
    def poll(question: str, options: List[str]) -> "MessageSegment":
        return MessageSegment("poll", {"question": question, "options": options})

    @staticmethod
    def dice() -> "MessageSegment":
        return MessageSegment("dice")

    @staticmethod
    def chat_action(
        action: str, message: Union["MessageSegment", "Message"]
    ) -> "MessageSegment":
        """
        仅发送，用于提醒用户机器人正在准备什么
        """
        return MessageSegment("chat_action", {"action": action, "message": message})

    # TODO DELAY
    @staticmethod
    def invoice(
        title: str,
        description: str,
        payload: str,
        provider_token: str,
        currency: str,
        prices: List[LabeledPrice],
    ):
        pass

    @staticmethod
    def game(game_short_name: str) -> "MessageSegment":
        return MessageSegment("game", {"message": game_short_name})


class Entity(MessageSegment):
    @overrides(BaseMessageSegment)
    def __str__(self) -> str:
        return self.data["text"]

    @overrides(BaseMessageSegment)
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


class File(MessageSegment):
    @staticmethod
    def photo(file: Union[str, bytes]) -> "MessageSegment":
        return File("photo", {"file": file})

    @staticmethod
    def voice(
        file: Union[str, bytes],
    ) -> "MessageSegment":
        return File("voice", {"file": file})

    @staticmethod
    def sticker(file: Union[str, bytes]) -> "MessageSegment":
        return File("video_note", {"file": file})

    @staticmethod
    def animation(
        file: Union[str, bytes],
        thumb: Union[None, str, bytes] = None,
    ) -> "MessageSegment":
        return File("animation", {"file": file, "thumb": thumb})

    @staticmethod
    def audio(
        file: Union[str, bytes],
        thumb: Union[None, str, bytes] = None,
    ) -> "MessageSegment":
        return File("audio", {"file": file, "thumb": thumb})

    @staticmethod
    def document(
        file: Union[str, bytes],
        thumb: Union[None, str, bytes] = None,
    ) -> "MessageSegment":
        return File("document", {"file": file, "thumb": thumb})

    @staticmethod
    def video(
        file: Union[str, bytes],
        thumb: Union[None, str, bytes] = None,
    ) -> "MessageSegment":
        return File("video", {"file": file, "thumb": thumb})

    @staticmethod
    def video_note(
        file: Union[str, bytes],
        thumb: Union[None, str, bytes] = None,
    ) -> "MessageSegment":
        return File("video_note", {"file": file, "thumb": thumb})


class Message(BaseMessage[MessageSegment]):
    @classmethod
    @overrides(BaseMessage)
    def get_segment_class(cls) -> Type["MessageSegment"]:
        return MessageSegment

    @staticmethod
    @overrides(BaseMessage)
    def _construct(msg: str) -> Iterable[MessageSegment]:
        yield Entity.text(msg)

    @classmethod
    def parse_obj(cls, obj: Dict[str, Any]) -> "Message":
        msg = []
        if "text" in obj or "caption" in obj:
            key = "text" if "text" in obj else "caption"
            offset = 0
            for entity in obj.get("entities", obj.get("caption_entities", [])):
                if entity["offset"] > offset:
                    msg.append(
                        Entity("text", {"text": obj[key][offset : entity["offset"]]})
                    )
                nb_entity = Entity(
                    entity["type"],
                    {
                        "text": obj[key][
                            entity["offset"] : entity["offset"] + entity["length"]
                        ]
                    },
                )
                if "language" in entity:
                    nb_entity.data["language"] = entity["language"]
                if "url" in entity:
                    nb_entity.data["url"] = entity["url"]
                if "user" in entity:
                    nb_entity.data["user"] = User(**entity["user"])
                msg.append(nb_entity)

                offset = entity["offset"] + entity["length"]
            if offset < len(obj[key]):
                msg.append(Entity("text", {"text": obj[key][offset:]}))
        for key in obj:
            if key == "photo":
                msg.append(File("photo", {"file": obj[key][-1]["file_id"]}))
            elif key in ["animation", "audio", "document", "video", "voice"]:
                msg.append(File(key, {key: obj[key]}))
            elif key in ["sticker", "video_note", "dice", "poll"]:
                msg.append(MessageSegment(key, {key: obj[key]}))
        return cls(msg)
