
from pyswaggen.parser.om import Ref
from pyswaggen.parser.parse import parse_to_python_type, parse_property_value, parse_properties, parse_all_of, \
    parse_swagger_file


def test_parse_python_type():
    types = [['integer', 'int'],
             ['number', 'float'],
             ['bool', 'bool'],
             ['boolean', 'bool'],
             ['str', 'str'],
             ['string', 'str']]

    for swagger_type, expected_type in types:
        assert parse_to_python_type(swagger_type) == expected_type


def test_parse_property_value():
    assert parse_property_value({'$ref': 'a/a/c'}) == 'c'

    assert parse_property_value({'type': 'bool'}) == 'bool'


def test_parse_properties():
    obj = parse_properties({
        'var1': {'$ref': 'a/a/c'},
        'var2': {'type': 'integer'},
        'var3': {'$ref': 'a/a/b'}
    })

    properties = obj.properties

    assert len(properties) == 3
    assert properties[0].name == 'var1'
    assert properties[0].type == 'c'
    assert properties[1].name == 'var2'
    assert properties[1].type == 'int'

    assert properties[2].name == 'var3'
    assert properties[2].type == 'b'


def test_parse_all_of():
    obj = parse_all_of([
        {'properties': {
            'var1': {'$ref': 'a/a/c'},
            'var2': {'type': 'integer'},
            'var3': {'$ref': 'a/a/b'}
        },
        },
        {'$ref': 'a/b/c'}
    ])

    properties = obj.properties
    subclasses = obj.subclasses

    assert len(properties) == 3
    assert len(subclasses) == 1

    assert subclasses == [Ref('c')]


def test_parse_swagger():
    schema = parse_swagger_file(
        'silo-gateway-api.yaml'
    )

    print(f"schema => {schema}")
