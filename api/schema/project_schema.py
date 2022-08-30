from marshmallow import Schema, fields
from .customer_schema import CustomerSchema

class ProjectSchema(Schema):
    id = fields.Int(dump_only=True)
    code = fields.Str()
    description = fields.Str()
    customer = fields.Nested(CustomerSchema)

project_schema = ProjectSchema()