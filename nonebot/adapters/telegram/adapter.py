import json
import asyncio
import pathlib
from typing import Any, Dict, List, cast

from anyio import open_file
from pydantic.main import BaseModel
from nonebot.typing import overrides
from nonebot.message import handle_event
from pydantic.json import pydantic_encoder
from nonebot.utils import escape_tag, logger_wrapper
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

from .bot import Bot
from .event import Event
from .model import InputMedia
from .config import BotConfig, AdapterConfig
from .exception import (
    ActionFailed,
    NetworkError,
    ApiNotAvailable,
    TelegramAdapterException,
)


def _escape_none(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}


log = logger_wrapper("Telegram")


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
                try:
                    log("INFO", "Delete old webhook")
                    await bot.delete_webhook()
                    log("INFO", "Set new webhook")
                    await bot.set_webhook(
                        url=f"{bot.bot_config.webhook_url}/telegram/{bot.self_id}"
                    )

                    self.bot_connect(bot)
                    setup = HTTPServerSetup(
                        URL(f"/telegram/{bot.self_id}"),
                        "POST",
                        self.get_name(),
                        handle_http,
                    )
                    self.setup_http_server(setup)
                except Exception as e:
                    log("ERROR", f"Setup for bot {bot.self_id} failed", e)

    def setup_polling(self, bot_configs: List[BotConfig]):
        @self.driver.on_startup
        async def _():
            async def poll(bot: Bot):
                try:
                    log("INFO", "Delete old webhook")
                    await bot.delete_webhook()
                    log("INFO", "Start poll")
                    self.bot_connect(bot)

                    update_offset = None
                    while True:
                        try:
                            message = await bot.get_updates(
                                offset=update_offset, timeout=30
                            )
                            if update_offset is not None:
                                for msg in message:
                                    update_offset = msg.update_id + 1
                                    event = Event.parse_event(
                                        msg.dict(by_alias=True, exclude_none=True)
                                    )
                                    log(
                                        "DEBUG",
                                        escape_tag(
                                            str(
                                                event.dict(
                                                    exclude_none=True,
                                                    exclude={"telegram_model"},
                                                )
                                            )
                                        ),
                                    )
                                    await handle_event(bot, event)
                            elif message:
                                update_offset = message[0].update_id
                        except Exception as e:
                            log("ERROR", f"Get updates for bot {bot.self_id} failed", e)
                except Exception as e:
                    log("ERROR", f"Setup for bot {bot.self_id} failed", e)

            for bot_config in bot_configs:
                self.tasks.append(asyncio.create_task(poll(Bot(self, bot_config))))

        @self.driver.on_shutdown
        async def _():
            for task in self.tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*self.tasks, return_exceptions=True)

    def setup(self) -> None:
        polling_bot_configs = []
        webhook_bot_configs = []

        for bot_config in self.adapter_config.telegram_bots:
            if bot_config.webhook_url:
                webhook_bot_configs.append(bot_config)
            else:
                polling_bot_configs.append(bot_config)

        self.setup_webhook(webhook_bot_configs)
        self.setup_polling(polling_bot_configs)

    @overrides(BaseAdapter)
    async def _call_api(self, bot: Bot, api: str, **data) -> Any:
        # 将方法名称改为驼峰式
        api = api.split("_", maxsplit=1)[0] + "".join(
            s.capitalize() for s in api.split("_")[1:]
        )
        data = _escape_none(data)

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
                elif (file := pathlib.Path(media.media)).is_file():
                    async with await open_file(media.media, "rb") as f:
                        files[file.name] = (file.name, await f.read())
                    media.media = f"attach://{pathlib.Path(media.media).name}"
        elif api in (
            "sendPhoto",
            "sendAudio",
            "sendDocument",
            "sendVideo",
            "sendAnimation",
            "sendVoice",
            "sendVideoNote",
        ):
            type = api[4:].lower()
            for key in (type, "thumb"):
                value = data.pop(key, None)
                if isinstance(value, bytes):
                    files[key] = ("upload", value)
                elif (
                    isinstance(value, str)
                    and (file := pathlib.Path(str(value))).is_file()
                ):
                    async with await open_file(value, "rb") as f:
                        files[key] = (file.name, await f.read())

        # 最后处理 data 以符合 DataTypes
        for key in data:
            if not isinstance(data[key], str):
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
        try:
            response = await self.request(request)
            if response.content:
                if 200 <= response.status_code < 300:
                    return json.loads(response.content)["result"]
                elif 400 <= response.status_code < 404:
                    raise ActionFailed(json.loads(response.content)["description"])
                elif response.status_code == 404:
                    raise ApiNotAvailable
                raise NetworkError(
                    f"HTTP request received unexpected {response.status_code} {response.content}"
                )
            else:
                raise ValueError("Empty response")
        except TelegramAdapterException:
            raise
        except Exception as e:
            raise NetworkError("HTTP request failed") from e
