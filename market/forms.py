from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class PredictionForm(FlaskForm):
    study_hours = FloatField('Study Hours Per Day', validators=[
        DataRequired(), NumberRange(min=0, max=24)])
    
    extracurricular_hours = FloatField('Extracurricular Hours Per Day', validators=[
        DataRequired(), NumberRange(min=0, max=24)])
    
    sleep_hours = IntegerField('Sleep Hours Per Day', validators=[
        DataRequired(), NumberRange(min=3, max=12)])
    
    social_hours = FloatField('Social Hours Per Day', validators=[
        DataRequired(), NumberRange(min=0, max=24)])
    
    physical_activity_hours = IntegerField('Physical Activity Hours Per Day', validators=[
        DataRequired(), NumberRange(min=0, max=24)])
    
    gpa = FloatField('GPA', validators=[DataRequired(), NumberRange(min=0, max=4.0)])
    
    stress_level = SelectField('Stress Level', choices=[
        ('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')
    ], validators=[DataRequired()])

    submit = SubmitField('Predict Performance')