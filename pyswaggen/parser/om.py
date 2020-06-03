from dataclasses import dataclass
from typing import List, Any


@dataclass
class PropertyType:
    name: str


@dataclass
class Primitive(PropertyType):
    type: str


@dataclass
class Ref:
    name: str


@dataclass
class Object:
    subclasses: List[Ref]
    properties: List[Primitive]

    inner_classes: List[Any]  # is an Object

    def __add__(self, obj):
        return Object(
            subclasses=self.subclasses + obj.subclasses,
            properties=self.properties + obj.properties,
            inner_classes=self.inner_classes + obj.inner_classes
        )

    def add_subclasses(self, subclasses: List[Ref]):
        return Object(
            subclasses=self.subclasses + subclasses,
            properties=self.properties,
            inner_classes=self.inner_classes
        )


@dataclass
class SchemaObj:
    name: str
    obj: Object

    def write_template(self) -> str:
        pass


@dataclass
class SwaggerDoc:
    schemas: dict  # of key=string, v=SchemaObj
