import json
import asyncio
from typing import Any, Dict, List, Tuple, Union, Optional, cast, overload

import anyio
from pydantic.main import BaseModel
from nonebot.typing import overrides
from pydantic.json import pydantic_encoder
from nonebot.utils import escape_tag, logger_wrapper
from nonebot.drivers import URL, Driver, Request, Response, HTTPServerSetup

from nonebot.adapters import Adapter as BaseAdapter

from .bot import Bot
from .event import Event
from .model import InputMedia
from .config import AdapterConfig
from .exception import ActionFailed, NetworkError, ApiNotAvailable


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

    def setup_webhook(self, bot: Bot):
        @self.driver.on_startup
        async def _():
            try:
                bot.username = (await bot.get_me()).username
                log("INFO", "Delete old webhook")
                await bot.delete_webhook()
                log("INFO", "Set new webhook")
                await bot.set_webhook(
                    url=f"{self.adapter_config.telegram_webhook_url}/telegram",
                    secret_token=bot.secret_token,
                )
                self.bot_connect(bot)
            except Exception as e:
                log("ERROR", f"Setup for bot {bot.self_id} failed", e)

    async def poll(self, bot: Bot):
        try:
            bot.username = (await bot.get_me()).username
            log("INFO", "Delete old webhook")
            await bot.delete_webhook()
            log("INFO", "Start poll")
            self.bot_connect(bot)

            update_offset = None
            while True:
                try:
                    updates = await bot.get_updates(offset=update_offset, timeout=30)
                    if update_offset is not None:
                        for update in updates:
                            update_offset = update.update_id + 1
                            event = Event.parse_event(
                                update.dict(by_alias=True, exclude_none=True)
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
                            await bot.handle_event(event)
                    elif updates:
                        update_offset = updates[0].update_id
                except Exception as e:
                    log("ERROR", f"Get updates for bot {bot.self_id} failed", e)
        except Exception as e:
            log("ERROR", f"Setup for bot {bot.self_id} failed", e)

    def setup_polling(self, bot: Bot):
        @self.driver.on_startup
        async def _():
            self.tasks.append(asyncio.create_task(self.poll(bot)))

        @self.driver.on_shutdown
        async def _():
            for task in self.tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*self.tasks, return_exceptions=True)

    async def handle_http(self, request: Request) -> Response:
        token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        for bot in self.bots.values():
            bot = cast(Bot, bot)
            if bot.secret_token == token:
                if request.content:
                    update: dict = json.loads(request.content)
                    asyncio.create_task(bot.handle_event(Event.parse_event(update)))
                return Response(204)
        return Response(401)

    def setup(self) -> None:
        if list(filter(lambda b: b.is_webhook, self.adapter_config.telegram_bots)):
            self.setup_http_server(
                HTTPServerSetup(
                    URL("/telegram"),
                    "POST",
                    self.get_name(),
                    self.handle_http,
                )
            )
        for bot_config in self.adapter_config.telegram_bots:
            bot = Bot(self, bot_config)
            if bot_config.is_webhook:
                self.setup_webhook(bot)
            else:
                self.setup_polling(bot)

    @overload
    async def __read_file(self, file: bytes) -> Tuple[None, bytes]:
        ...

    @overload
    async def __read_file(self, file: str) -> Optional[Tuple[str, bytes]]:
        ...

    async def __read_file(self, file):
        if isinstance(file, bytes):
            return None, file
        if isinstance(file, str) and await (path := anyio.Path(file)).is_file():
            return path.name, await path.read_bytes()
        return None

    @overrides(BaseAdapter)
    async def _call_api(self, bot: Bot, api: str, **data) -> Any:
        # 将方法名称改为驼峰式
        api = api.split("_", maxsplit=1)[0] + "".join(
            s.capitalize() for s in api.split("_")[1:]
        )
        data = _escape_none(data)

        # 分离文件到 files
        files: Dict[str, Tuple[str, bytes]] = {}

        # 多个文件
        if api == "sendMediaGroup":
            medias = [
                x.dict() if isinstance(x, InputMedia) else x for x in data["media"]
            ]
            upload_bytes_count = 0
            for media in medias:
                # 需要处理 bot.send 传过来的 bytes media 和 filename
                file: Union[str, bytes] = media["media"]
                filename = cast(Optional[str], media.pop("filename", None))
                file_data = await self.__read_file(file)

                if file_data:
                    name, value = file_data
                    if filename:
                        name = filename
                    if not name:
                        name = f"upload{upload_bytes_count}"
                        upload_bytes_count += 1

                    files[name] = (name, value)
                    media["media"] = f"attach://{name}"

        # 单个文件
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
            filename = cast(Optional[str], data.pop("filename", None))

            for key in (type, "thumbnail"):
                value = cast(Optional[Union[str, bytes]], data.pop(key, None))
                if value:
                    file_data = await self.__read_file(value)
                    if file_data:
                        name, value = file_data
                        files[key] = ((filename if key == type else name) or key, value)
                    else:
                        data[key] = value

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

        log("DEBUG", f"Calling API <y>{api}</y>")
        request = Request(
            "POST",
            f"{bot.bot_config.api_server}bot{bot.bot_config.token}/{api}",
            data=data if files else None,
            json=data if not files else None,
            files=files,  # type: ignore
            proxy=self.adapter_config.proxy,
        )
        try:
            response = await self.request(request)
        except Exception as e:
            raise NetworkError("HTTP request failed") from e

        if not response.content:
            raise ValueError("Empty response")
        if 200 <= response.status_code < 300:
            return json.loads(response.content)["result"]
        if 400 <= response.status_code < 404:
            raise ActionFailed(json.loads(response.content)["description"])
        if response.status_code == 404:
            raise ApiNotAvailable
        raise NetworkError(
            f"HTTP request received unexpected {response.status_code} {response.content}",
        )
