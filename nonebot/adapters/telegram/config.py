from typing import List, Optional

from pydantic import Field, BaseModel


class BotConfig(BaseModel):
    """
    Telegram Bot 配置类

    :配置项:
      - ``token``: telegram bot token
      - ``api_server``: 自定义 API 服务器
      - ``webhook_url``: WebHook 域名
      - ``webhook_token``: WebHook secret_token

    """

    token: str
    api_server: str = "https://api.telegram.org/"
    webhook_url: Optional[str] = None
    webhook_token: Optional[str] = None

    class Config:
        extra = "ignore"
        allow_population_by_field_name = True


class AdapterConfig(BaseModel):
    """
    Telegram Adapter 配置类

    :配置项:

      - ``proxy``: 自定义代理
      - ``telegram_bots`` 机器人单独配置
    """

    proxy: Optional[str] = Field(default=None, alias="telegram_proxy")
    telegram_bots: List["BotConfig"] = []

    class Config:
        extra = "ignore"
        allow_population_by_field_name = True
