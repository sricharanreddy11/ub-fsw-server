from flask import Blueprint, jsonify, request
from auth.models.index import User, db
from auth.utils.jwt import token_required, generate_jwt

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/info', methods=['GET'])
@token_required
def get_user(payload):
    user_id = payload.get('user_id')
    user = User.get_by_user_id(user_id=user_id)
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@auth_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user_id = data.get('user_id')
    username = data.get('username')
    device_id = data.get('device_id')

    if not user_id or not username:
        return jsonify({'error': 'user_id and username are required'}), 400

    user = User.get_by_user_id(user_id)

    if not user:
        try:
            user = User.create_user(user_id, username, device_id)
        except Exception as e:
            return jsonify({'error': 'User creation failed', 'details': str(e)}), 500
        
    generate_jwt_token = generate_jwt(user_id, device_id)
    return jsonify({'token': generate_jwt_token}), 200