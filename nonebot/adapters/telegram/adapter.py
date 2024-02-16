import json
import asyncio
from typing_extensions import override
from typing import Any, Dict, List, Tuple, Union, Iterable, Optional, cast

import anyio
from pydantic.main import BaseModel
from pydantic.json import pydantic_encoder
from nonebot.utils import escape_tag, logger_wrapper
from nonebot.drivers import URL, Driver, Request, Response, HTTPServerSetup

from nonebot.adapters import Adapter as BaseAdapter

from .bot import Bot
from .event import Event
from .config import AdapterConfig
from .model import InputFile, InputMedia
from .exception import ActionFailed, NetworkError, ApiNotAvailable


def _escape_none(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}


log = logger_wrapper("Telegram")


class Adapter(BaseAdapter):
    @override
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.adapter_config = AdapterConfig(**self.config.model_dump())
        self.tasks: List[asyncio.Task] = []
        self.setup()

    @classmethod
    @override
    def get_name(cls) -> str:
        return "Telegram"

    async def __handle_update(self, bot: Bot, update: Dict[str, Any]):
        try:
            event = Event.parse_event(update)
        except Exception as e:
            log("ERROR", f"Error when parsing event {update}", e)
            return

        log(
            "DEBUG",
            escape_tag(
                str(event.model_dump(exclude_none=True, exclude={"telegram_model"}))
            ),
        )
        await bot.handle_event(event)

    async def __bot_pre_setup(self, bot: Bot):
        bot.username = (await bot.get_me()).username
        log("INFO", "Delete old webhook")
        await bot.delete_webhook()

    def setup_webhook(self, bot: Bot):
        @self.on_ready
        async def _():
            try:
                await self.__bot_pre_setup(bot)
                log("INFO", "Set new webhook")
                await bot.set_webhook(
                    url=f"{self.adapter_config.telegram_webhook_url}/telegram",
                    secret_token=bot.secret_token,
                )
                self.bot_connect(bot)
            except Exception as e:
                log("ERROR", f"Setup for bot {bot.self_id} failed", e)
                raise

    async def poll(self, bot: Bot):
        try:
            await self.__bot_pre_setup(bot)
            log("INFO", "Start poll")
            self.bot_connect(bot)
        except Exception as e:
            log("ERROR", f"Setup for bot {bot.self_id} failed", e)
            raise

        update_offset = None
        while True:
            try:
                updates = await bot.get_updates(offset=update_offset, timeout=30)
                if update_offset is not None:
                    for update in updates:
                        update_offset = update.update_id + 1
                        asyncio.create_task(
                            self.__handle_update(
                                bot, update.model_dump(by_alias=True, exclude_none=True)
                            )
                        )
                elif updates:
                    update_offset = updates[0].update_id
            except Exception as e:
                log("ERROR", f"Get updates for bot {bot.self_id} failed", e)

    def setup_polling(self, bot: Bot):
        @self.on_ready
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
                    asyncio.create_task(self.__handle_update(bot, update))
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
            bot = Bot(
                self,
                Bot.get_bot_id_by_token(bot_config.token),
                config=bot_config,
            )
            if bot_config.is_webhook:
                self.setup_webhook(bot)
            else:
                self.setup_polling(bot)

    @override
    async def _call_api(self, bot: Bot, api: str, **data) -> Any:
        # 将方法名称改为驼峰式
        api = api.split("_", maxsplit=1)[0] + "".join(
            s.capitalize() for s in api.split("_")[1:]
        )
        data = _escape_none(data)

        # 分离文件到 files
        files: Dict[str, Tuple[str, bytes]] = {}
        bytes_upload_count = 0

        async def process_input_file(file: Union[InputFile, str]) -> Optional[str]:
            """处理传过来的文件，如果文件被添加到 files 列表则返回文件名"""
            nonlocal bytes_upload_count
            filename = None

            if isinstance(file, tuple):
                filename = file[0]
                files[filename] = file
                return filename

            if isinstance(file, str):
                if await (path := anyio.Path(file)).exists():
                    file = await path.read_bytes()
                    filename = path.name
                else:
                    return None

            if not filename:
                filename = f"upload{bytes_upload_count}"
                bytes_upload_count += 1
            files[filename] = (filename, file)
            return filename

        # 多个文件
        if api == "sendMediaGroup":
            medias: Iterable[InputMedia] = data["media"]
            for media in medias:
                filename = await process_input_file(media.media)
                if filename:
                    media.media = f"attach://{filename}"
        # 对修改消息媒体消息的处理
        elif api == "editMessageMedia":
            media: InputMedia = data["media"]
            filename = await process_input_file(media.media)
            if filename:
                media.media = f"attach://{filename}"
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
            for key in (type, "thumbnail"):
                value = cast(Optional[Union[str, bytes]], data.pop(key, None))
                if value:
                    filename = await process_input_file(value)
                    data[key] = f"attach://{filename}" if filename else value

        # 最后处理 data 以符合 DataTypes
        for key in data:
            if not isinstance(data[key], str):
                data[key] = json.dumps(
                    data[key],
                    default=(
                        lambda o: (
                            o.model_dump(exclude_none=True)
                            if isinstance(o, BaseModel)
                            else pydantic_encoder(o)
                        )
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
