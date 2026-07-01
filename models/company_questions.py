from datetime import datetime
from models import db

class CompanyQuestion(db.Model):
    __tablename__ = 'company_questions'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False, index=True)
    selection_process = db.Column(db.Text, nullable=False)
    interview_rounds = db.Column(db.Text, nullable=False)
    coding_question = db.Column(db.Text, nullable=False)
    hr_question = db.Column(db.Text, nullable=False)
    previous_interview_question = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'company_name': self.company_name,
            'selection_process': self.selection_process,
            'interview_rounds': self.interview_rounds,
            'coding_question': self.coding_question,
            'hr_question': self.hr_question,
            'previous_interview_question': self.previous_interview_question
        }
