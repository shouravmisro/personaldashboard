from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Single db instance shared by entire project
db = SQLAlchemy()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.DateTime, nullable=False)
    image_url = db.Column(db.String(255))

class ToDoTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_text = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50))
    priority = db.Column(db.Integer, default=1)
    deadline = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    linked_event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=True)

    external_data = db.Column(db.Text) 


from flask_sqlalchemy import SQLAlchemy

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_name = db.Column(db.String(100), nullable=False)
    frequency = db.Column(db.String(20))  # daily, weekly, monthly
    goal = db.Column(db.Integer, default=1)  # times per freq
    notes = db.Column(db.Text)

    # Relationship to HabitProgress with cascade delete
    daily_progress = db.relationship(
        "HabitProgress",
        cascade="all, delete-orphan",
        backref="habit",
        lazy='dynamic'
    )

class HabitProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    count = db.Column(db.Integer, default=0)


class WeatherPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_location = db.Column(db.String(100), unique=True)
    last_updated = db.Column(db.DateTime)
    weather_data = db.Column(db.Text)  # JSON string cached
