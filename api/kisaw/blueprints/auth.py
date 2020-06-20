import bcrypt
import datetime
import jwt

from flask import Blueprint, make_response, request

from functools import wraps

from ..db import db
from ..db.models import User

from ..settings import JWT_SECRET


auth_bp = Blueprint('auth_bp', __name__)

def token_required(f):
    @wraps(f)
    def verify_token(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return make_response({'msg': 'Token is required.'}), 401

        # Split into Bearer and token
        split = auth_header.split(' ')
        token = split[1] # retrieve the token part

        try:
            data = jwt.decode(token, JWT_SECRET)
        except:
            return make_response({'msg': 'Token is invalid.'}), 401
        return f(*args, **kwargs)
    
    return verify_token


@auth_bp.route('/register', methods=('POST',))
def register():
    request_data = request.get_json()
    
    user = User(email=request_data['email'], username=request_data['username'], password=request_data['password'])
    db.session.add(user)
    db.session.commit()

    return make_response({'msg': '{} added.'.format(user.username)}), 201


@auth_bp.route('/auth/login', methods=('POST',))
def login():
    request_data = request.get_json()

    # Require username and password
    if 'username' not in request_data or 'password' not in request_data:
        return make_response({'msg': 'Username and Password required.'}), 400

    user = User.query.filter_by(username=request_data['username']).first()

    # Make sure user exists
    if not user:
        return make_response({'msg': 'User not found.'}), 401

    # Authenticate user
    if bcrypt.checkpw(request_data['password'].encode('utf-8'), user.password):
        token_expiration = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        
        # Generate JWT Token
        payload = {'id': user.id, 'username': user.username, 'email': user.email, 'exp': token_expiration}
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')

        return make_response({
            'msg': 'Authenticated',
            'token': token.decode('utf-8')
        }), 200        

    return make_response({'msg': 'Authenticated Failed.'}), 401
