from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from controllers.student_controller import StudentController
from models.student_model import StudentModel
import os
import time
from werkzeug.utils import secure_filename

student_bp = Blueprint('students', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@student_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_students():
    if 'file' not in request.files:
        return jsonify({'error': 'No se proporcionó ningún archivo'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Tipo de archivo no permitido. Use .xlsx, .xls o .csv'}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    
    try:
        # Validar archivo
        valid_students, errors = StudentController.validate_excel_file(file_path)
        
        if errors:
            os.remove(file_path)
            return jsonify({
                'valid': False,
                'errors': errors,
                'valid_count': len(valid_students)
            }), 400
        
        if not valid_students:
            os.remove(file_path)
            return jsonify({
                'valid': False,
                'errors': [{'row': 0, 'field': 'file', 'value': '', 'message': 'No hay estudiantes válidos en el archivo'}],
                'valid_count': 0
            }), 400
        
        # Tiempo mínimo de espera (simular procesamiento)
        time.sleep(1)
        
        # Insertar estudiantes
        result = StudentController.insert_students(valid_students)
        
        os.remove(file_path)
        
        if result['errors']:
            return jsonify({
                'success': True,
                'inserted': result['inserted'],
                'errors': result['errors'],
                'message': f'Se insertaron {result["inserted"]} estudiantes con algunos errores'
            }), 200
        
        return jsonify({
            'success': True,
            'inserted': result['inserted'],
            'message': f'Se insertaron {result["inserted"]} estudiantes exitosamente'
        }), 200
        
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        return jsonify({'error': f'Error al procesar el archivo: {str(e)}'}), 500

@student_bp.route('/', methods=['GET'])
@jwt_required()
def get_students():
    students = StudentModel.get_all_students()
    return jsonify(students), 200

