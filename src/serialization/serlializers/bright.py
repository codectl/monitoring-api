from marshmallow import Schema, fields


class HealthCheckSchema(Schema):
    name = fields.String()
    status = fields.String()
    node = fields.String()
    seconds_agp = fields.Integer()
    timestamp = fields.Integer()
    raw = fields.Raw()
