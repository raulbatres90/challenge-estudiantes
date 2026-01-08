from models.student_model import StudentModel
from typing import List, Dict
import pandas as pd
from datetime import datetime

class StudentController:
    @staticmethod
    def validate_excel_file(file_path: str) -> tuple[List[Dict], List[Dict]]:
        """
        Validates Excel file and returns (valid_students, errors)
        """
        errors = []
        valid_students = []
        current_year = datetime.now().year
        
        try:
            # Determinar el tipo de archivo y leer en consecuencia
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            
            # Verificar columnas requeridas
            required_columns = ['nombre_estudiante', 'anio_inicio', 'NUE']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                errors.append({
                    'row': 0,
                    'field': 'columns',
                    'value': ', '.join(missing_columns),
                    'message': f'Columnas faltantes: {", ".join(missing_columns)}'
                })
                return valid_students, errors
            
            # Obtener estudiantes existentes para verificaciones de unicidad
            existing_students = StudentModel.get_all_students()
            existing_nombres = {s['nombre_estudiante'] for s in existing_students}
            existing_nues = {s['nue'] for s in existing_students}
            
            for index, row in df.iterrows():
                row_num = index + 2  # +2 porque excel empieza en 1 y tenemos encabezado
                row_errors = []
                
                # Validando nombre_estudiante (único, string)
                nombre = str(row.get('nombre_estudiante', '')).strip()
                if not nombre or nombre == 'nan':
                    row_errors.append({
                        'row': row_num,
                        'field': 'nombre_estudiante',
                        'value': nombre,
                        'message': 'nombre_estudiante es requerido'
                    })
                elif nombre in existing_nombres:
                    row_errors.append({
                        'row': row_num,
                        'field': 'nombre_estudiante',
                        'value': nombre,
                        'message': f'nombre_estudiante "{nombre}" ya existe en la base de datos'
                    })
                
                # Validando anio_inicio (requerido, no mayor al año actual)
                anio_inicio = row.get('anio_inicio')
                if pd.isna(anio_inicio):
                    row_errors.append({
                        'row': row_num,
                        'field': 'anio_inicio',
                        'value': anio_inicio,
                        'message': 'anio_inicio es requerido'
                    })
                else:
                    try:
                        anio_inicio = int(float(anio_inicio))
                        if anio_inicio > current_year:
                            row_errors.append({
                                'row': row_num,
                                'field': 'anio_inicio',
                                'value': anio_inicio,
                                'message': f'anio_inicio ({anio_inicio}) no puede ser mayor al año actual ({current_year})'
                            })
                    except (ValueError, TypeError):
                        row_errors.append({
                            'row': row_num,
                            'field': 'anio_inicio',
                            'value': anio_inicio,
                            'message': 'anio_inicio debe ser un número válido'
                        })
                
                # Validando NUE (único, numérico)
                nue = row.get('NUE')
                if pd.isna(nue):
                    row_errors.append({
                        'row': row_num,
                        'field': 'NUE',
                        'value': nue,
                        'message': 'NUE es requerido'
                    })
                else:
                    try:
                        nue = int(float(nue))
                        if nue in existing_nues:
                            row_errors.append({
                                'row': row_num,
                                'field': 'NUE',
                                'value': nue,
                                'message': f'NUE {nue} ya existe en la base de datos'
                            })
                    except (ValueError, TypeError):
                        row_errors.append({
                            'row': row_num,
                            'field': 'NUE',
                            'value': nue,
                            'message': 'NUE debe ser un número válido'
                        })
                
                # Obteniendo estado para determinar si está graduado
                estado = str(row.get('estado', '')).strip().lower()
                graduado = estado == 'graduado'
                
                # Promedios - permitir valores decimales y valores vacíos
                promedio_actual = row.get('promedio_actual')
                promedio_graduacion = row.get('promedio_graduacion')
                
                try:
                    if pd.isna(promedio_actual) or promedio_actual == '' or str(promedio_actual).strip() == '':
                        promedio_actual = None
                    else:
                        promedio_actual = float(promedio_actual)
                except (ValueError, TypeError):
                    row_errors.append({
                        'row': row_num,
                        'field': 'promedio_actual',
                        'value': promedio_actual,
                        'message': 'promedio_actual debe ser un número válido (puede ser decimal)'
                    })
                    promedio_actual = None
                
                # promedio_graduacion puede ir vacío siempre
                try:
                    if pd.isna(promedio_graduacion) or promedio_graduacion == '' or str(promedio_graduacion).strip() == '':
                        promedio_graduacion = None
                    else:
                        promedio_graduacion = float(promedio_graduacion)
                except (ValueError, TypeError):
                    row_errors.append({
                        'row': row_num,
                        'field': 'promedio_graduacion',
                        'value': promedio_graduacion,
                        'message': 'promedio_graduacion debe ser un número válido (puede ser decimal) o estar vacío'
                    })
                    promedio_graduacion = None
                
                # Si está graduado y ambos promedios están presentes, deben ser iguales
                if graduado and promedio_actual is not None and promedio_graduacion is not None:
                    if abs(promedio_actual - promedio_graduacion) > 0.01:  # Permitir pequeñas diferencias de punto flotante
                        row_errors.append({
                            'row': row_num,
                            'field': 'promedio',
                            'value': f'actual: {promedio_actual}, graduacion: {promedio_graduacion}',
                            'message': f'Para estudiantes graduados, si ambos promedios están presentes, promedio_actual ({promedio_actual}) y promedio_graduacion ({promedio_graduacion}) deben ser iguales'
                        })
                
                # anio_fin puede ir vacío 
                
                if row_errors:
                    errors.extend(row_errors)
                else:
                    # Agregar a estudiantes válidos
                    valid_students.append({
                        'nombre_estudiante': nombre,
                        'nue': int(float(nue)),
                        'anio_inicio': int(float(anio_inicio)),
                        'promedio_actual': promedio_actual,
                        'promedio_graduacion': promedio_graduacion,
                        'graduado': graduado
                    })
                    # Agregar a conjuntos existentes para verificar duplicados dentro del archivo
                    existing_nombres.add(nombre)
                    existing_nues.add(int(float(nue)))
            
            return valid_students, errors
            
        except Exception as e:
            errors.append({
                'row': 0,
                'field': 'file',
                'value': '',
                'message': f'Error al leer el archivo: {str(e)}'
            })
            return valid_students, errors

    @staticmethod
    def insert_students(students: List[Dict]) -> Dict:
        """
        Inserts valid students into database
        """
        inserted = 0
        errors = []
        
        for student in students:
            try:
                StudentModel.create_student(
                    nombre_estudiante=student['nombre_estudiante'],
                    nue=student['nue'],
                    anio_inicio=student['anio_inicio'],
                    promedio_actual=student['promedio_actual'],
                    promedio_graduacion=student['promedio_graduacion'],
                    graduado=student['graduado']
                )
                inserted += 1
            except Exception as e:
                errors.append({
                    'student': student['nombre_estudiante'],
                    'error': str(e)
                })
        
        return {
            'inserted': inserted,
            'errors': errors
        }

