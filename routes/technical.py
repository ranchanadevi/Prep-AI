from flask import Blueprint, render_template, request
from models import db
from models.technical_questions import TechnicalQuestion
from routes.auth import login_required

technical_bp = Blueprint('technical', __name__, url_prefix='/technical')

# Map URL parameters/subject strings to display titles
SUBJECT_MAP = {
    'C': 'C Programming',
    'C++': 'C++ OOP & Core',
    'Java': 'Java Programming & JVM',
    'Python': 'Python Scripting',
    'SQL': 'Structured Query Language (SQL)',
    'DBMS': 'Database Management Systems (DBMS)',
    'OS': 'Operating Systems (OS)',
    'CN': 'Computer Networks (CN)',
    'DSA': 'Data Structures & Algorithms (DSA)',
    'OOP': 'Object-Oriented Programming (OOP)'
}

@technical_bp.route('/')
@login_required
def index():
    # Render subject selection cards
    return render_template('technical/subjects.html', subjects=SUBJECT_MAP)

@technical_bp.route('/subject/<subject_name>')
@login_required
def subject_detail(subject_name):
    # Retrieve subject title
    display_title = SUBJECT_MAP.get(subject_name, subject_name)
    
    # Handle search query
    search_query = request.args.get('q', '').strip()
    
    if search_query:
        # Search by substring in question or answer
        questions = TechnicalQuestion.query.filter(
            TechnicalQuestion.subject == subject_name,
            (TechnicalQuestion.question.contains(search_query) | 
             TechnicalQuestion.answer.contains(search_query))
        ).all()
    else:
        questions = TechnicalQuestion.query.filter_by(subject=subject_name).all()

    return render_template(
        'technical/questions.html',
        subject_name=subject_name,
        display_title=display_title,
        questions=questions,
        search_query=search_query
    )
