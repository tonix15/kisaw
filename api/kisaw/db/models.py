import bcrypt
from datetime import datetime
from sqlalchemy.orm import validates
from . import db

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,
                           onupdate=datetime.utcnow)


class User(BaseModel):
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    photo = db.Column(db.String, nullable=True)

    @validates('password')
    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def __repr__(self):
        return '<User %r>' % self.username


class Article(BaseModel):
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return '<Article %r>' % self.title
