from marshmallow import Schema, fields



class PlainItemScheme(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class PlainStoreScheme(Schema):
    id = fields.Str(dump_only=True)
    name =fields.Str(required=True)


class PlainTagSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

class ItemUpdateScheme(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Str()


class ItemScheme(PlainItemScheme):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreScheme(), dump_only=True)
    tags = fields.Nested(PlainTagSchema(), dump_only=True)


class StoreScheme(PlainStoreScheme):
    items = fields.List(fields.Nested(PlainItemScheme()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class StoreupdateScheme(Schema):
    name = fields.Str()


class TagScheme(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreScheme(), dump_only=True)
    items= fields.Nested(PlainItemScheme(), dump_only=True)

class ItemTagScheme(Schema):
    mesage = fields.Str()
    items = fields.Nested(ItemScheme)
    tags = fields.Nested(TagScheme)

class UserScheme(Schema):
    id = fields.Int(dump_only=True) 
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True) #load_only para nunca devolver la password al cliente