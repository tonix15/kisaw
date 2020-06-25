from flask import Blueprint, make_response, request

from .auth import token_required

from ..db import db
from ..db.models import Article
from ..db.schemas import ArticleSchema

articles_bp = Blueprint('articles_bp', __name__)


@articles_bp.route('/articles', methods=('GET',))
@token_required
def index():
    articles = Article.query.all()

    if not articles:
        return make_response({'msg': 'No articles yet.'}), 204

    article_schema = ArticleSchema(many=True)
    serialized_result = article_schema.dump(articles)
    return make_response({'articles': serialized_result}), 200


@articles_bp.route('/article', methods=('POST',))
@token_required
def new_article():
    request_data = request.get_json()

    if 'title' not in request_data or 'body' not in request_data or 'author_id' not in request_data:
        return make_response({'msg': 'Title, Article Content and Author Required'}), 400

    article = Article(title=request_data['title'], body=request_data['body'], author_id=request_data['author_id'])
    db.session.add(article)
    db.session.commit()
    
    return make_response({'msg': 'New Article added.'}), 201


@articles_bp.route('/article/<int:id>', methods=('GET',))
@token_required
def get_article(id):
    article = Article.query.get(id)

    if not article:
        return make_response({'msg': 'Article not found.'}), 400

    article_schema = ArticleSchema()
    serialized_result = article_schema.dump(article)
    return make_response({'article': serialized_result}), 200

    
@articles_bp.route('/article/<int:id>', methods=('PUT',))
@token_required
def update_article(id):
    article = Article.query.get(id)

    if not article:
        return make_response({'msg': 'Article not found.'}), 400
    
    request_data = request.get_json()

    if 'title' in request_data:
        article.title  = request_data['title']

    if 'body' in request_data:
        article.body = request_data['body']

    if 'author_id' in request_data:
        article.author_id = request_data['author_id']

    db.session.commit()
    return make_response({'msg': '{} updated.'.format(article.title)}), 202


@articles_bp.route('/article/<int:id>', methods=('DELETE',))
@token_required
def delete_article(id):
    article = Article.query.get(id)

    if not article:
        return make_response({'msg': 'Article not found.'}), 400
    
    db.session.delete(article)
    db.session.commit()
    return make_response({'msg': '{} deleted.'.format(article.title)}), 202
