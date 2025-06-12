from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
import webbrowser

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schedule.db'
db.init_app(app)


from models import User, Event

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
        new_user = User(username=username, password=hashed)
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

@app.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    from models import Subject, Teacher  # импорт внутри, чтобы избежать циклических проблем

    subjects = Subject.query.all()
    teachers = Teacher.query.all()

    selected_date = request.args.get('date')
    selected_subject = request.args.get('subject')
    selected_teacher = request.args.get('teacher')

    query = current_user.events

    # Фильтрация
    if selected_date:
        query = [e for e in query if e.date == selected_date]
    if selected_subject and selected_subject != 'all':
        query = [e for e in query if str(e.subject_id) == selected_subject]
    if selected_teacher and selected_teacher != 'all':
        query = [e for e in query if str(e.teacher_id) == selected_teacher]

    return render_template('schedule.html', events=query,
                           subjects=subjects, teachers=teachers,
                           selected_date=selected_date,
                           selected_subject=selected_subject,
                           selected_teacher=selected_teacher)



if __name__ == '__main__':
    url = "http://127.0.0.1:5000"
    print(f"Приложение доступно по адресу: {url}")
    webbrowser.open(url)
    app.run(debug=True)
