from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Email, Length, EqualTo

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

# Added these forms for login functionality
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    email_address = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email_address = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')