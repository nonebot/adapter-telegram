from typing import Optional

from nonebot.exception import AdapterException
from nonebot.exception import ActionFailed as BaseActionFailed
from nonebot.exception import NetworkError as BaseNetworkError
from nonebot.exception import NoLogException as BaseNoLogException
from nonebot.exception import ApiNotAvailable as BaseApiNotAvailable


class TelegramAdapterException(AdapterException):
    def __init__(self):
        super().__init__("Telegram")


class NoLogException(BaseNoLogException, TelegramAdapterException):
    pass


class ActionFailed(BaseActionFailed, TelegramAdapterException):
    """
    :说明:
      API 请求返回错误信息。
    """

    def __init__(self, description: Optional[str] = None):
        super().__init__()
        self.description = description

    def __repr__(self):
        return f"<ActionFailed {self.description}>"

    def __str__(self):
        return self.__repr__()


class NetworkError(BaseNetworkError, TelegramAdapterException):
    """
    :说明:
      网络错误。
    """

    def __init__(self, msg: Optional[str] = None):
        super().__init__()
        self.msg = msg

    def __repr__(self):
        return f"<NetWorkError message={self.msg}>"

    def __str__(self):
        return self.__repr__()


class ApiNotAvailable(BaseApiNotAvailable, TelegramAdapterException):
    pass
