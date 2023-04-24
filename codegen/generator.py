from keyword import kwlist
from typing import Dict, List

from .model import Type, Array, Method, Object, Union_, obj_schemas


def update_models(schemas: Dict[str, Object]) -> Dict[str, Object]:
    models = {}
    for name, model in schemas.items():
        properties = {}
        for key, property in model.properties.items():
            if isinstance(property, Object):
                property = schemas[property.name]
            elif isinstance(property, Array):
                tmp = 0
                while isinstance(property, Array):
                    property = property.items
                    tmp += 1
                if isinstance(property, Object):
                    property = schemas[property.name]
                for _ in range(tmp):
                    property = Array(items=property)
            properties[key] = property
        model.properties = properties
        models[name] = model
    return models


def sort_models(schemas: Dict[str, Type]) -> Dict[str, Object]:
    models: Dict[str, Object] = {}

    for model in schemas.values():
        while isinstance(model, Array):
            model = model.items

        if isinstance(model, Union_):
            model = model.items

        if not isinstance(model, Object):
            continue

        if model.name in models:
            continue

        models.update(
            sort_models(
                {
                    k: v
                    for k, v in model.properties.items()
                    if k in model.required
                    and not (isinstance(v, Object) and v.name == model.name)
                }
            )
        )

        models[model.name] = model

    return models


def sort_models2(schemas: Dict[str, Type]) -> Dict[str, Object]:
    models: Dict[str, Object] = {}

    for model in schemas.values():
        while isinstance(model, Array):
            model = model.items

        if isinstance(model, Union_):
            model = model.items

        if not isinstance(model, Object):
            continue

        if model.name in models:
            continue

        models.update(
            sort_models(
                {
                    k: v
                    for k, v in model.properties.items()
                    if not (isinstance(v, Object) and v.name == model.name)
                }
            )
        )

        models[model.name] = model

    return models


def gen_model(models: List[Object]):
    print(
        """from typing import List, Union, Literal, Optional

from pydantic import Field, BaseModel"""
    )
    print("\n")
    for model in update_models(obj_schemas).values():
        print(f"class {model.to_annotation()}(BaseModel):")
        for name in model.properties:
            text = f"    {name}: {model.property_annotation(name)}"
            if name not in model.required:
                text = text + f" = None"
            if name in kwlist:
                text = f'    {name}_: {model.property_annotation(name)} = Field(alias="{name}")'
                if name not in model.required:
                    text = f'    {name}_: {model.property_annotation(name)} = Field(default=None, alias="{name}")'
            print(text)
        if not model.properties:
            print("    pass")
        print("\n")


def gen_api(methods: List[Method]):
    print(
        """from typing import Any, List, Union, Optional

from nonebot.adapters import Bot as BaseBot
from nonebot.adapters import Adapter as Adapter

from .event import Event
from .config import BotConfig
from .message import Message, MessageSegment
from .model import (
    InputFile,
    BotCommand,
    ForceReply,
    InputMedia,
    MenuButton,
    LabeledPrice,
    MaskPosition,
    MessageEntity,
    ShippingOption,
    BotCommandScope,
    ChatPermissions,
    InputMediaAudio,
    InputMediaPhoto,
    InputMediaVideo,
    InlineQueryResult,
    InputMediaDocument,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    PassportElementError,
    ChatAdministratorRights,
)

class API:"""
    )
    for method in methods:
        text = ""
        text += f"    async def {method.name}(\n"
        text += "        self,\n"
        for name in method.required:
            text += f"        {name}: {method.params[name].to_annotation()},\n"
        for name, type in method.params.items():
            if name not in method.required:
                text += f"        {name}: Optional[{type.to_annotation()}] = None,\n"
        print(text.removesuffix(",\n"))
        print("): ...")