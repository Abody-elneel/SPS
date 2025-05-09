from market import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    email_address = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(60))

class Student(db.Model):
    Student_ID = db.Column(db.Integer, primary_key=True)
    Study_Hours_Per_Day = db.Column(db.Float)
    Extracurricular_Hours_Per_Day = db.Column(db.Float)
    Sleep_Hours_Per_Day = db.Column(db.Integer)
    Social_Hours_Per_Day = db.Column(db.Float)
    Physical_Activity_Hours_Per_Day = db.Column(db.Integer)
    GPA = db.Column(db.Float)
    Stress_Level = db.Column(db.String)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Study_Hours_Per_Day = db.Column(db.Float)
    Extracurricular_Hours_Per_Day = db.Column(db.Float)
    Sleep_Hours_Per_Day = db.Column(db.Integer)
    Social_Hours_Per_Day = db.Column(db.Float)
    Physical_Activity_Hours_Per_Day = db.Column(db.Integer)
    GPA = db.Column(db.Float)
    Predicted_Score = db.Column(db.Float, nullable=False)
    Performance_Level = db.Column(db.String(20), nullable=False)
    Recommendation = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)