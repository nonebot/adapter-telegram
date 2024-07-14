from enum import Enum
from typing import Any, Union, Literal, Annotated  # type: ignore

from pydantic import Field, BaseModel

DataType = Any


obj_schemas: dict[str, "Object"] = {}


class TypeEnum(str, Enum):
    integer = "Integer"
    array = "Array"
    string = "String"
    boolean = "Boolean"
    true = "True"
    float = "Float"
    float_number = "Float number"
    union = "Union"
    object = "Object"


class Integer(BaseModel):
    type: Literal[TypeEnum.integer]

    def to_annotation(self):
        return "int"


class Array(BaseModel):
    type: Literal[TypeEnum.array] = TypeEnum.array
    item: Union["Type", "Object", "Array"]

    def to_annotation(self):
        return f"list[{self.item.to_annotation()}]"


class String(BaseModel):
    type: Literal[TypeEnum.string]

    def to_annotation(self):
        return "str"


class Boolean(BaseModel):
    type: Literal[TypeEnum.boolean]

    def to_annotation(self):
        return "bool"


class LiteralTrue(BaseModel):
    type: Literal[TypeEnum.true]

    def to_annotation(self):
        return "Literal[True]"


class Float(BaseModel):
    type: Literal[TypeEnum.float, TypeEnum.float_number]

    def to_annotation(self):
        return "float"


class Union_(BaseModel):
    type: Literal[TypeEnum.union] = TypeEnum.union
    items: list[Union["Type", "Object"]]

    def to_annotation(self):
        return f"Union[{', '.join(i.to_annotation() for i in self.items)}]"


class Object(BaseModel):
    name: str
    type: TypeEnum = TypeEnum.object
    items: list[Union["Type", "Object"]] = Field(default_factory=list)
    properties: dict[str, "Type"] = Field(default_factory=dict)
    required: list[str] = Field(default_factory=list)

    def to_annotation(self):
        return self.name

    def property_annotation(self, name: str):
        annotation = self.properties[name].to_annotation()
        if name not in self.required:
            annotation = f"Optional[{annotation}]"
        return annotation


class Method(BaseModel):
    name: str
    params: dict[str, "Type"] = Field(default_factory=dict)
    required: list[str] = Field(default_factory=list)


Type = Annotated[
    Union[Boolean, Integer, Float, String, LiteralTrue],
    Field(discriminator="type"),
]
