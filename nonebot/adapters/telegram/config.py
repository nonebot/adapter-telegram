from typing import List, Optional

from pydantic import Field, BaseModel


class BotConfig(BaseModel):
    """
    Telegram Bot 配置类

    :配置项:
      - ``token``: telegram bot token
      - ``webhook_url``: WebHook 域名
      - ``api_server``: 自定义 API 服务器
    """

    token: str
    webhook_url: Optional[str] = None
    api_server: str = "https://api.telegram.org/"

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
