from flask import Blueprint
import os


articles_bp = Blueprint('articles_bp', __name__)


@articles_bp.route('/articles')
def index():
    return {'msg': 'Articles Index'}
