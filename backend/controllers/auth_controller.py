from models.user_model import UserModel
from flask_jwt_extended import create_access_token

class AuthController:
    @staticmethod
    def login(email, password):
        user = UserModel.get_user_by_email(email)
        
        if not user:
            return {'error': 'Credenciales inválidas'}, 401
        
        if not UserModel.verify_password(user['password'], password):
            return {'error': 'Credenciales inválidas'}, 401
        
        access_token = create_access_token(identity=str(user['id']))
        
        return {
            'access_token': access_token,
            'user': {
                'id': user['id'],
                'email': user['email']
            }
        }, 200

    @staticmethod
    def register(email, password):
        if not email or not password:
            return {'error': 'Email y contraseña son requeridos'}, 400
        
        if len(password) < 6:
            return {'error': 'La contraseña debe tener al menos 6 caracteres'}, 400
        
        try:
            user_id = UserModel.create_user(email, password)
            return {'message': 'Usuario creado exitosamente', 'user_id': user_id}, 201
        except Exception as e:
            if 'Duplicate entry' in str(e):
                return {'error': 'El email ya está registrado'}, 400
            return {'error': 'Error al crear usuario'}, 500

