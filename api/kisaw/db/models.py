import bcrypt
from datetime import datetime
from sqlalchemy.orm import validates
from . import db

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow,
                           onupdate=datetime.utcnow)


class Role(BaseModel):
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    users = db.relationship('User', backref='role', lazy=True)    
    
class User(BaseModel):
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    photo = db.Column(db.String, nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)    
    articles = db.relationship('Article', backref='user', lazy=True)

    @validates('password')
    def hash_password(self, key, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def __repr__(self):
        return '<User %r>' % self.username


class Article(BaseModel):
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # This will be used to show or hide an article
    published = db.Column(db.Boolean)
    metadatas = db.relationship('ArticleMeta', backref='article', lazy=True)
    comments = db.relationship('Comment', backref='article', lazy=True)
    
    def __repr__(self):
        return '<Article %r>' % self.title

class ArticleMeta(BaseModel):
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    meta_title = db.Column(db.String, nullable=False)
    meta_banner = db.Column(db.String)


class Comment(BaseModel):
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    parent_id = db.Column(db.Integer, nullable=True, default=0)
    body = db.Column(db.Text)

    # This will be used to show or hide a comment
    published = db.Column(db.Boolean, default=True)


article_category = db.Table('article_category',
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class Category(BaseModel):
    title = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<Category %r>' % self,title


article_tag = db.Table('article_tag',
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Tag(BaseModel):
    name  = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
