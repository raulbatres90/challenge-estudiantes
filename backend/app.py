from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY

CORS(app, origins=['http://localhost:3000'], supports_credentials=True)
jwt = JWTManager(app)

from routes.auth_routes import auth_bp
from routes.student_routes import student_bp
from routes.dashboard_routes import dashboard_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(student_bp, url_prefix='/api/students')
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

