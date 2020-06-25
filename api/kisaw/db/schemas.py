from marshmallow import Schema, fields

class RoleSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class UserSchema(Schema):
    id = fields.Int()
    email = fields.Email()
    username = fields.Str()
    password = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    photo = fields.Str()
    role_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class ArticleSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    body = fields.Str()
    author_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class CategorySchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
