from typing import List, Optional

from pydantic import Field, BaseModel
from nonebot.compat import PYDANTIC_V2, ConfigDict


class BotConfig(BaseModel):
    """
    Telegram Bot 配置类

    :配置项:
      - ``token``: telegram bot token
      - ``api_server``: 自定义 API 服务器
      - ``is_webhook``: 是否使用 webhook

    """

    token: str
    api_server: str = "https://api.telegram.org/"
    is_webhook: bool = False

    if PYDANTIC_V2:
        model_config: ConfigDict = ConfigDict(
            extra = "ignore",
            populate_by_name = True,
        )
    else:
        class Config:
            extra = "ignore"
            allow_population_by_field_name = True


class AdapterConfig(BaseModel):
    """
    Telegram Adapter 配置类

    :配置项:

      - ``proxy``: 自定义代理
      - ``telegram_bots`` 机器人单独配置
      - ``telegram_webhook_url``: 自定义 webhook url
    """

    proxy: Optional[str] = Field(default=None, alias="telegram_proxy")
    telegram_bots: List["BotConfig"] = []
    telegram_webhook_url: Optional[str] = None

    if PYDANTIC_V2:
        model_config: ConfigDict = ConfigDict(
            extra = "ignore",
            populate_by_name = True,
        )
    else:
        class Config:
            extra = "ignore"
            allow_population_by_field_name = True
