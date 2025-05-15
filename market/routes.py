
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from market import db
from market.models import Student, Prediction, User
from market.forms import PredictionForm, RegisterForm, LoginForm
from datetime import datetime, timedelta
from market.predict import predict_performance
from werkzeug.security import generate_password_hash, check_password_hash
from flask import abort
from flask_login import current_user
from functools import wraps
# Create blueprint
main_bp = Blueprint('main', __name__)

def role_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.is_authenticated and current_user.role in roles:
                return f(*args, **kwargs)
            else:
                abort(403)  # Forbidden
        return decorated_function
    return wrapper
# Decorator to check if user is admin
@main_bp.route('/')
@main_bp.route('/home')
@login_required
@role_required('admin', 'professor', 'user')
def home():
    recent_predictions = Prediction.query.order_by(Prediction.date.desc()).limit(5).all()
    return render_template('home.html', recent_predictions=recent_predictions)

@main_bp.route('/predict_form', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'professor', 'user')
def predict_form():
    form = PredictionForm()
    if request.method == 'GET':
        return render_template('predict_form.html', form=form)
    else:  # POST request
        if form.validate_on_submit():
            try:
                # Get form data
                Student_Id = form.Student_Id.data
                study_hours = form.study_hours.data
                extracurricular = form.extracurricular_hours.data
                sleep_hours = form.sleep_hours.data
                social_hours = form.social_hours.data
                physical_activity = form.physical_activity_hours.data
                stress_level = form.stress_level.data
                student = Student.query.filter_by(Student_Id=Student_Id).first()
                if student is None:
                    flash("Student ID not found", "danger")
                    return render_template('predict_form.html', form=form)

                input_features = {
                    'Study_Hours_Per_Day': study_hours,
                    'Sleep_Hours_Per_Day': sleep_hours,
                    'Social_Hours_Per_Day': social_hours,
                    'Extracurricular_Hours_Per_Day': extracurricular,
                    'Physical_Activity_Hours_Per_Day': physical_activity,
                    'Stress_Level': stress_level
                }

                prediction_score = predict_performance(input_features)
                prediction_score = max(0, min(prediction_score, 4.0))

                # Determine performance level
                if prediction_score >= 3.5:
                    level = "Excellent" 
                elif prediction_score >= 3.0:
                    level = "Good"
                elif prediction_score >= 2.5:
                    level = "Average"
                else:
                    level = "Below Average"

                # Generate recommendations
                recommendations = []
                if study_hours < 2:
                    recommendations.append("Increase study time to at least 2 hours per day")
                if sleep_hours < 6 or sleep_hours > 9:
                    recommendations.append("Aim for 7–9 hours of sleep for optimal cognitive function")
                if prediction_score < 3.0:
                    recommendations.append("Work on improving academic performance through consistent study habits")
                if stress_level == 'High':
                    recommendations.append("Consider stress management techniques like meditation or talking to a counselor")
                    
                # Format recommendations as a single string if list is not empty
                recommendation_text = ". ".join(recommendations) if recommendations else "Keep up the good work!"
                if recommendations and not recommendation_text.endswith('.'):
                    recommendation_text += '.'

                # Save prediction
                prediction = Prediction(
                    Student_Id=Student_Id,
                    Study_Hours_Per_Day=study_hours,
                    Extracurricular_Hours_Per_Day=extracurricular,
                    Sleep_Hours_Per_Day=sleep_hours,
                    Social_Hours_Per_Day=social_hours,
                    Physical_Activity_Hours_Per_Day=physical_activity,
                    GPA=prediction_score,
                    Stress_Level=stress_level,
                    Predicted_Score=prediction_score,
                    Performance_Level=level,
                    Recommendation=recommendation_text
                )

                db.session.add(prediction)
                db.session.commit()

                prediction_data = {
                    'score': prediction_score,
                    'level': level,
                    'recommendation': recommendation_text,
                    'suggestions': recommendations
                }

                student_data = {
                    'study_hours': study_hours,
                    'extracurricular_hours': extracurricular,
                    'sleep_hours': sleep_hours,
                    'social_hours': social_hours,
                    'physical_activity_hours': physical_activity,
                    'predicted_gpa': prediction_score,
                    'stress_level': stress_level
                }

                return render_template('result.html', prediction=prediction_data, student_data=student_data)

            except Exception as e:
                flash(f"An error occurred: {e}", "danger")
                return render_template('predict_form.html', form=form)
        else:
            flash("Please fix form errors.", "danger")
            return render_template('predict_form.html', form=form)

# Route for backward compatibility - redirects to predict_form
@main_bp.route('/predict', methods=['POST'])
@login_required
@role_required('admin', 'professor', 'user')
def predict():
    return redirect(url_for('main.predict_form'))

@main_bp.route('/history')
@login_required
@role_required('admin', 'professor')
def history():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    level_filter = request.args.get('level', '')
    date_range = request.args.get('date_range', '')
    student_id = request.args.get('Student_Id','')
    query = Prediction.query

    if level_filter:
        query = query.filter(Prediction.Performance_Level == level_filter)

    if date_range:
        days = int(date_range)
        query = query.filter(Prediction.date >= datetime.now() - timedelta(days=days))
    if student_id!="":
        query = query.filter(Prediction.Student_Id == student_id)
    predictions = query.order_by(Prediction.date.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return render_template('history.html',
                           predictions=predictions.items,
                           page=page,
                           pages=predictions.pages)

@main_bp.route('/prediction/<int:id>')
@login_required
def view_prediction(id):
    prediction = Prediction.query.get_or_404(id)

    student_data = {
        'study_hours': prediction.Study_Hours_Per_Day,
        'extracurricular_hours': prediction.Extracurricular_Hours_Per_Day,
        'sleep_hours': prediction.Sleep_Hours_Per_Day,
        'social_hours': prediction.Social_Hours_Per_Day,
        'physical_activity_hours': prediction.Physical_Activity_Hours_Per_Day,
        'predicted_gpa': prediction.GPA,
        'stress_level': prediction.Stress_Level
    }

    suggestions = []
    if prediction.Recommendation:
        suggestions = [s + '.' if not s.endswith('.') else s for s in prediction.Recommendation.split('.') if s.strip()]

    prediction_data = {
        'score': prediction.Predicted_Score,
        'level': prediction.Performance_Level,
        'recommendation': prediction.Recommendation,
        'suggestions': suggestions
    }

    return render_template('result.html', prediction=prediction_data, student_data=student_data)

@main_bp.route('/about')
@login_required
def about():
    return render_template('about.html')

# Auth routes
@main_bp.route('/register', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def register():
    if current_user.is_authenticated and current_user.role != 'admin':
        return redirect(url_for('main.home'))
    
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            email_address=form.email_address.data,
            password_hash=hashed_password,
            role=form.role.data 
        )
        
        db.session.add(user)
        
        # Check if the role is 'user' (which represents a student in your form)
        if form.role.data == 'user':
            student_id = request.form.get('student_id')
            major = request.form.get('major')
            
            # Make sure we have the required student data
            if student_id and major:
                student = Student(
                    Student_Id=student_id,
                    Student_Name=form.email_address.data,
                    Major=major
                )
                db.session.add(student)
            else:
                flash("Student ID and Major are required for student accounts", "danger")
                return render_template('register.html', form=form)
        
        # Commit the transaction after all entities are added
        db.session.commit()
        flash("Account created successfully!", "success")
        return redirect(url_for('main.home'))
    
    return render_template('register.html', form=form)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page or url_for('main.home'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')
    
    return render_template('login.html', form=form)

@main_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))
