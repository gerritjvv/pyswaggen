from dataclasses import dataclass
from typing import List, Any

import yaml
from more_itertools import last

from pyswaggen.parser.om import Primitive, Ref, SchemaObj, SwaggerDoc, Object


def parse_ref(ref_val: str):
    return Ref(last(ref_val.split('/')))


def parse_to_python_type(v):
    if v == 'integer':
        return 'int'
    elif v == 'bool' or v == 'boolean':
        return 'bool'
    elif v == 'number':
        return 'float'
    else:
        return 'str'


def parse_property_value(body: dict) -> str:
    """
        ref: <reference val>
        or
        type: <string/integer/number/bool>
    """
    if '$ref' in body:
        return last(body['$ref'].split('/'))
    elif 'type' in body:
        return parse_to_python_type(body['type'])
    else:
        raise Exception(f"{body} not expected here")


def parse_properties(body: dict) -> Object:
    """
    from: properites:
        <name>:
           ref
        or
        <name>:
           type: <type>

        or
         allOf:
          - ref: <ref>
          - properties
    """

    inner_classes = []
    properties = []

    for k, v in body.items():
        if 'allOf' in v:
            inner_classes.append(parse_all_of(v['allOf']))
        else:
            properties.append(Primitive(name=k, type=parse_property_value(v)))

    return Object(inner_classes=inner_classes, properties=properties, subclasses=[])


def parse_all_of(body: List[Any]) -> Object:
    """
        allOf:
        body=>
            - ref: <ref>
            - properties: ...
    """
    obj = Object(properties=[], inner_classes=[], subclasses=[])
    subclasses = []

    for item in body:
        if 'properties' in item:
            obj = obj + parse_properties(item['properties'])
        elif '$ref' in item:
            subclasses.append(parse_ref(item['$ref']))
        else:
            raise Exception(f"Not expecting {item} in allOf body")

    return obj.add_subclasses(subclasses)


def parse_schema_obj(name: str, body: dict) -> SchemaObj:
    """
    Parse a schema in "schemas"
    """
    obj = Object(subclasses=[], properties=[], inner_classes=[])

    print(f"parse_schema_obj: {name}")
    if 'properties' in body:
        obj = obj + parse_properties(body['properties'])

    if 'allOf' in body:
        obj = obj + parse_all_of(body['allOf'])

    return SchemaObj(name=name, obj=obj)


def parse_schema(schemas: dict) -> dict:
    schema_objs = {}

    for k, v in schemas.items():
        schema_obj = parse_schema_obj(k, v)
        schema_objs[k] = schema_obj

    return schema_objs


def parse_swagger(doc: dict) -> SwaggerDoc:
    if 'components' in doc:
        components = doc['components']
        if 'schemas' in components:
            return SwaggerDoc(
                schemas=parse_schema(components['schemas'])
            )


def parse_swagger_file(file: str) -> SwaggerDoc:
    with open(file, 'r') as f:
        doc = dict(yaml.load(f.read(), Loader=yaml.FullLoader))
        return parse_swagger(doc)
