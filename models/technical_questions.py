from datetime import datetime
from models import db

class TechnicalQuestion(db.Model):
    __tablename__ = 'technical_questions'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50), nullable=False, index=True) # C, C++, Java, Python, SQL, DBMS, OS, CN, DSA, OOP
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    is_frequently_asked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'question': self.question,
            'answer': self.answer,
            'is_frequently_asked': self.is_frequently_asked
        }
