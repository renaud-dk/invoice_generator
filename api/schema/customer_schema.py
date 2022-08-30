from marshmallow import Schema, fields

class CustomerSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str()
    address = fields.Str()
    city = fields.Str()
    zip_code = fields.Integer(dump_only=True)
    country = fields.Str()
    vat = fields.Str()
    rate = fields.Float()

customer_schema = CustomerSchema()

