from flask import Blueprint, render_template, session
from models import db
from models.quiz_scores import QuizScore
from models.user_progress import UserProgress
from routes.auth import login_required

progress_bp = Blueprint('progress', __name__, url_prefix='/progress')

@progress_bp.route('/')
@login_required
def index():
    user_id = session['user_id']
    
    # 1. Fetch full quiz attempt history
    quiz_history = QuizScore.query.filter_by(user_id=user_id).order_by(QuizScore.created_at.desc()).all()
    
    # 2. Compile chronologically ascending scores for Trend Chart (limit to last 10 attempts)
    trend_quizzes = QuizScore.query.filter_by(user_id=user_id).order_by(QuizScore.created_at.asc()).limit(10).all()
    trend_labels = [q.created_at.strftime('%d %b') for q in trend_quizzes]
    trend_data = [round((q.score / q.total_questions) * 100, 1) for q in trend_quizzes]
    
    # 3. Retrieve aggregated category progress stats for Subject Strength Chart
    category_stats = UserProgress.query.filter_by(user_id=user_id).all()
    subject_labels = [stat.category for stat in category_stats]
    subject_avgs = [round(stat.average_score, 1) for stat in category_stats]
    subject_counts = [stat.completed_count for stat in category_stats]

    # Calculate computed lists of strong/weak subjects
    strong_topics = [s.category for s in category_stats if s.average_score >= 70.0]
    weak_topics = [s.category for s in category_stats if s.average_score < 50.0]

    return render_template(
        'progress.html',
        quiz_history=quiz_history,
        trend_labels=trend_labels,
        trend_data=trend_data,
        subject_labels=subject_labels,
        subject_avgs=subject_avgs,
        subject_counts=subject_counts,
        strong_topics=strong_topics,
        weak_topics=weak_topics
    )
