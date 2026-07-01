from flask import Blueprint, render_template, jsonify, flash
from models import db
from models.hr_questions import HRQuestion
from utils.gemini_helper import GeminiHelper
from routes.auth import login_required

hr_bp = Blueprint('hr', __name__, url_prefix='/hr')

@hr_bp.route('/')
@login_required
def index():
    # Fetch all 10 HR questions
    questions = HRQuestion.query.all()
    return render_template('hr/questions.html', questions=questions)

@hr_bp.route('/generate/<int:question_id>', methods=['POST'])
@login_required
def generate_answer(question_id):
    question = HRQuestion.query.get_or_404(question_id)
    
    # Return cached answer if available
    if question.cached_sample_answer:
        return jsonify({
            'status': 'success',
            'answer': question.cached_sample_answer,
            'source': 'cache'
        })
        
    # Generate live using Gemini
    generated_answer = GeminiHelper.generate_hr_answer(question.question)
    
    if generated_answer:
        # Cache it back in the database
        question.cached_sample_answer = generated_answer
        try:
            db.session.commit()
            return jsonify({
                'status': 'success',
                'answer': generated_answer,
                'source': 'ai_live'
            })
        except Exception as e:
            db.session.rollback()
            print(f"Error caching HR answer: {e}")
            return jsonify({
                'status': 'success',
                'answer': generated_answer,
                'source': 'ai_uncached'
            })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Failed to generate answer. Please try again.'
        }), 500
