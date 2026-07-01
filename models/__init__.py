from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models to register them with SQLAlchemy
from models.user import User
from models.chat_history import ChatHistory
from models.aptitude_questions import AptitudeQuestion
from models.technical_questions import TechnicalQuestion
from models.company_questions import CompanyQuestion
from models.hr_questions import HRQuestion
from models.coding_questions import CodingQuestion
from models.quiz_scores import QuizScore
from models.user_progress import UserProgress
from models.resume_reports import ResumeReport
from models.mock_interviews import MockInterview
