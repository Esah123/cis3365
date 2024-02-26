from flask import Blueprint, request, jsonify, abort, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import Facility, Classroom, Teacher, Child
from datetime import timedelta

bp = Blueprint('api', __name__)
jwt = JWTManager()

@bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username == 'admin' and password == 'password':
        access_token = create_access_token(identity=username, expires_delta=timedelta(hours=1))
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

@bp.route('/facility', methods=['POST'])
@jwt_required()
def add_facility():
    data = request.json
    new_facility = Facility(name=data['name'])
    db.session.add(new_facility)
    db.session.commit()
    return jsonify({'message': 'Facility added successfully'}), 201

@bp.route('/facility', methods=['GET'])
@jwt_required()
def get_facilities():
    facilities = Facility.query.all()
    return jsonify([{'id': f.id, 'name': f.name} for f in facilities]), 200

@bp.route('/classroom', methods=['POST'])
@jwt_required()
def add_classroom():
    data = request.json
    new_classroom = Classroom(name=data['name'], capacity=data['capacity'], facility_id=data['facility_id'])
    db.session.add(new_classroom)
    db.session.commit()
    return jsonify({'message': 'Classroom added successfully'}), 201

@bp.route('/classroom', methods=['GET'])
@jwt_required()
def get_classrooms():
    classrooms = Classroom.query.all()
    return jsonify([{'id': c.id, 'name': c.name, 'capacity': c.capacity, 'facility_id': c.facility_id} for c in classrooms]), 200

@bp.route('/teacher', methods=['POST'])
@jwt_required()
def add_teacher():
    data = request.json
    new_teacher = Teacher(firstname=data['firstname'], lastname=data['lastname'], room_id=data['room_id'])
    db.session.add(new_teacher)
    db.session.commit()
    return jsonify({'message': 'Teacher added successfully'}), 201

@bp.route('/teacher', methods=['GET'])
@jwt_required()
def get_teachers():
    teachers = Teacher.query.all()
    return jsonify([{'id': t.id, 'firstname': t.firstname, 'lastname': t.lastname, 'room_id': t.room_id} for t in teachers]), 200

@bp.route('/child', methods=['POST'])
@jwt_required()
def add_child():
    data = request.json
    room_id = data['room_id']
    classroom = Classroom.query.get_or_404(room_id)
    
    current_children_count = Child.query.filter_by(room_id=room_id).count()
    current_teachers_count = Teacher.query.filter_by(room_id=room_id).count()
    
    max_children_allowed = current_teachers_count * 10
    
    if current_children_count < min(classroom.capacity, max_children_allowed):
        new_child = Child(firstname=data['firstname'], lastname=data['lastname'], age=data['age'], room_id=room_id)
        db.session.add(new_child)
        db.session.commit()
        return jsonify({'message': 'Child added successfully'}), 201
    else:
        return jsonify({'message': 'Adding child failed. Exceeds maximum children allowed for current teachers.'}), 400

@bp.route('/child', methods=['GET'])
@jwt_required()
def get_children():
    children = Child.query.all()
    return jsonify([{'id': ch.id, 'firstname': ch.firstname, 'lastname': ch.lastname, 'age': ch.age, 'room_id': ch.room_id} for ch in children]), 200

@bp.route('/facility/<int:id>', methods=['PUT'])
@jwt_required()
def update_facility(id):
    data = request.json
    facility = Facility.query.get_or_404(id)
    facility.name = data['name']
    db.session.commit()
    return jsonify({'message': 'Facility updated successfully'}), 200

@bp.route('/facility/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_facility(id):
    facility = Facility.query.get_or_404(id)
    db.session.delete(facility)
    db.session.commit()
    return jsonify({'message': 'Facility deleted successfully'}), 200

@bp.route('/classroom/<int:id>', methods=['PUT'])
@jwt_required()
def update_classroom(id):
    data = request.json
    classroom = Classroom.query.get_or_404(id)
    classroom.name = data['name']
    classroom.capacity = data['capacity']
    classroom.facility_id = data['facility_id']
    db.session.commit()
    return jsonify({'message': 'Classroom updated successfully'}), 200

@bp.route('/classroom/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_classroom(id):
    classroom = Classroom.query.get_or_404(id)
    db.session.delete(classroom)
    db.session.commit()
    return jsonify({'message': 'Classroom deleted successfully'}), 200

@bp.route('/teacher/<int:id>', methods=['PUT'])
@jwt_required()
def update_teacher(id):
    data = request.json
    teacher = Teacher.query.get_or_404(id)
    teacher.firstname = data['firstname']
    teacher.lastname = data['lastname']
    teacher.room_id = data['room_id']
    db.session.commit()
    return jsonify({'message': 'Teacher updated successfully'}), 200

@bp.route('/teacher/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    db.session.delete(teacher)
    db.session.commit()
    return jsonify({'message': 'Teacher deleted successfully'}), 200

@bp.route('/child/<int:id>', methods=['PUT'])
@jwt_required()
def update_child(id):
    data = request.json
    child = Child.query.get_or_404(id)
    child.firstname = data['firstname']
    child.lastname = data['lastname']
    child.age = data['age']
    child.room_id = data['room_id']
    db.session.commit()
    return jsonify({'message': 'Child updated successfully'}), 200

@bp.route('/child/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_child(id):
    child = Child.query.get_or_404(id)
    db.session.delete(child)
    db.session.commit()
    return jsonify({'message': 'Child deleted successfully'}), 200

# Initialize JWT with the Flask app somewhere in your application setup
# app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
# jwt.init_app(app)
