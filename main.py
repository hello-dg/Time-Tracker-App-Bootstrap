from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from sqlite3 import Date
from datetime import datetime, date, time


app = Flask(__name__)
app.secret_key = "SECRET_KEY_PLACEHOLDER"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///entries.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Lists for Category, Project, and Task dropdowns
Category_List = []
Project_List = []
Task_List = []


class Entry(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category: Mapped[str] = mapped_column(String(200), nullable=True)
    project: Mapped[str] = mapped_column(String(200), nullable=True)
    task: Mapped[str] = mapped_column(String(200), nullable=True)
    note: Mapped[str] = mapped_column(String(600), nullable=True)
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
    return render_template('index.html')


@app.route('/add-entry', methods=['GET', 'POST'])
def add_entry():
    category_data = request.form.get('category')
    project_data = request.form.get('project')
    task_data = request.form.get('task')
    note_data = request.form.get('note')
    date_data = request.form.get('date')
    start_time_data = str(request.form.get('start_time'))
    end_time_data = str(request.form.get('end_time'))

    new_entry = Entry(category=category_data, project=project_data, task=task_data, note=note_data, date=date_data, start_time=start_time_data, end_time=end_time_data)

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
    pass


@app.route('/add-category', methods=['GET', 'POST'])
def add_category():
    pass


@app.route('/delete/<int:category_name>')
def delete_category(category_name):
    pass


@app.route('/add-project', methods=['GET', 'POST'])
def add_project():
    pass


@app.route('/delete/<int:project_name>')
def delete_project(project_name):
    pass


@app.route('/add-task', methods=['GET', 'POST'])
def add_task():
    pass


@app.route('/delete/<int:task_name>')
def delete_task(task_name):
    pass


if __name__ == '__main__':
    app.run(debug=True)