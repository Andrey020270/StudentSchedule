import datetime

from flask import Flask
from werkzeug.security import generate_password_hash
from extensions import db
from models import User, Group, Subject, Teacher, Room, Event

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schedule.db'
app.config['SECRET_KEY'] = 'dummy_secret'

db.init_app(app)


GROUP_NAMES = [
    "Олимпиада по информатике",
    "Олимпиада по математике",
    "Олимпиада по физике",
    "Олимпиада по химии",
    "Олимпиада по биологии",
    "Олимпиада по русскому языку",
    "Олимпиада по английскому языку",
    "Олимпиада по истории",
    "Олимпиада по обществознанию",
    "Олимпиада по географии",
]

SUBJECT_NAMES = [
    "Информатика",
    "Математика",
    "Физика",
    "Химия",
    "Биология",
    "Русский язык",
    "Английский язык",
    "История",
    "Обществознание",
    "География",
]

TEACHER_NAMES = [
    "Иванов И.И.",
    "Петров П.П.",
    "Сидоров С.С.",
    "Смирнова О.А.",
    "Кузнецова Н.В.",
    "Морозов Д.А.",
    "Васильева Е.С.",
    "Николаев А.П.",
    "Федорова М.М.",
    "Волкова Т.И.",
]

ROOM_NUMBERS = [
    "Ауд. 101",
    "Ауд. 102",
    "Ауд. 201",
    "Ауд. 202",
    "Ауд. 203",
    "Ауд. 301",
    "Ауд. 302",
    "Ауд. 303",
    "Ауд. 401",
    "Актовый зал",
]

USER_DATA = [
    ("admin", "admin123", "admin", 0),
    ("bob", "bob123", "organizer", 0),
    ("svetlana", "svetlana123", "organizer", 1),
    ("alice", "alice123", "participant", 0),
    ("ivan", "ivan123", "participant", 1),
    ("maria", "maria123", "participant", 2),
    ("sergey", "sergey123", "participant", 3),
    ("elena", "elena123", "participant", 4),
    ("dmitry", "dmitry123", "participant", 5),
    ("anna", "anna123", "participant", 6),
]

EVENT_DATA = [
    ("Регистрация участников олимпиады", datetime.date(2025, 9, 25), datetime.time(9, 0), "Консультация", "alice", 0, 0, 0),
    ("Отборочный тур по информатике", datetime.date(2025, 9, 30), datetime.time(10, 0), "Отборочный", "alice", 0, 0, 1),
    ("Разбор задач по информатике", datetime.date(2025, 10, 1), datetime.time(15, 0), "Консультация", "alice", 0, 1, 2),
    ("Отборочный тур по математике", datetime.date(2025, 10, 2), datetime.time(9, 30), "Отборочный", "alice", 1, 1, 3),
    ("Консультация по математике", datetime.date(2025, 10, 3), datetime.time(14, 0), "Консультация", "alice", 1, 2, 4),
    ("Полуфинал по физике", datetime.date(2025, 10, 4), datetime.time(11, 0), "Полуфинал", "alice", 2, 2, 5),
    ("Практический тур по химии", datetime.date(2025, 10, 5), datetime.time(10, 30), "Полуфинал", "alice", 3, 3, 6),
    ("Теоретический тур по биологии", datetime.date(2025, 10, 6), datetime.time(12, 0), "Полуфинал", "alice", 4, 4, 7),
    ("Полуфинал по английскому языку", datetime.date(2025, 10, 7), datetime.time(13, 0), "Полуфинал", "alice", 6, 6, 8),
    ("Финал олимпиады по информатике", datetime.date(2025, 10, 8), datetime.time(10, 0), "Заключительный", "alice", 0, 0, 9),
    ("Апелляция по математике", datetime.date(2025, 10, 9), datetime.time(16, 0), "Консультация", "ivan", 1, 7, 3),
    ("Награждение победителей", datetime.date(2025, 10, 10), datetime.time(12, 30), "Заключительный", "maria", 8, 8, 9),
]


def hash_password(password):
    return generate_password_hash(password, method="pbkdf2:sha256")


with app.app_context():
    db.drop_all()
    db.create_all()

    groups = [Group(name=name) for name in GROUP_NAMES]
    subjects = [Subject(name=name) for name in SUBJECT_NAMES]
    teachers = [Teacher(name=name) for name in TEACHER_NAMES]
    rooms = [Room(number=number) for number in ROOM_NUMBERS]

    db.session.add_all(groups + subjects + teachers + rooms)

    users = [
        User(
            username=username,
            password=hash_password(password),
            role=role,
            group=groups[group_index],
        )
        for username, password, role, group_index in USER_DATA
    ]
    db.session.add_all(users)

    users_by_username = {user.username: user for user in users}

    events = [
        Event(
            title=title,
            date=event_date,
            time=event_time,
            stage=stage,
            user=users_by_username[username],
            subject=subjects[subject_index],
            teacher=teachers[teacher_index],
            room=rooms[room_index],
        )
        for title, event_date, event_time, stage, username, subject_index, teacher_index, room_index in EVENT_DATA
    ]
    db.session.add_all(events)

    db.session.commit()
    print("База SQLite успешно проинициализирована: группы=10, пользователи=10, предметы=10, преподаватели=10, аудитории=10, события=12.")
