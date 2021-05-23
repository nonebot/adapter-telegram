from typing import Optional

from pydantic import Field, BaseModel


# priority: alias > origin
class Config(BaseModel):
    """
    telegram 配置类

    :配置项:

      - ``token`` / ``telegram_token``: telegram bot token
      - ``api_server`` / ``telegram_api_server``: custom api server
    """
    token: Optional[str] = Field(default=None, alias="telegram_token")
    api_server: Optional[str] = Field(default="https://api.telegram.org/", alias="telegram_api_server")

    class Config:
        extra = "ignore"
        allow_population_by_field_name = True
