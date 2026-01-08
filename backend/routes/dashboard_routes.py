from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models.student_model import StudentModel

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_statistics():
    stats = StudentModel.get_students_statistics()
    return jsonify(stats), 200

@dashboard_bp.route('/students', methods=['GET'])
@jwt_required()
def get_all_students():
    students = StudentModel.get_all_students()
    return jsonify(students), 200

