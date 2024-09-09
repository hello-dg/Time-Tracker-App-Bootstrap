from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, create_engine, MetaData
from sqlalchemy import ForeignKey
from typing import List
from sqlite3 import Date
from datetime import datetime, date, time
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = "SECRET_KEY_PLACEHOLDER"


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///time_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Configure Flask-Login's Login Manager
login_manager = LoginManager()
login_manager.init_app(app)


# Create a user_loader callback
# @login_manager.user_loader
# def load_user(user_id):
#     try:
#         user = db.get(User, user_id)
#         if user is None:
#             print(f"User with ID {user_id} not found.")
#             return None
#         return user
#     except Exception as e:
#         print(f"Error loading user: {e}")
#         return None


@login_manager.user_loader
def load_user(user_id):
    print("hello")
    return db.get_or_404(User, user_id)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False, unique=False)
    category: Mapped[List['Category']] = relationship('Category', backref='user', lazy=True)
    project: Mapped[List['Project']] = relationship('Project', backref='user', lazy=True)
    task: Mapped[List['Task']] = relationship('Task', backref='user', lazy=True)
    entry: Mapped[List['Entry']] = relationship('Entry', backref='user', lazy=True)


class Category(db.Model):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))


class Project(db.Model):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))


class Task(db.Model):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))


class Entry(db.Model):
    __tablename__ = "entries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category: Mapped[str] = mapped_column(String(200), nullable=False)
    project: Mapped[str] = mapped_column(String(200), nullable=False)
    task: Mapped[str] = mapped_column(String(200), nullable=False)
    note: Mapped[str] = mapped_column(String(600), nullable=True)
    tags: Mapped[str] = mapped_column(String(400), nullable=True)
    billable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    date: Mapped[str] = mapped_column(String(200), nullable=False)
    start_time: Mapped[str] = mapped_column(String(200), nullable=False)
    end_time: Mapped[str] = mapped_column(String(20), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    def __repr__(self):
        return f'<task {self.task}>'


# ADD TO DATABASE LATER
# tags: Mapped[str] = mapped_column(String(400), nullable=False)
# billable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
# duration_hours: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
# duration_decimal: Mapped[int] = mapped_column(Integer, nullable=True, default=0)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    today = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M')
    entries = Entry.query.order_by(Entry.date.desc(), Entry.start_time.desc()).all()
    category_data = Category.query.order_by(Category.name.asc()).all()
    project_data = Project.query.order_by(Project.name.asc()).all()
    task_data = Task.query.order_by(Task.name.asc()).all()
    return render_template('index.html', entries=entries, categories=category_data, projects=project_data, tasks=task_data, today=today, time=current_time, datetime=datetime, str=str, logged_in=current_user.is_authenticated)


@app.route('/add-entry', methods=['GET', 'POST'])
@login_required
def add_entry():
    category_data = request.form.get('category')
    project_data = request.form.get('project')
    task_data = request.form.get('task')
    note_data = request.form.get('note')
    billable_data = request.form.get('billable')
    billable_boolean = billable_data == 'on'
    date_data = request.form.get('date')
    start_time_data = str(request.form.get('start_time'))
    end_time_data = str(request.form.get('end_time'))

    new_entry = Entry(category=category_data, project=project_data, task=task_data, note=note_data, billable=billable_boolean, date=date_data, start_time=start_time_data, end_time=end_time_data, user_id=current_user.id)

    try:
        db.session.add(new_entry)
        db.session.commit()
        print("Added to database")
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")

    print(category_data)
    print(project_data)
    print(task_data)

    return redirect(url_for('index'))


@app.route('/delete/<int:entry_id>')
@login_required
def delete_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/categories')
@login_required
def categories():
    category_data = Category.query.order_by(Category.name.asc()).all()
    return render_template('categories.html', categories=category_data, logged_in=current_user.is_authenticated)


@app.route('/add-category', methods=['GET', 'POST'])
@login_required
def add_category():
    category_name = request.form.get('new-category')
    new_category = Category(name=category_name, user_id=current_user.id)

    try:
        db.session.add(new_category)
        db.session.commit()
        print("Added to database")
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")

    return redirect(url_for('categories'))


@app.route('/delete-category/<int:category_id>')
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('categories'))


@app.route('/projects')
@login_required
def projects():
    project_data = Project.query.order_by(Project.name.asc()).all()
    return render_template('projects.html', projects=project_data, logged_in=current_user.is_authenticated)


@app.route('/add-project', methods=['GET', 'POST'])
@login_required
def add_project():
    project_name = request.form.get('new-project')
    new_project = Project(name=project_name, user_id=current_user.id)

    try:
        db.session.add(new_project)
        db.session.commit()
        print("Added to database")
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")

    return redirect(url_for('projects'))


@app.route('/delete-project/<int:project_id>')
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('projects'))


@app.route('/tasks')
@login_required
def tasks():
    task_data = Task.query.order_by(Task.name.asc()).all()
    return render_template('tasks.html', tasks=task_data, logged_in=current_user.is_authenticated)


@app.route('/add-task', methods=['GET', 'POST'])
@login_required
def add_task():
    task_name = request.form.get('new-task')
    new_task = Task(name=task_name, user_id=current_user.id)

    try:
        db.session.add(new_task)
        db.session.commit()
        print("Added to database")
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")

    return redirect(url_for('tasks'))


@app.route('/delete-task/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('tasks'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        result = db.session.execute(db.select(User).where(User.email == email))

        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )

        new_user = User(
            name=request.form.get('name'),
            email=request.form.get('email'),
            password=hash_and_salted_password
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for('index'))

    return render_template('register.html', logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # Find user by email entered.
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        if not user or not check_password_hash(user.password, password):
            flash("Incorrect username or password, please try again.")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('index'))


    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)