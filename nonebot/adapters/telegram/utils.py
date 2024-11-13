import base64
import struct
import binascii


def _decode_telegram_base64(string):
    """
    来自 [telethon](https://github.com/LonamiWebs/Telethon/blob/v1/telethon/utils.py#L1086)
    """
    return base64.urlsafe_b64decode(string + "=" * (len(string) % 4))


def _encode_telegram_base64(string):
    """
    来自 [telethon](https://github.com/LonamiWebs/Telethon/blob/v1/telethon/utils.py#L1102)
    """
    try:
        return base64.urlsafe_b64encode(string).rstrip(b"=").decode("ascii")
    except (binascii.Error, ValueError, TypeError):
        return None  # not valid base64, not valid ascii, not a string


def resolve_inline_message_id(inline_msg_id: str):
    """
    来自 [telethon](https://github.com/LonamiWebs/Telethon/blob/v1/telethon/utils.py#L1304)
    从 inline_msg_id 解析出 message_id, peer, dc_id, access_hash
    """
    _, _, pid, _ = struct.unpack("<iiiq", _decode_telegram_base64(inline_msg_id))
    return f"-100{-pid}" if pid > 0 else f"{pid}"
