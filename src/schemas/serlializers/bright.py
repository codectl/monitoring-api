from marshmallow import Schema, fields


class HealthCheckSchema(Schema):
    name = fields.String()
    status = fields.String(attribute='status.name')
    node = fields.String()
    seconds_ago = fields.Integer()
    timestamp = fields.Integer()
    info = fields.String()
