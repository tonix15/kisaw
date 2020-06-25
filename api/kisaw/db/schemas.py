from . import ma

from .models import Article, Category, Comment, Role, User

class RoleSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Role
        
    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
    
    id = ma.auto_field()
    email = ma.auto_field()
    username = ma.auto_field()
    password = ma.auto_field()
    first_name = ma.auto_field()
    last_name = ma.auto_field()
    photo = ma.auto_field()
    role_id = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()

class ArticleSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Article
    
    id = ma.auto_field()
    title = ma.auto_field()
    body = ma.auto_field()
    author_id = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()

class CategorySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Category
    
    id = ma.auto_field()
    title = ma.auto_field()
    description = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()

class CommentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Comment
        
    id = ma.auto_field()
    article_id = ma.auto_field()
    parent_id = ma.auto_field()
    body = ma.auto_field()
    published = ma.auto_field()
