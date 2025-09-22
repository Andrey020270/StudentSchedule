import os
import webbrowser
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models import User, Event, Subject, Teacher

app = Flask(__name__)

# Конфигурация (MySQL, заглушки для PythonAnywhere)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dummy_secret')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'mysql+pymysql://user:password@localhost/olympiad_schedule'
)
db.init_app(app)

# Логин-менеджер
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('schedule'))
        flash('Неверный логин или пароль')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Пользователь уже существует')
            return redirect(url_for('register'))
        hashed = generate_password_hash(password)
        # новые пользователи всегда участники
        new_user = User(username=username, password=hashed, role="participant")
        db.session.add(new_user)
        db.session.commit()
        flash('Успешная регистрация. Войдите.')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/schedule', methods=['GET'])
@login_required
def schedule():
    subjects = Subject.query.all()
    teachers = Teacher.query.all()

    selected_date = request.args.get('date')
    selected_subject = request.args.get('subject')
    selected_teacher = request.args.get('teacher')

    # участник видит только свои события
    if current_user.role == "participant":
        query = current_user.events
    else:
        query = Event.query.all()

    # Фильтрация
    if selected_date:
        query = [e for e in query if str(e.date) == selected_date]
    if selected_subject and selected_subject != 'all':
        query = [e for e in query if str(e.subject_id) == selected_subject]
    if selected_teacher and selected_teacher != 'all':
        query = [e for e in query if str(e.teacher_id) == selected_teacher]

    return render_template('schedule.html', events=query,
                           subjects=subjects, teachers=teachers,
                           selected_date=selected_date,
                           selected_subject=selected_subject,
                           selected_teacher=selected_teacher)


# Пример защищённого маршрута для добавления событий (только организатор/админ)
@app.route('/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    if current_user.role not in ["organizer", "admin"]:
        flash("Недостаточно прав для добавления событий")
        return redirect(url_for('schedule'))

    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        time = request.form['time']
        stage = request.form['stage']
        subject_id = request.form['subject']
        teacher_id = request.form['teacher']
        room_id = request.form['room']
        user_id = request.form['user']

        new_event = Event(
            title=title,
            date=date,
            time=time,
            stage=stage,
            subject_id=subject_id,
            teacher_id=teacher_id,
            room_id=room_id,
            user_id=user_id
        )
        db.session.add(new_event)
        db.session.commit()
        flash("Событие успешно добавлено")
        return redirect(url_for('schedule'))

    subjects = Subject.query.all()
    teachers = Teacher.query.all()
    return render_template('add_event.html', subjects=subjects, teachers=teachers)


if __name__ == '__main__':
    url = "http://127.0.0.1:5000"
    print(f"Приложение доступно по адресу: {url}")
    webbrowser.open(url)
    app.run(host="0.0.0.0", port=5000, debug=True)
