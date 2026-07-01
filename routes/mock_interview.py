import random
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from models import db
from models.mock_interviews import MockInterview
from utils.gemini_helper import GeminiHelper
from routes.auth import login_required

mock_bp = Blueprint('mock_interview', __name__, url_prefix='/mock-interview')

POOL_QUESTIONS = [
    "Introduce yourself and highlight your academic background.",
    "Explain your final year project or any technical project you are proud of. What was your role?",
    "Why should we hire you? What value do you bring to our organization?",
    "What are your greatest professional strengths and weaknesses?",
    "Describe a situation where you had to work in a team and resolve a conflict or guide a project.",
    "Where do you see yourself in five years? What are your short-term and long-term career goals?"
]

@mock_bp.route('/')
@login_required
def index():
    # If a session is already in progress, redirect to chat, else show intro
    if 'mock_interview' in session:
        return redirect(url_for('mock_interview.chat'))
    return render_template('mock_interview/intro.html')

@mock_bp.route('/start')
@login_required
def start():
    # Randomize order of interview questions
    questions = list(POOL_QUESTIONS)
    random.shuffle(questions)
    
    # Store initial state in session
    session['mock_interview'] = {
        'questions': questions,
        'current_index': 0,
        'evaluations': []
    }
    session.modified = True
    
    return redirect(url_for('mock_interview.chat'))

@mock_bp.route('/chat')
@login_required
def chat():
    state = session.get('mock_interview')
    if not state:
        return redirect(url_for('mock_interview.index'))
        
    current_index = state['current_index']
    questions = state['questions']
    
    # If completed all questions, redirect to summary
    if current_index >= len(questions):
        return redirect(url_for('mock_interview.summary'))
        
    question = questions[current_index]
    
    return render_template(
        'mock_interview/chat.html',
        question=question,
        current_num=current_index + 1,
        total_num=len(questions)
    )

@mock_bp.route('/evaluate', methods=['POST'])
@login_required
def evaluate():
    state = session.get('mock_interview')
    if not state:
        return jsonify({'status': 'error', 'message': 'No active interview session'}), 400
        
    user_id = session['user_id']
    data = request.get_json() or {}
    answer = data.get('answer', '').strip()
    
    if not answer:
        return jsonify({'status': 'error', 'message': 'Answer cannot be empty'}), 400
        
    current_index = state['current_index']
    questions = state['questions']
    question = questions[current_index]
    
    # Run evaluation using Gemini API
    feedback = GeminiHelper.evaluate_mock_answer(question, answer)
    
    # Save parameters to database table
    record = MockInterview(
        user_id=user_id,
        question=question,
        answer=answer,
        communication_score=feedback.get('communication_score', 5),
        technical_score=feedback.get('technical_score', 5),
        confidence_score=feedback.get('confidence_score', 5),
        suggestions=feedback.get('suggestions', '')
    )
    
    try:
        db.session.add(record)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error saving mock interview response: {e}")

    # Append evaluation to session cache
    state['evaluations'].append({
        'question': question,
        'answer': answer,
        'comm_score': feedback.get('communication_score', 5),
        'tech_score': feedback.get('technical_score', 5),
        'conf_score': feedback.get('confidence_score', 5),
        'suggestions': feedback.get('suggestions', '')
    })
    
    # Increment position
    state['current_index'] += 1
    session.modified = True
    
    is_last = (state['current_index'] >= len(questions))
    
    return jsonify({
        'status': 'success',
        'feedback': feedback,
        'is_last': is_last
    })

@mock_bp.route('/summary')
@login_required
def summary():
    state = session.pop('mock_interview', None)  # Extract and clear session
    if not state or not state['evaluations']:
        flash("No completed mock interview results found. Start a new session.", "error")
        return redirect(url_for('mock_interview.index'))
        
    evals = state['evaluations']
    
    # Calculate average scores
    avg_comm = round(sum(e['comm_score'] for e in evals) / len(evals), 1)
    avg_tech = round(sum(e['tech_score'] for e in evals) / len(evals), 1)
    avg_conf = round(sum(e['conf_score'] for e in evals) / len(evals), 1)
    overall_avg = round((avg_comm + avg_tech + avg_conf) / 3, 1)

    return render_template(
        'mock_interview/summary.html',
        evals=evals,
        avg_comm=avg_comm,
        avg_tech=avg_tech,
        avg_conf=avg_conf,
        overall_avg=overall_avg
    )
