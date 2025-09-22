import datetime

from flask import Flask
from werkzeug.security import generate_password_hash
from extensions import db
from models import User, Group, Subject, Teacher, Room, Event

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schedule.db'
app.config['SECRET_KEY'] = 'dummy_secret'

db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

    # Группы
    group1 = Group(name="Олимпиада по информатике")
    group2 = Group(name="Олимпиада по математике")
    db.session.add_all([group1, group2])

    # Пользователи
    admin = User(username="admin", password=generate_password_hash("admin123"), role="admin", group=group1)
    bob = User(username="bob", password=generate_password_hash("bob123"), role="organizer", group=group1)
    alice = User(username="alice", password=generate_password_hash("alice123"), role="participant", group=group2)

    db.session.add_all([admin, bob, alice])

    # Предметы
    subj_inf = Subject(name="Информатика")
    subj_math = Subject(name="Математика")
    teacher1 = Teacher(name="Иванов И.И.")
    teacher2 = Teacher(name="Петров П.П.")
    db.session.add_all([subj_inf, subj_math, teacher1, teacher2])

    # Аудитории
    room1 = Room(number="Ауд. 101")
    room2 = Room(number="Ауд. 202")
    db.session.add_all([room1, room2])

    # События
    event1 = Event(
        title="Отборочный тур",
        date=datetime.date(2025, 9, 30),
        time=datetime.time(10, 0),
        stage="Отборочный",
        user=alice,
        subject=subj_inf,
        teacher=teacher1,
        room=room1
    )
    event2 = Event(
        title="Заключительный тур",
        date=datetime.date(2025, 10, 5),
        time=datetime.time(12, 0),
        stage="Заключительный",
        user=alice,
        subject=subj_math,
        teacher=teacher2,
        room=room2
    )

    db.session.add_all([event1, event2])

    db.session.commit()
    print("✅ База SQLite успешно проинициализирована!")
