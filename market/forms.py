
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, SelectField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired, NumberRange, ValidationError, Regexp

class PredictionForm(FlaskForm):
    Student_Id = StringField(
        label='Student_Id',
        validators=[
            DataRequired(),
            Regexp(r'^\d+$', message="Only numbers are allowed."),
            Length(min=1, max=10, message="ID must be between 1 and 10 digits.")
        ],
        render_kw={"maxlength": 10, "placeholder": "Enter student ID"}
    )
    study_hours = DecimalField(label='Study Hours Per Day',
                              validators=[DataRequired(), NumberRange(min=0, max=24)],
                              default=3.0)
    extracurricular_hours = DecimalField(label='Extracurricular Hours Per Day', 
                                        validators=[DataRequired(), NumberRange(min=0, max=24)],
                                        default=2.0)
    sleep_hours = DecimalField(label='Sleep Hours Per Day', 
                              validators=[DataRequired(), NumberRange(min=3, max=12)],
                              default=7.0)
    social_hours = DecimalField(label='Social Hours Per Day', 
                               validators=[DataRequired(), NumberRange(min=0, max=24)],
                               default=2.0)
    physical_activity_hours = DecimalField(label='Physical Activity Hours Per Day', 
                                          validators=[DataRequired(), NumberRange(min=0, max=24)],
                                          default=1.0)
    stress_level = SelectField(label='Stress Level', 
                              choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')],
                              validators=[DataRequired()],
                              default='Medium')
    submit = SubmitField(label='Predict My Performance')
    
    def validate(self, extra_validators=None):
        if not super(PredictionForm, self).validate():
            return False
            
        # Additional validation - make sure total hours don't exceed 24
        total_hours = sum([
            float(self.study_hours.data or 0),
            float(self.extracurricular_hours.data or 0),
            float(self.sleep_hours.data or 0),
            float(self.social_hours.data or 0),
            float(self.physical_activity_hours.data or 0)
        ])
        
        if total_hours > 24:
            self.study_hours.errors.append('The total of all hours exceeds 24 hours per day')
            return False
            
        return True

class RegisterForm(FlaskForm):
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password_confirm = PasswordField(label='Confirm Password', validators=[EqualTo('password'), DataRequired()])
    role = SelectField('Role', choices=[('professor', 'Professor'), ('user', 'student'),('admin', 'Admin')], validators=[DataRequired()])
    student_id = StringField(label='Student ID', validators=[DataRequired(), Regexp(r'^\d+$', message="Only numbers are allowed.")])
    major = StringField(label='Major', validators=[DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')
