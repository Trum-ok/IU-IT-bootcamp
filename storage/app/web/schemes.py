from marshmallow import Schema, fields


class OkResponseSchema(Schema):
    status = fields.Str()
    data = fields.Dict()


class ErrorResponseSchema(Schema):
    status = fields.Str()
    message = fields.Str()
    data = fields.Dict()
