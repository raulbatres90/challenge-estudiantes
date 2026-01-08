import mysql.connector
from mysql.connector import Error
from config import Config

class DatabaseConnection:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def get_connection(self):
        if self._connection is None or not self._connection.is_connected():
            try:
                self._connection = mysql.connector.connect(
                    host=Config.DB_HOST,
                    user=Config.DB_USER,
                    password=Config.DB_PASSWORD,
                    database=Config.DB_NAME,
                    charset='utf8mb4',
                    collation='utf8mb4_unicode_ci'
                )
            except Error as e:
                print(f"Error connecting to MySQL: {e}")
                raise
        return self._connection

    def close_connection(self):
        if self._connection and self._connection.is_connected():
            self._connection.close()
            self._connection = None

db = DatabaseConnection()

