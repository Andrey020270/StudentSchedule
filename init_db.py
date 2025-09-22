from extensions import db
from app import app
from models import User, Group, Subject, Teacher, Room, Event
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()

    # Добавляем тестовые группы
    group1 = Group(name="Олимпиада по информатике")
    group2 = Group(name="Олимпиада по математике")
    db.session.add_all([group1, group2])

    # Добавляем пользователей с ролями
    admin = User(username="admin", password=generate_password_hash("admin123"), role="admin", group=group1)
    organizer = User(username="organizer", password=generate_password_hash("org123"), role="organizer", group=group1)
    participant = User(username="participant", password=generate_password_hash("part123"), role="participant", group=group2)

    db.session.add_all([admin, organizer, participant])

    # Добавляем предметы и преподавателей
    subj_inf = Subject(name="Информатика")
    subj_math = Subject(name="Математика")
    teacher1 = Teacher(name="Иванов И.И.")
    teacher2 = Teacher(name="Петров П.П.")
    db.session.add_all([subj_inf, subj_math, teacher1, teacher2])

    # Добавляем аудитории
    room1 = Room(number="Ауд. 101")
    room2 = Room(number="Ауд. 202")
    db.session.add_all([room1, room2])

    # Добавляем события (этапы олимпиады)
    event1 = Event(
        title="Отборочный тур",
        date="2025-09-30",
        time="10:00",
        stage="Отборочный",
        user=participant,
        subject=subj_inf,
        teacher=teacher1,
        room=room1
    )

    event2 = Event(
        title="Заключительный тур",
        date="2025-10-05",
        time="12:00",
        stage="Заключительный",
        user=participant,
        subject=subj_math,
        teacher=teacher2,
        room=room2
    )

    db.session.add_all([event1, event2])

    db.session.commit()
    print("База данных успешно инициализирована!")
