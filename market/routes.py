from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from market import db
from market.models import Student, Prediction, User
from market.forms import PredictionForm, RegisterForm, LoginForm
from datetime import datetime, timedelta
from market.predict import predict_performance
from werkzeug.security import generate_password_hash, check_password_hash

# Create blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/home')
def home():
    recent_predictions = Prediction.query.order_by(Prediction.date.desc()).limit(5).all()
    return render_template('home.html', recent_predictions=recent_predictions)

@main_bp.route('/predict_form')
def predict_form():
    form = PredictionForm()
    return render_template('predict_form.html', form=form)

@main_bp.route('/predict', methods=['POST'])
def predict():
    form = PredictionForm()
    if form.validate_on_submit():
        try:
            # Get form data
            study_hours = form.study_hours.data
            extracurricular = form.extracurricular_hours.data
            sleep_hours = form.sleep_hours.data
            social_hours = form.social_hours.data
            physical_activity = form.physical_activity_hours.data
            gpa = form.gpa.data
            stress_level = form.stress_level.data

            input_features = {
                'GPA': gpa,
                'Study_Hours_Per_Day': study_hours,
                'Sleep_Hours_Per_Day': sleep_hours,
                'Social_Hours_Per_Day': social_hours,
                'Extracurricular_Hours_Per_Day': extracurricular,
                'Physical_Activity_Hours_Per_Day': physical_activity,
                'Stress_Level': stress_level
            }

            prediction_score = predict_performance(input_features)
            prediction_score = max(0, min(prediction_score, 100))

            # Determine performance level
            if prediction_score >= 85:
                level = "Excellent"
            elif prediction_score >= 70:
                level = "Good"
            elif prediction_score >= 50:
                level = "Average"
            else:
                level = "Below Average"

            # Generate recommendations
            recommendations = []
            if study_hours < 2:
                recommendations.append("Increase study time to at least 2 hours per day.")
            if sleep_hours < 6 or sleep_hours > 9:
                recommendations.append("Aim for 7–9 hours of sleep for optimal cognitive function.")
            if gpa < 3.0:
                recommendations.append("Work on improving GPA through consistent study habits.")
            if stress_level == 'High':
                recommendations.append("Consider stress management techniques like meditation or talking to a counselor.")
                
            # Format recommendations as a single string if list is not empty
            recommendation_text = ". ".join(recommendations) if recommendations else "Keep up the good work!"
            if recommendations and not recommendation_text.endswith('.'):
                recommendation_text += '.'

            # Save prediction
            prediction = Prediction(
                Study_Hours_Per_Day=study_hours,
                Extracurricular_Hours_Per_Day=extracurricular,
                Sleep_Hours_Per_Day=sleep_hours,
                Social_Hours_Per_Day=social_hours,
                Physical_Activity_Hours_Per_Day=physical_activity,
                GPA=gpa,
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
                'gpa': gpa,
                'stress_level': stress_level
            }

            return render_template('result.html', prediction=prediction_data, student_data=student_data)

        except Exception as e:
            flash(f"An error occurred: {e}", "danger")
            return redirect(url_for('main.predict_form'))
    else:
        flash("Please fix form errors.", "danger")
        return redirect(url_for('main.predict_form'))

@main_bp.route('/history')
def history():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    level_filter = request.args.get('level', '')
    date_range = request.args.get('date_range', '')

    query = Prediction.query

    if level_filter:
        query = query.filter(Prediction.Performance_Level == level_filter)

    if date_range:
        days = int(date_range)
        query = query.filter(Prediction.date >= datetime.now() - timedelta(days=days))

    predictions = query.order_by(Prediction.date.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return render_template('history.html',
                           predictions=predictions.items,
                           page=page,
                           pages=predictions.pages)

@main_bp.route('/prediction/<int:id>')
def view_prediction(id):
    prediction = Prediction.query.get_or_404(id)

    student_data = {
        'study_hours': Student.Study_Hours_Per_Day,
        'extracurricular_hours': Student.Extracurricular_Hours_Per_Day,
        'sleep_hours': Student.Sleep_Hours_Per_Day,
        'social_hours': Student.Social_Hours_Per_Day,
        'physical_activity_hours': Student.Physical_Activity_Hours_Per_Day,
        'gpa': Student.GPA,
        'stress_level': Student.Stress_Level
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
def about():
    return render_template('about.html')

# Auth routes
@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            username=form.username.data,
            email_address=form.email_address.data,
            password_hash=hashed_password,
            role='user'
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('main.login'))
    
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