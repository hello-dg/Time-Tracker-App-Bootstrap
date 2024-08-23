from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
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
    id: db.Column(db.Integer, primary_key=True)
    category: db.Column(db.String(250), nullable=False)
    project: db.Column(db.String(250), nullable=False)
    task: db.Column(db.String(250), nullable=False)
    note: db.Column(db.String(600), nullable=False)
    tags: db.Column(db.String(400), nullable=False)
    billable: db.Column(db.Boolean, default=False)
    date: db.Column(db.Date, nullable=False)
    start_time: db.Column(db.Time, nullable=False)
    end_time: db.Column(db.Time, nullable=False)

    def __repr__(self):
        return f'<task {self.task}>'


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    pass


@app.route('/add-entry', methods=['GET', 'POST'])
def add_entry():
    pass


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
