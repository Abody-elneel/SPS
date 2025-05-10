import pandas as pd
import os
import random

def predict_performance(form_data):
    """
    Predicts student performance based on the provided form data.
    
    Args:
        form_data (dict): Dictionary containing the student's metrics
            - GPA
            - Study_Hours_Per_Day
            - Sleep_Hours_Per_Day
            - Social_Hours_Per_Day
            - Extracurricular_Hours_Per_Day
            - Physical_Activity_Hours_Per_Day
            - Stress_Level
            
    Returns:
        float: Predicted performance score (0-100)
    """
    # Extract relevant features
    gpa = form_data.get('GPA', 0)
    study_hours = form_data.get('Study_Hours_Per_Day', 0)
    sleep_hours = form_data.get('Sleep_Hours_Per_Day', 0)
    stress_level = form_data.get('Stress_Level', 'Medium')
    
    # Base score comes from GPA (max 60 points)
    base_score = min(gpa * 15, 60)
    
    # Study hours bonus (max 20 points)
    study_bonus = min(study_hours * 2, 20)
    
    # Sleep factor (-10 to +10 points)
    # Optimal sleep is 7-8 hours
    sleep_factor = 0
    if sleep_hours < 6:
        sleep_factor = -10
    elif sleep_hours < 7:
        sleep_factor = -5
    elif sleep_hours <= 8:
        sleep_factor = 10
    elif sleep_hours <= 9:
        sleep_factor = 5
    else:
        sleep_factor = 0
        
    # Stress penalty
    stress_penalty = 0
    if stress_level == 'High':
        stress_penalty = -10
    elif stress_level == 'Medium':
        stress_penalty = -5
    
    # Calculate total score
    total_score = base_score + study_bonus + sleep_factor + stress_penalty
    
    # Add small random variation (±5 points)
    variation = random.uniform(-5, 5)
    total_score += variation
    
    # Ensure score is within 0-100 range
    total_score = max(0, min(total_score, 100))
    
    return round(total_score, 1)