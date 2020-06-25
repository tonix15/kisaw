import time
import click

from flask import Flask

from .db import db, ma, migrate
from .db.models import User

from .blueprints.auth import auth_bp
from .blueprints.articles import articles_bp
from .blueprints.category import category_bp
from .blueprints.roles import roles_bp
from .blueprints.users import users_bp


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

    @click.command('create-user')
    @click.option('--username', required=True)
    @click.option('--password', required=True)
    @click.option('--email', required=True)
    def create_user(email, username, password):
        user = User(email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()
        click.echo('Created user {}'.format(username))
    
    return app
