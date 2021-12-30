from typing import Optional

from pydantic import BaseModel, Field


# priority: alias > origin
class Config(BaseModel):
    """
    telegram 配置类

    :配置项:

      - ``token`` / ``telegram_token``: telegram bot token
      - ``proxy`` / ``telegram_proxy``: 自定义代理
      - ``webhook_url`` / ``telegram_api_url``: WebHook 域名
      - ``polling_interval`` / ``telegram_polling_interval``: 拉取消息的间隔时间
      - ``api_server`` / ``telegram_api_server``: 自定义 API 服务器

    """

    token: str = Field(alias="telegram_token")
    proxy: Optional[str] = Field(default=None, alias="telegram_proxy")
    webhook_url: Optional[str] = Field(default=None, alias="telegram_webhook_url")
    polling_interval: float = Field(default=0.01, alias="telegram_polling_interval")
    api_server: str = Field(
        default="https://api.telegram.org/", alias="telegram_api_server"
    )

    class Config:
        extra = "ignore"
        allow_population_by_field_name = True
