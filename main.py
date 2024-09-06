from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from sqlite3 import Date
from datetime import datetime, date, time


app = Flask(__name__)
app.secret_key = "SECRET_KEY_PLACEHOLDER"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///time_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Lists for Category, Project, and Task dropdowns
Category_List = []
Project_List = []
Task_List = []


class Category(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=True, unique=True)


class Project(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=True, unique=True)


class Task(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=True, unique=True)


class Entry(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category: Mapped[str] = mapped_column(String(200), nullable=True)
    project: Mapped[str] = mapped_column(String(200), nullable=True)
    task: Mapped[str] = mapped_column(String(200), nullable=True)
    note: Mapped[str] = mapped_column(String(600), nullable=True)
    tags: Mapped[str] = mapped_column(String(400), nullable=True)
    billable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    date: Mapped[str] = mapped_column(String(200), nullable=True)
    start_time: Mapped[str] = mapped_column(String(200), nullable=True)
    end_time: Mapped[str] = mapped_column(String(20), nullable=True)


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
    today = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M')
    entries = Entry.query.order_by(Entry.date.desc(), Entry.start_time.desc()).all()
    category_data = Category.query.order_by(Category.name.asc()).all()
    projects = Project.query.order_by(Project.name.asc()).all()
    tasks = Task.query.order_by(Task.name.asc()).all()
    return render_template('index.html', entries=entries, categories=category_data, projects=projects, tasks=tasks, today=today, time=current_time, datetime=datetime, str=str)


@app.route('/add-entry', methods=['GET', 'POST'])
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

    new_entry = Entry(category=category_data, project=project_data, task=task_data, note=note_data, billable=billable_boolean, date=date_data, start_time=start_time_data, end_time=end_time_data)

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
def delete_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/categories')
def categories():
    category_data = Category.query.order_by(Category.name.asc()).all()
    return render_template('categories.html', categories=category_data)


@app.route('/add-category', methods=['GET', 'POST'])
def add_category():
    category_name = request.form.get('new-category')
    new_category = Category(name=category_name)

    try:
        db.session.add(new_category)
        db.session.commit()
        print("Added to database")
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")

    return redirect(url_for('categories'))


@app.route('/delete-category/<int:category_id>')
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('categories'))


@app.route('/projects')
def projects():
    project_data = Project.query.order_by(Project.name.asc()).all()
    return render_template('projects.html', projects=project_data)


@app.route('/add-project', methods=['GET', 'POST'])
def add_project():
    project_name = request.form.get('new-project')
    new_project = Project(name=project_name)

    try:
        db.session.add(new_project)
        db.session.commit()
        print("Added to database")
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")

    return redirect(url_for('projects'))


@app.route('/delete-project/<int:project_id>')
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('projects'))


@app.route('/tasks')
def tasks():
    task_data = Task.query.order_by(Task.name.asc()).all()
    return render_template('tasks.html', tasks=task_data)


@app.route('/add-task', methods=['GET', 'POST'])
def add_task():
    task_name = request.form.get('new-task')
    new_task = Task(name=task_name)

    try:
        db.session.add(new_task)
        db.session.commit()
        print("Added to database")
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")

    return redirect(url_for('tasks'))


@app.route('/delete-task/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('tasks'))


if __name__ == '__main__':
    app.run(debug=True)