import pandas as pd
from xgboost import XGBRegressor
import joblib
import os

# 
def predict_performance(form_data):
    """
    A simple fake prediction function.
    Returns a score between 0-100 based on GPA and study hours.
    """
    gpa = form_data.get('GPA', 0)
    study_hours = form_data.get('Study_Hours_Per_Day', 0)

    base_score = min(gpa * 25, 100)
    study_bonus = min(study_hours * 1.5, 15)
    total_score = base_score + study_bonus
    return round(total_score, 1)