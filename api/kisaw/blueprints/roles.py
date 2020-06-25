from flask import Blueprint, request, make_response


from .auth import token_required

from ..db import db
from ..db.models import Role
from ..db.schemas import RoleSchema

from ..settings import JWT_SECRET

roles_bp = Blueprint('roles_bp', '__name__')


@roles_bp.route('/roles', methods=('GET',))
@token_required
def index():
    roles = Role.query.all()

    if not roles:
        return make_response({}), 204
    
    role_schema = RoleSchema(many=True)
    serialized_result = role_schema.dump(roles)
    
    return make_response({'roles': serialized_result}), 200

@roles_bp.route('/role', methods=('POST',))
@token_required
def new_role():
    request_data = request.get_json()

    if 'name' not in request_data:
        return make_response({'msg': 'Role name Required'}), 400

    description = None
    if 'description' in request_data:
        description = request_data['description']
    
    role = Role(name=request_data['name'], description=description)
    db.session.add(role)
    db.session.commit()
    
    return make_response({'msg': 'New Role added.'}), 201


@roles_bp.route('/role/<int:id>', methods=('GET',))
@token_required
def get_role(id):
    role = Role.query.get(id)

    if not role:
        return make_response({'msg': 'Role not found.'}), 400

    role_schema = RoleSchema()
    serialized_result = role_schema.dump(role)
    return make_response({'role': serialized_result}), 200

    
@roles_bp.route('/role/<int:id>', methods=('PUT',))
@token_required
def update_role(id):
    role = Role.query.get(id)

    if not role:
        return make_response({'msg': 'Role not found.'}), 400
    
    request_data = request.get_json()

    if 'name' in request_data:
        role.name  = request_data['name']

    if 'description' in request_data:
        role.description = request_data['description']
        
    db.session.commit()
    return make_response({'msg': '{} updated.'.format(role.name)}), 202


@roles_bp.route('/role/<int:id>', methods=('DELETE',))
@token_required
def delete_role(id):
    role = Role.query.get(id)

    if not role:
        return make_response({'msg': 'Role not found.'}), 400
    
    db.session.delete(role)
    db.session.commit()
    return make_response({'msg': '{} deleted.'.format(role.name)}), 202
