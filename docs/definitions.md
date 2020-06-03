

```
servers:
  - url: <text> e.g /v1
    description: <text>

components:
  schemas:
     <schema objects>
```


# parsing schema objects


```

<name>:
    properties:
          <name>:
             type: <type>

    allOf:
      - $ref: <ref>
      - type: object
        properties:
            <name>:
              type: <type>
```

Type: 

```
PropertyType()
PrimitiveEnum(Primitive)(enums=[vals])
Primitive(PropertyType)(value=<type string>)
Ref(PropertyType)(name=link)

```

Property:
```
Property(name=str, type=PropertyType)

Parse(dict):
    <name>:
        type: <type>

    or
    <name>
       allOf:
          <properties>
          
        
```

Properties:
```
Parse(d:dict):
   for k,v in d.items():
      Property.parse(name=k, v)
```  


