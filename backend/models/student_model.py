from database.connection import db
from typing import List, Dict, Optional

class StudentModel:
    @staticmethod
    def create_student(nombre_estudiante, nue, anio_inicio, promedio_actual=None, 
                      promedio_graduacion=None, graduado=False):
        connection = db.get_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute(
                """INSERT INTO students 
                   (nombre_estudiante, nue, anio_inicio, promedio_actual, 
                    promedio_graduacion, graduado) 
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (nombre_estudiante, nue, anio_inicio, promedio_actual, 
                 promedio_graduacion, graduado)
            )
            connection.commit()
            return cursor.lastrowid
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def get_all_students():
        connection = db.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT * FROM students ORDER BY id DESC")
            return cursor.fetchall()
        finally:
            cursor.close()

    @staticmethod
    def get_student_by_nombre(nombre_estudiante):
        connection = db.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT * FROM students WHERE nombre_estudiante = %s", 
                          (nombre_estudiante,))
            return cursor.fetchone()
        finally:
            cursor.close()

    @staticmethod
    def get_student_by_nue(nue):
        connection = db.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT * FROM students WHERE nue = %s", (nue,))
            return cursor.fetchone()
        finally:
            cursor.close()

    @staticmethod
    def get_students_statistics():
        connection = db.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            stats = {}
            
            # Total de estudiantes
            cursor.execute("SELECT COUNT(*) as total FROM students")
            stats['total'] = cursor.fetchone()['total']
            
            # Estudiantes activos
            cursor.execute("SELECT COUNT(*) as active FROM students WHERE graduado = 0")
            stats['active'] = cursor.fetchone()['active']
            
            # Estudiantes graduados
            cursor.execute("SELECT COUNT(*) as graduated FROM students WHERE graduado = 1")
            stats['graduated'] = cursor.fetchone()['graduated']
            
            # Promedio por estado de graduación
            cursor.execute("""
                SELECT 
                    graduado,
                    AVG(promedio_actual) as avg_promedio
                FROM students 
                WHERE promedio_actual IS NOT NULL
                GROUP BY graduado
            """)
            stats['avg_by_status'] = cursor.fetchall()
            
            # Estudiantes por año
            cursor.execute("""
                SELECT 
                    anio_inicio,
                    COUNT(*) as count
                FROM students
                GROUP BY anio_inicio
                ORDER BY anio_inicio DESC
            """)
            stats['by_year'] = cursor.fetchall()
            
            return stats
        finally:
            cursor.close()

