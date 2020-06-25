from flask import Blueprint, request, make_response

from .auth import token_required

from ..db import db
from ..db.models import User
from ..db.schemas import UserSchema

from ..settings import JWT_SECRET

users_bp = Blueprint('users_bp', __name__)


@users_bp.route('/users', methods=('GET',))
@token_required
def index():
    users = User.query.all()

    if not users:
        return make_response({'msg': 'No users yet.'}), 204
    
    user_schema = UserSchema(many=True, exclude=('password', 'role_id'))
    serialized_result = user_schema.dump(users)
    
    return make_response({'users': serialized_result}), 200


@users_bp.route('/user/<int:id>', methods=('GET', 'POST', 'PUT', 'DELETE'))
@token_required
def user(id):
    user = User.query.get(id)
    if not user:
        return make_response({'msg': 'User not found.'}), 400
    
    if request.method == 'GET':
        user_schema = UserSchema(exclude=('password',))
        serialized_result = user_schema.dump(user)
        return make_response({'user': serialized_result}), 200
        
    elif request.method == 'PUT':
        request_data = request.get_json()

        keys = request_data.keys()

        if 'email' in keys:
            user.email = request_data['email']

        if 'username' in keys:
            user.username = request_data['username']

        if 'password' in keys:
            user.password = request_data['password']

        if 'first_name' in keys:
            user.first_name = request_data['first_name']

        if 'last_name' in keys:
            user.last_name = request_data['last_name']

        db.session.commit()
        return make_response({'msg': '{} updated.'.format(user.username)}), 202
    else:
        db.session.delete(user)
        db.session.commit()
        return make_response({'msg': '{} deleted.'.format(user.username)}), 202
