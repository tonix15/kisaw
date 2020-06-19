from marshmallow import Schema, fields

class UserSchema(Schema):
    email = fields.Email()
    username = fields.Str()
    password = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    photo = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
