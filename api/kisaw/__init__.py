import time
import click

from flask import Flask

from .db import db, migrate
from .db.models import User

from .blueprints.articles import articles_bp


def create_app(config=None):
    app = Flask(__name__)

    if config is None:
        app.config.from_pyfile('settings.py')
    else:
        app.config.from_pyfile(config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(articles_bp, url_prefix='/api')

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
