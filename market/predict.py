import pandas as pd
from xgboost import XGBRegressor
import joblib
import os

# data = pd.read_csv('student_performance_data.csv')

# Check if required columns exist
# cols_to_use = [
#     'Study_Hours_Per_Day',
#     'Extracurricular_Hours_Per_Day',
#     'Sleep_Hours_Per_Day',
#     'Social_Hours_Per_Day',
#     'Physical_Activity_Hours_Per_Day',
#     'GPA'
# ]

# for col in cols_to_use:
#     if col not in data.columns:
#         raise ValueError(f"Missing required column in CSV: {col}")

# if 'Performance_Score' not in data.columns:
#     raise ValueError("CSV file must contain 'Performance_Score' column for training.")

# X = data[cols_to_use]
# y = data['Performance_Score']

# # Train model
# model = XGBRegressor(n_estimators=200, learning_rate=0.1, max_depth=3)
# model.fit(X, y)

# # Save model
# joblib.dump(model, 'performance_model.pkl')

# # Prediction function using trained model
# def predict_performance(form_data):
#     df = pd.DataFrame([form_data])
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