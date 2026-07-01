import random
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db
from models.aptitude_questions import AptitudeQuestion
from models.quiz_scores import QuizScore
from models.user_progress import UserProgress
from routes.auth import login_required

aptitude_bp = Blueprint('aptitude', __name__, url_prefix='/aptitude')

@aptitude_bp.route('/')
@login_required
def index():
    # Render categories page
    return render_template('aptitude/categories.html')

@aptitude_bp.route('/start/<category>')
@login_required
def start(category):
    if category not in ['Quantitative', 'Logical', 'Verbal']:
        flash("Invalid aptitude category.", "error")
        return redirect(url_for('aptitude.index'))

    # Retrieve all questions in the category and sample 10 of them
    all_questions = AptitudeQuestion.query.filter_by(category=category).all()
    if not all_questions:
        flash("No questions found in this category. Database seed may be missing.", "error")
        return redirect(url_for('aptitude.index'))

    sampled_questions = random.sample(all_questions, min(10, len(all_questions)))

    # Set up session state
    session['aptitude_quiz'] = {
        'category': category,
        'question_ids': [q.id for q in sampled_questions],
        'answers': {},  # format: {"0": "A", "1": "C"}
        'start_time': datetime.utcnow().isoformat(),
        'time_limit': 600  # 10 minutes (600 seconds)
    }
    
    return redirect(url_for('aptitude.quiz', idx=0))

@aptitude_bp.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    quiz_state = session.get('aptitude_quiz')
    if not quiz_state:
        flash("No active test session found.", "error")
        return redirect(url_for('aptitude.index'))

    current_idx = int(request.args.get('idx', 0))
    q_ids = quiz_state['question_ids']

    # Validate index boundaries
    if current_idx < 0:
        current_idx = 0
    elif current_idx >= len(q_ids):
        current_idx = len(q_ids) - 1

    # Check timing expiration on the server side
    start_time = datetime.fromisoformat(quiz_state['start_time'])
    elapsed = (datetime.utcnow() - start_time).total_seconds()
    remaining_time = max(0, quiz_state['time_limit'] - int(elapsed))

    if remaining_time <= 0:
        flash("Time's up! Your quiz has been auto-submitted.", "warning")
        return redirect(url_for('aptitude.submit_quiz'))

    if request.method == 'POST':
        # Retrieve answer selection
        selected_option = request.form.get('option')
        prev_idx = int(request.form.get('current_idx', 0))
        
        # Save the selection to session state
        if selected_option:
            quiz_state['answers'][str(prev_idx)] = selected_option
            session.modified = True

        action = request.form.get('action')
        
        if action == 'prev':
            return redirect(url_for('aptitude.quiz', idx=prev_idx - 1))
        elif action == 'next':
            return redirect(url_for('aptitude.quiz', idx=prev_idx + 1))
        elif action == 'submit':
            return redirect(url_for('aptitude.submit_quiz'))

    # Load current question
    q_id = q_ids[current_idx]
    question = AptitudeQuestion.query.get(q_id)
    saved_answer = quiz_state['answers'].get(str(current_idx))

    return render_template(
        'aptitude/quiz.html',
        question=question,
        current_idx=current_idx,
        total_questions=len(q_ids),
        remaining_time=remaining_time,
        saved_answer=saved_answer
    )

@aptitude_bp.route('/submit')
@login_required
def submit_quiz():
    quiz_state = session.pop('aptitude_quiz', None)
    if not quiz_state:
        return redirect(url_for('aptitude.index'))

    user_id = session['user_id']
    category = quiz_state['category']
    q_ids = quiz_state['question_ids']
    answers = quiz_state['answers']

    correct_count = 0
    detailed_results = []

    # Verify answers and build response breakdowns
    for idx, q_id in enumerate(q_ids):
        question = AptitudeQuestion.query.get(q_id)
        user_choice = answers.get(str(idx), '')
        is_correct = (user_choice == question.correct_option)
        
        if is_correct:
            correct_count += 1
            
        detailed_results.append({
            'question': question.question,
            'option_a': question.option_a,
            'option_b': question.option_b,
            'option_c': question.option_c,
            'option_d': question.option_d,
            'user_choice': user_choice,
            'correct_option': question.correct_option,
            'is_correct': is_correct,
            'explanation': question.explanation
        })

    # Save score record
    score_record = QuizScore(
        user_id=user_id,
        category=category,
        score=correct_count,
        total_questions=len(q_ids)
    )
    db.session.add(score_record)

    # Update or insert user progress summary metrics
    progress = UserProgress.query.filter_by(user_id=user_id, category=category).first()
    if not progress:
        progress = UserProgress(
            user_id=user_id,
            category=category,
            completed_count=0,
            average_score=0.0
        )
        db.session.add(progress)

    # Commit first so the aggregate includes this attempt
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error saving quiz score: {e}")
        flash("Could not write test results to database.", "error")
        return redirect(url_for('aptitude.index'))

    # Re-calculate aggregate stats
    all_scores = QuizScore.query.filter_by(user_id=user_id, category=category).all()
    if all_scores:
        total_percent = sum((s.score / s.total_questions) * 100 for s in all_scores)
        progress.average_score = total_percent / len(all_scores)
    progress.completed_count = len(all_scores)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error updating progress stats: {e}")

    # Render results template immediately with contextual payload
    return render_template(
        'aptitude/result.html',
        category=category,
        score=correct_count,
        total=len(q_ids),
        results=detailed_results
    )
