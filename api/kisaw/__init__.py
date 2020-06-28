import time
import click

from flask import Flask

from kisaw.db import db, ma, migrate
from kisaw.db.models import User

from kisaw.blueprints.articles import articles_bp
from kisaw.blueprints.auth import auth_bp
from kisaw.blueprints.category import category_bp
from kisaw.blueprints.roles import roles_bp
from kisaw.blueprints.users import users_bp

def create_app(config=None):
    app = Flask(__name__)

    if config is None:
        app.config.from_pyfile('settings.py')
    else:
        app.config.from_pyfile(config)

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp, url_prefix='/api/v1')
    app.register_blueprint(articles_bp, url_prefix='/api/v1')
    app.register_blueprint(category_bp, url_prefix='/api/v1')
    app.register_blueprint(roles_bp, url_prefix='/api/v1')
    app.register_blueprint(users_bp, url_prefix='/api/v1')

    return app
