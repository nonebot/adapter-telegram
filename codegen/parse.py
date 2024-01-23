from pyquery import PyQuery
from pydantic import parse_obj_as

from codegen.utils import pascal_to_snake

from .model import Type, Array, Method, Object, Union_, TypeEnum, obj_schemas


class Parser(object):
    def __init__(self, source: str) -> None:
        self.methods = []
        self.types = []

        skip = True
        for element in PyQuery(source)("div#dev_page_content").children().items():
            if skip:
                if element.is_("h3") and element.text() == "Getting updates":
                    skip = False
                continue
            if element.is_("h4") and " " not in element.text():
                if element.text()[0].isupper():
                    object = Object(name=element.text())
                    element = element.next()
                    while not (
                        element.is_("h4") or element.is_("h3") or element.is_("hr")
                    ):
                        if element.is_("blockquote"):
                            element = element.next()
                            continue

                        items = []
                        for item in element("ul li").items():
                            items.append(Object(name=item.text()))
                        if items:
                            object.type = TypeEnum.union
                            object.items = items

                        for item in element("tbody tr").items():
                            property = item("td").eq(0).text()
                            type = item("td").eq(1).text()
                            if item("td").eq(2).text()[:8] != "Optional":
                                object.required.append(property)
                            for _ in range(type.count("Array of ")):
                                if not isinstance(type, Array):
                                    try:
                                        type = parse_obj_as(
                                            Type,
                                            {"type": type.replace("Array of ", "")},
                                        )

                                    except:
                                        type = Object(
                                            name=type.replace("Array of ", "")
                                        )
                                type = Array(item=type)
                            if isinstance(type, str):
                                if " or " in type:
                                    type = type.split(" or ")
                                    items = []
                                    for t in type:
                                        try:
                                            t = parse_obj_as(
                                                Type,
                                                {"type": t},
                                            )
                                        except:
                                            t = Object(name=t)
                                        items.append(t)
                                    type = Union_(items=items)
                                else:
                                    try:
                                        type = parse_obj_as(Type, {"type": type})
                                    except:
                                        type = Object(name=type)
                            object.properties[property] = type
                        element = element.next()
                    self.types.append(object)
                    obj_schemas[object.name] = object
                else:
                    method = Method(name=pascal_to_snake(element.text()))
                    element = element.next()
                    while not (
                        element.is_("h4") or element.is_("h3") or element.is_("hr")
                    ):
                        for item in element("tbody tr").items():
                            param = item("td").eq(0).text()
                            type = item("td").eq(1).text()
                            if item("td").eq(2).text() == "Yes":
                                method.required.append(param)
                            for _ in range(type.count("Array of ")):
                                if not isinstance(type, Array):
                                    try:
                                        type = parse_obj_as(
                                            Type,
                                            {"type": type.replace("Array of ", "")},
                                        )
                                    except:
                                        type = Object(
                                            name=type.replace("Array of ", "")
                                        )
                                type = Array(item=type)
                            if isinstance(type, str):
                                if " or " in type:
                                    type = type.split(" or ")
                                    items = []
                                    for t in type:
                                        try:
                                            t = parse_obj_as(
                                                Type,
                                                {"type": t},
                                            )
                                        except:
                                            t = Object(name=t)
                                        items.append(t)
                                    type = Union_(items=items)
                                else:
                                    try:
                                        type = parse_obj_as(Type, {"type": type})
                                    except:
                                        type = Object(name=type)
                            method.params[param] = type
                        element = element.next()
                    self.methods.append(method)
