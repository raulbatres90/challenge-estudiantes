"""
Script para inicializar la base de datos y crear un usuario por defecto
"""
from database.connection import db
from models.user_model import UserModel
import mysql.connector
from config import Config

def init_database():
    """Crea las tablas si no existen"""
    try:
        # Connect without database first
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        cursor = connection.cursor()
        
        # Create database if not exists
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME} CHARACTER SET utf8mb4")
        cursor.execute(f"USE {Config.DB_NAME}")
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(150) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)
        
        # Create students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre_estudiante VARCHAR(150) UNIQUE NOT NULL,
                nue BIGINT UNIQUE NOT NULL,
                anio_inicio INT NOT NULL,
                promedio_actual DECIMAL(5,2),
                promedio_graduacion DECIMAL(5,2),
                graduado BOOLEAN
            )
        """)
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("Base de datos inicializada correctamente")
        return True
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        return False

def create_default_user():
    """Crea un usuario por defecto si no existe"""
    try:
        # Check if user exists
        user = UserModel.get_user_by_email('admin@test.com')
        if user:
            print("Usuario admin@test.com ya existe")
            return
        
        # Create default user
        UserModel.create_user('admin@test.com', 'admin123')
        print("Usuario por defecto creado:")
        print("Email: admin@test.com")
        print("Password: admin123")
    except Exception as e:
        print(f"Error al crear usuario por defecto: {e}")

if __name__ == '__main__':
    print("Inicializando base de datos...")
    if init_database():
        print("\nCreando usuario por defecto...")
        create_default_user()
        print("\n¡Inicialización completada!")

