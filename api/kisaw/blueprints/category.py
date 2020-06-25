from flask import Blueprint, make_response, request

from .auth import token_required

from ..db import db
from ..db.models import Category
from ..db.schemas import CategorySchema

category_bp = Blueprint('category_bp', __name__)


@category_bp.route('/categories', methods=('GET',))
@token_required
def index():
    categories = Category.query.all()

    if not categories:
        return make_response({'msg': 'No categories yet.'}), 204

    categories_schema = CategorySchema(many=True)
    serialized_result = categories_schema.dump(categories)
    return make_response({'categories': serialized_result}), 200


@category_bp.route('/category', methods=('POST',))
@token_required
def new_category():
    request_data = request.get_json()

    if 'title' not in request_data:
        return make_response({'msg': 'Title Required'}), 400

    description = None
    if 'description' in request_data:
        description = request_data['description']

    category = Category(title=request_data['title'], description=description)
    db.session.add(category)
    db.session.commit()
    
    return make_response({'msg': 'New Category added.'}), 201


@category_bp.route('/category/<int:id>', methods=('GET',))
@token_required
def get_category(id):
    category = Category.query.get(id)

    if not category:
        return make_response({'msg': 'Category not found.'}), 400

    category_schema = CategorySchema()
    serialized_result = category_schema.dump(category)
    return make_response({'category': serialized_result}), 200

    
@category_bp.route('/category/<int:id>', methods=('PUT',))
@token_required
def update_category(id):
    category = Category.query.get(id)

    if not category:
        return make_response({'msg': 'Category not found.'}), 400
    
    request_data = request.get_json()

    if 'title' in request_data:
        category.title  = request_data['title']

    if 'description' in request_data:
        category.description = request_data['description']

    db.session.commit()
    return make_response({'msg': '{} updated.'.format(category.title)}), 202


@category_bp.route('/category/<int:id>', methods=('DELETE',))
@token_required
def delete_category(id):
    category = Category.query.get(id)

    if not category:
        return make_response({'msg': 'Category not found.'}), 400
    
    db.session.delete(category)
    db.session.commit()
    return make_response({'msg': '{} deleted.'.format(category.title)}), 202
