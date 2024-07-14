from keyword import kwlist

from .model import Array, Method, Object, Union_, TypeEnum, obj_schemas


def gen_requires(schemas: dict[str, Object]):
    requires = {}
    for name, model in schemas.items():
        requires[name] = []

        for item in model.items:
            requires[name].append(item.name)

        for _, property in model.properties.items():
            if isinstance(property, Object):
                requires[name].append(property.name)
            elif isinstance(property, Array):
                while isinstance(property, Array):
                    property = property.item
                if isinstance(property, Object):
                    requires[name].append(property.name)
            elif isinstance(property, Union_):
                for item in property.items:
                    if isinstance(item, Object):
                        requires[name].append(item.name)
    return requires


def sort_models(models: list[Object], requires: dict[str, list[str]]) -> list[Object]:
    new_models = []
    for model in models:
        if model.name not in requires:
            continue
        _ = sort_models(
            [obj_schemas[model_name] for model_name in requires.pop(model.name)],
            requires,
        ) + [model]
        new_models.extend(_)
    return new_models


def gen_model(models: list[Object]) -> str:
    output = ""
    for model in sort_models(models, gen_requires(obj_schemas)):
        if model.type == TypeEnum.union:
            output += (
                f"{model.name} = {Union_(items=model.items).to_annotation()}\n\n\n"
            )
            continue
        output += f"class {model.to_annotation()}(BaseModel):\n"
        for name in model.properties:
            text = f"    {name}: {model.property_annotation(name)}"
            if name not in model.required:
                text = text + " = None"
            if name in kwlist:
                text = f'    {name}_: {model.property_annotation(name)} = Field(alias="{name}")'
                if name not in model.required:
                    text = f'    {name}_: {model.property_annotation(name)} = Field(default=None, alias="{name}")'
            output += text + "\n"
        if not model.properties:
            output += "    pass\n"
        output += "\n\n"
    return output


def gen_api(methods: list[Method]) -> str:
    output = "class API:\n"
    for method in methods:
        text = ""
        text += f"    async def {method.name}(\n"
        text += "        self,\n"
        for name in method.required:
            text += f"        {name}: {method.params[name].to_annotation()},\n"
        for name, type in method.params.items():
            if name not in method.required:
                text += f"        {name}: Optional[{type.to_annotation()}] = None,\n"
        output += text.removesuffix(",\n") + "): ... \n"  # type: ignore
    return output
