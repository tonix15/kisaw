from flask import Blueprint, make_response, request

from kisaw.blueprints.auth import token_required

from kisaw.db import db
from kisaw.db.models import Comment
from kisaw.db.schemas import CommentSchema

comments_bp = Blueprint('comments_bp', __name__)


@comments_bp.route('/comments', methods=('GET',))
@token_required
def index():
    comments = Comment.query.all()

    if not comments:
        return make_response({'msg': 'No comments yet.'}), 204

    comment_schema = CommentSchema(many=True)
    serialized_result = comment_schema.dump(comments)
    return make_response({'comments': serialized_result}), 200


@comments_bp.route('/comment', methods=('POST',))
@token_required
def new_comment():
    request_data = request.get_json()

    if 'title' not in request_data or 'body' not in request_data or 'author_id' not in request_data:
        return make_response({'msg': 'Title, Comment Content and Author Required'}), 400

    comment = Comment(title=request_data['title'], body=request_data['body'], author_id=request_data['author_id'])
    db.session.add(comment)
    db.session.commit()
    
    return make_response({'msg': 'New Comment added.'}), 201


@comments_bp.route('/comment/<int:id>', methods=('GET',))
@token_required
def get_comment(id):
    comment = Comment.query.get(id)

    if not comment:
        return make_response({'msg': 'Comment not found.'}), 400

    comment_schema = CommentSchema()
    serialized_result = comment_schema.dump(comment)
    return make_response({'comment': serialized_result}), 200

    
@comments_bp.route('/comment/<int:id>', methods=('PUT',))
@token_required
def update_comment(id):
    comment = Comment.query.get(id)

    if not comment:
        return make_response({'msg': 'Comment not found.'}), 400
    
    request_data = request.get_json()

    if 'title' in request_data:
        comment.title  = request_data['title']

    if 'body' in request_data:
        comment.body = request_data['body']

    if 'author_id' in request_data:
        comment.author_id = request_data['author_id']

    db.session.commit()
    return make_response({'msg': '{} updated.'.format(comment.title)}), 202


@comments_bp.route('/comment/<int:id>', methods=('DELETE',))
@token_required
def delete_comment(id):
    comment = Comment.query.get(id)

    if not comment:
        return make_response({'msg': 'Comment not found.'}), 400
    
    db.session.delete(comment)
    db.session.commit()
    return make_response({'msg': '{} deleted.'.format(comment.title)}), 202
