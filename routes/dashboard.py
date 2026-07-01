from flask import Blueprint, render_template, session, redirect, url_for
from models import db
from models.user import User
from models.quiz_scores import QuizScore
from models.user_progress import UserProgress
from models.chat_history import ChatHistory
from models.resume_reports import ResumeReport
from models.mock_interviews import MockInterview
from routes.auth import login_required

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))

    # Calculate statistics
    total_quizzes = QuizScore.query.filter_by(user_id=user_id).count()
    
    # Calculate average score percentage
    scores = QuizScore.query.filter_by(user_id=user_id).all()
    if scores:
        total_percent = sum((s.score / s.total_questions) * 100 for s in scores)
        avg_score = round(total_percent / len(scores), 1)
    else:
        avg_score = 0.0

    # Retrieve progress records
    progress_records = UserProgress.query.filter_by(user_id=user_id).all()
    strong_topics = [p.category for p in progress_records if p.average_score >= 70.0]
    weak_topics = [p.category for p in progress_records if p.average_score < 50.0]

    # Smart practice recommendation engine
    recommendations = []
    if weak_topics:
        for topic in weak_topics:
            if topic in ['Quantitative', 'Logical', 'Verbal']:
                recommendations.append({
                    'title': f"Strengthen {topic} Aptitude",
                    'description': f"Your average score is below 50%. Practice more timed MCQs in this module.",
                    'link': url_for('aptitude.index'),
                    'icon': 'fa-book'
                })
            else:
                recommendations.append({
                    'title': f"Review {topic} Coding/Theory",
                    'description': f"Brush up on {topic} questions or chat with Prep AI to clear doubts.",
                    'link': url_for('technical.index'),
                    'icon': 'fa-code'
                })
    else:
        # Standard onboarding recommendation
        recommendations.append({
            'title': "Perform Resume ATS Evaluation",
            'description': "Upload your profile to receive comprehensive reviews on grammar, styling, and skills.",
            'link': url_for('resume.index'),
            'icon': 'fa-file-invoice'
        })
        recommendations.append({
            'title': "Attempt a Mock Interview",
            'description': "Simulate a placement interview with live scoring and custom tips.",
            'link': url_for('mock_interview.index'),
            'icon': 'fa-microphone'
        })

    # Limit to top 3 recommendations
    recommendations = recommendations[:3]

    # Consolidate dynamic unified activity feed
    activities = []
    
    # 1. Quizzes
    for q in QuizScore.query.filter_by(user_id=user_id).order_by(QuizScore.created_at.desc()).limit(5).all():
        activities.append({
            'icon': 'fa-book text-info',
            'title': f"Completed {q.category} Test",
            'desc': f"Scored {q.score} out of {q.total_questions} questions",
            'date': q.created_at
        })
        
    # 2. Chat history
    for c in ChatHistory.query.filter_by(user_id=user_id).order_by(ChatHistory.created_at.desc()).limit(5).all():
        short_msg = c.message[:40] + "..." if len(c.message) > 40 else c.message
        activities.append({
            'icon': 'fa-robot text-primary',
            'title': "Interacted with Chatbot",
            'desc': f"Inquired: \"{short_msg}\"",
            'date': c.created_at
        })

    # 3. Resume reports
    for r in ResumeReport.query.filter_by(user_id=user_id).order_by(ResumeReport.created_at.desc()).limit(5).all():
        activities.append({
            'icon': 'fa-file-invoice text-success',
            'title': "Analyzed Resume",
            'desc': f"Report '{r.filename}' generated with ATS Score {r.ats_score}%",
            'date': r.created_at
        })

    # 4. Mock interviews
    for m in MockInterview.query.filter_by(user_id=user_id).order_by(MockInterview.created_at.desc()).limit(5).all():
        activities.append({
            'icon': 'fa-microphone text-warning',
            'title': "Mock Interview Assessment",
            'desc': f"Response scored: Tech {m.technical_score}/10, Comm {m.communication_score}/10",
            'date': m.created_at
        })

    # Sort chronological descending and limit to top 5
    activities.sort(key=lambda x: x['date'], reverse=True)
    recent_activities = activities[:5]

    return render_template(
        'dashboard.html',
        user=user,
        total_quizzes=total_quizzes,
        avg_score=avg_score,
        strong_topics=strong_topics,
        weak_topics=weak_topics,
        recommendations=recommendations,
        recent_activities=recent_activities
    )
