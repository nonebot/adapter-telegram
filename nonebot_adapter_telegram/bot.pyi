from typing import Any, Dict, Iterable, Union, Optional

from nonebot.adapters import Bot as BaseBot

from .model import *

class Bot(BaseBot):
    async def get_me(self):
        """
        :说明:
          用于测试机器人 Token 的 API
        :返回:
          * ``User``: 机器人本身的 User
        """
        ...
    async def log_out(self): ...
    async def close(self): ...
    async def send_message(
        self,
        chat_id: Union[int, str],
        text: str,
        parse_mode: Optional[str],
        entities: Optional[Iterable[MessageEntity]],
        disble_web_page_preview: Optional[bool],
        disble_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def forward_message(
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        diable_notification: Optional[bool],
        message_id: int,
    ): ...
    async def copy_message(
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_id: int,
        caption: Optional[str],
        parse_mode: Optional[str],
        caption_entities: Optional[Iterable[MessageEntity]],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_photo(
        chat_id: Union[int, str],
        photo: Union[InputFile, str],
        caption: Optional[str],
        parse_mode: Optional[str],
        caption_entities: Optional[Iterable[MessageEntity]],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_audio(
        chat_id: Union[int, str],
        audio: Union[InputFile, str],
        caption: Optional[str],
        parse_mode: Optional[str],
        caption_entities: Optional[Iterable[MessageEntity]],
        duration: Optional[int],
        performer: Optional[str],
        title: Optional[str],
        thumb: Optional[Union[InputFile, str]],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_document(
        chat_id: Union[int, str],
        document: Union[InputFile, str],
        thumb: Optional[Union[InputFile, str]],
        caption: Optional[str],
        parse_mode: Optional[str],
        caption_entities: Optional[Iterable[MessageEntity]],
        disable_content_type_detection: Optional[bool],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_video(
        chat_id: Union[int, str],
        video: Union[InputFile, str],
        duration: Optional[int],
        width: Optional[int],
        height: Optional[int],
        thumb: Optional[Union[InputFile, str]],
        caption: Optional[str],
        parse_mode: Optional[str],
        caption_entities: Optional[Iterable[MessageEntity]],
        support_streaming: Optional[bool],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_animation(
        chat_id: Union[int, str],
        animation: Union[InputFile, str],
        duration: Optional[int],
        width: Optional[int],
        height: Optional[int],
        thumb: Optional[Union[InputFile, str]],
        caption: Optional[str],
        parse_mode: Optional[str],
        caption_entities: Optional[Iterable[MessageEntity]],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_voice(
        chat_id: Union[int, str],
        voice: Union[InputFile, str],
        caption: Optional[str],
        parse_mode: Optional[str],
        caption_entities: Optional[Iterable[MessageEntity]],
        duration: Optional[int],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_video_note(
        chat_id: Union[int, str],
        video_note: Union[InputFile, str],
        duration: Optional[int],
        length: Optional[int],
        thumb: Optional[Union[InputFile, str]],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_media_group(
        chat_id: Union[int, str],
        media: Iterable[
            Union[InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo]
        ],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
    ): ...
    async def send_location(
        chat_id: Union[int, str],
        latitude: float,
        longitude: float,
        horizontal_accurary: Optional[float],
        live_period: Optional[int],
        heading: Optional[int],
        proximity_alert_radius: Optional[int],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def edit_message_live_location(
        chat_id: Optional[Union[int, str]],
        message_id: Optional[int],
        inline_message_id: Optional[int],
        latitude: float,
        longitude: float,
        horizontal_accurary: Optional[float],
        heading: Optional[int],
        proximity_alert_radius: Optional[int],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def stop_message_live_location(
        chat_id: Optional[Union[int, str]],
        message_id: Optional[int],
        inline_message_id: Optional[int],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_venue(
        chat_id: Union[int, str],
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        foursquare_id: Optional[str],
        foursquare_type: Optional[str],
        google_place_id: Optional[str],
        google_place_type: Optional[str],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_contact(
        chat_id: Union[int, str],
        phone_number: str,
        first_name: str,
        last_name: Optional[str],
        vcard: Optional[str],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_poll(
        chat_id: Union[int, str],
        question: str,
        options: Iterable[str],
        is_anonymous: Optional[bool],
        type: Optional[str],
        allows_multiple_answers: Optional[bool],
        correct_option_id: Optional[int],
        explanation: Optional[str],
        explanation_parse_mode: Optional[str],
        explanation_entities: Optional[Iterable[MessageEntity]],
        open_period: Optional[int],
        close_date: Optional[int],
        is_closed: Optional[bool],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_dice(
        chat_id: Union[int, str],
        emoji: Optional[str],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_chat_action(
        chat_id: Union[int, str],
        action: str,
    ): ...
