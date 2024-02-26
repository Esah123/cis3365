from app import db

class Facility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    classrooms = db.relationship('Classroom', backref='facility', lazy='dynamic')

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=False)
    teachers = db.relationship('Teacher', backref='classroom', lazy='dynamic')
    children = db.relationship('Child', backref='classroom', lazy='dynamic')

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)

class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
