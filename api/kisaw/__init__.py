from flask import Flask

import time

from .blueprints.articles import articles_bp


def create_app(config=None):
    app = Flask(__name__)

    if config is None:
        app.config.from_pyfile('settings.py')
    else:
        app.config.from_pyfile(config)

    app.register_blueprint(articles_bp, url_prefix='/api')
    
    return app
