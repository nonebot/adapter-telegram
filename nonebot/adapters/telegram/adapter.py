import json
import asyncio
import pathlib
from typing import Any, List, Iterable, cast

import aiofiles
from nonebot.log import logger
from pydantic.main import BaseModel
from nonebot.typing import overrides
from nonebot.message import handle_event
from pydantic.json import pydantic_encoder
from nonebot.drivers import (
    URL,
    Driver,
    Request,
    Response,
    ForwardDriver,
    ReverseDriver,
    HTTPServerSetup,
)

from nonebot.adapters import Adapter as BaseAdapter
from nonebot.adapters.telegram.model import InputMedia

from .bot import Bot
from .event import Event
from .exception import NetworkError
from .config import BotConfig, AdapterConfig


class Adapter(BaseAdapter):
    @overrides(BaseAdapter)
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.adapter_config = AdapterConfig(**self.config.dict())
        self.tasks: List[asyncio.Task] = []
        self.setup()

    @classmethod
    @overrides(BaseAdapter)
    def get_name(cls) -> str:
        return "Telegram"

    def setup_webhook(self, bot_configs: List[BotConfig]):
        @self.driver.on_startup
        async def _():
            async def handle_http(request: Request) -> Response:
                if request.content:
                    message: dict = json.loads(request.content)
                    await handle_event(bot, Event.parse_event(message))
                return Response(204)

            for bot_config in bot_configs:
                bot = Bot(self, bot_config)
                logger.info("Delete old webhook")
                await self._call_api(bot, "delete_webhook")
                logger.info("Set new webhook")
                await self._call_api(
                    bot,
                    "set_webhook",
                    url=f"{bot.bot_config.webhook_url}/telegram/{bot.self_id}",
                )
                self.bot_connect(bot)
                setup = HTTPServerSetup(
                    URL(f"/telegram/{bot.self_id}"),
                    "POST",
                    self.get_name(),
                    handle_http,
                )
                self.setup_http_server(setup)

    def setup_polling(self, bot_configs: List[BotConfig]):
        @self.driver.on_startup
        async def _():
            async def poll(bot: Bot):
                logger.info("Delete old webhook")
                await self._call_api(bot, "delete_webhook")
                logger.info("Start poll")
                self.bot_connect(bot)

                update_offset = 0
                while True:
                    try:
                        message = (
                            await self._call_api(
                                bot, "get_updates", offset=update_offset
                            )
                        )["result"]
                        if update_offset:
                            for msg in message:
                                if msg["update_id"] > update_offset:
                                    update_offset = msg["update_id"]
                                    await handle_event(bot, Event.parse_event(msg))
                        elif message:
                            update_offset = message[0]["update_id"]
                    except Exception as e:
                        logger.error(e)
                    await asyncio.sleep(bot.bot_config.polling_interval)

            for bot_config in bot_configs:
                self.tasks.append(asyncio.create_task(poll(Bot(self, bot_config))))

        @self.driver.on_shutdown
        async def _():
            for task in self.tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*self.tasks, return_exceptions=True)

    def setup(self) -> None:
        if isinstance(self.driver, ForwardDriver):
            polling_bot_configs = []
            webhook_bot_configs = []

            for bot_config in self.adapter_config.telegram_bots:
                if bot_config.webhook_url:
                    if isinstance(self.driver, ReverseDriver):
                        webhook_bot_configs.append(bot_config)
                    else:
                        raise Exception
                else:
                    polling_bot_configs.append(bot_config)

            self.setup_webhook(webhook_bot_configs)
            self.setup_polling(polling_bot_configs)
        else:
            raise Exception

    @overrides(BaseAdapter)
    async def _call_api(self, bot: Bot, api: str, **data) -> Any:
        # 将方法名称改为驼峰式
        api = api.split("_", maxsplit=1)[0] + "".join(
            s.capitalize() for s in api.split("_")[1:]
        )

        # 分离文件到 files
        files = {}
        if api == "sendMediaGroup":
            upload_count = 0
            for media in data["media"]:
                media = cast(InputMedia, media)
                if isinstance(media.media, bytes):
                    files[f"upload{upload_count}"] = (
                        f"upload{upload_count}",
                        media.media,
                    )
                    media.media = f"attach://upload{upload_count}"
                else:
                    try:
                        async with aiofiles.open(media.media, "rb") as f:
                            files[pathlib.Path(media.media).name] = (
                                pathlib.Path(media.media).name,
                                await f.read(),
                            )
                        media.media = f"attach://{pathlib.Path(media.media).name}"
                    except:
                        pass
        else:
            for key, value in data.items():
                if isinstance(value, bytes):
                    files[key] = ("upload", value)
                elif isinstance(value, str) or not isinstance(value, Iterable):
                    try:
                        async with aiofiles.open(value, "rb") as f:
                            files[key] = (pathlib.Path(value).name, await f.read())
                    except:
                        pass
            for key in files:
                data.pop(key)

        # 最后处理 data 以符合 DataTypes
        for key in data:
            if (
                not isinstance(data[key], str)
                and isinstance(data[key], Iterable)
                or isinstance(data[key], BaseModel)
            ):
                data[key] = json.dumps(
                    data[key],
                    default=(
                        lambda o: o.dict(exclude_none=True)
                        if isinstance(o, BaseModel)
                        else pydantic_encoder(o)
                    ),
                )

        request = Request(
            "POST",
            f"{bot.bot_config.api_server}bot{bot.bot_config.token}/{api}",
            data=data if files else None,
            json=data if not files else None,
            files=files,
            proxy=self.adapter_config.proxy,
        )
        if isinstance(self.driver, ForwardDriver):
            try:
                response = await self.driver.request(request)
                if 200 <= response.status_code < 300:
                    if not response.content:
                        raise ValueError("Empty response")
                    result = json.loads(response.content)
                    return result
                raise NetworkError(
                    f"HTTP request received unexpected {response.status_code} {response.content}"
                )
            except NetworkError:
                raise
            except Exception as e:
                raise NetworkError("HTTP request failed") from e
