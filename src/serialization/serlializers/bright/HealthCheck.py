from marshmallow import Schema, fields


class HealthCheckSchema(Schema):
    status = fields.String()
