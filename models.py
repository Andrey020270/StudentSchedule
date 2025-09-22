from flask_login import UserMixin
from extensions import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="participant")  # participant, organizer, admin

    # связь с событиями (только для участников)
    events = db.relationship('Event', backref='user', lazy=True)


class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    users = db.relationship('User', backref='group', lazy=True)


class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)


class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50), nullable=False)


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

    # исправлено: для MySQL используем Date и Time
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    stage = db.Column(db.String(100), nullable=True)  # этап олимпиады

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))

    subject = db.relationship('Subject')
    teacher = db.relationship('Teacher')
    room = db.relationship('Room')
