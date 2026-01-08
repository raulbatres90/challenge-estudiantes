from flask import Blueprint, request, jsonify
from controllers.auth_controller import AuthController
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user_model import UserModel

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email y contraseña son requeridos'}), 400
    
    result, status_code = AuthController.login(email, password)
    return jsonify(result), status_code

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    result, status_code = AuthController.register(email, password)
    return jsonify(result), status_code

@auth_bp.route('/me', methods=['GET']) # Sirve para obtener los datos del usuario actual
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = UserModel.get_user_by_id(int(user_id))
    
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    return jsonify({
        'id': user['id'],
        'email': user['email']
    }), 200

