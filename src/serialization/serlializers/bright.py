from marshmallow import Schema, fields


class HealthCheckSchema(Schema):
    name = fields.String()
    status = fields.String()
    node = fields.String()
    seconds_ago = fields.Integer()
    timestamp = fields.Integer()
