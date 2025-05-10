import pandas as pd
import joblib
import os

def predict_performance(form_data):
    """
    Enhanced prediction function that uses more input parameters.
    Returns a score between 0-100 based on all provided student metrics.
    """
    gpa = form_data.get('GPA', 0)
    study_hours = form_data.get('Study_Hours_Per_Day', 0)
    extracurricular = form_data.get('Extracurricular_Hours_Per_Day', 0)
    sleep_hours = form_data.get('Sleep_Hours_Per_Day', 0)
    social_hours = form_data.get('Social_Hours_Per_Day', 0)
    physical_activity = form_data.get('Physical_Activity_Hours_Per_Day', 0)
    stress_level = form_data.get('Stress_Level', 'Medium')
    
    # Base score from GPA (max 60 points)
    base_score = min(gpa * 15, 60)
    
    # Study habits bonus (max 15 points)
    study_bonus = min(study_hours * 1.5, 15)
    
    # Sleep quality bonus (max 10 points)
    # Optimal sleep is between 7-9 hours
    if 7 <= sleep_hours <= 9:
        sleep_bonus = 10
    elif 6 <= sleep_hours < 7 or 9 < sleep_hours <= 10:
        sleep_bonus = 7
    elif 5 <= sleep_hours < 6 or 10 < sleep_hours <= 11:
        sleep_bonus = 4
    else:
        sleep_bonus = 0
        
    # Physical activity bonus (max 5 points)
    physical_bonus = min(physical_activity * 2, 5)
    
    # Balance bonus (max 5 points for well-balanced activities)
    if study_hours > 0 and extracurricular > 0 and social_hours > 0 and physical_activity > 0:
        balance_bonus = 5
    else:
        balance_bonus = 0
        
    # Stress penalty
    if stress_level == 'High':
        stress_penalty = -5
    elif stress_level == 'Medium':
        stress_penalty = -2
    else:  # Low stress
        stress_penalty = 0
        
    # Calculate total score
    total_score = base_score + study_bonus + sleep_bonus + physical_bonus + balance_bonus + stress_penalty
    
    # Ensure score is between 0 and 100
    total_score = max(0, min(total_score, 100))
    
    return round(total_score, 1)