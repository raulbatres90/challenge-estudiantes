from database.connection import db
import bcrypt

class UserModel:
    @staticmethod
    def create_user(email, password):
        connection = db.get_connection()
        cursor = connection.cursor()
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        try:
            cursor.execute(
                "INSERT INTO users (email, password) VALUES (%s, %s)",
                (email, hashed_password.decode('utf-8'))
            )
            connection.commit()
            return cursor.lastrowid
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def get_user_by_email(email):
        connection = db.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            return cursor.fetchone()
        finally:
            cursor.close()

    @staticmethod
    def verify_password(hashed_password, password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def get_user_by_id(user_id):
        connection = db.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT id, email FROM users WHERE id = %s", (user_id,))
            return cursor.fetchone()
        finally:
            cursor.close()

