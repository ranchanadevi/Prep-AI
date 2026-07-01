from datetime import datetime
from models import db

class QuizScore(db.Model):
    __tablename__ = 'quiz_scores'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    category = db.Column(db.String(100), nullable=False) # e.g. Quantitative, Logical, Verbal, C, DSA etc.
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category': self.category,
            'score': self.score,
            'total_questions': self.total_questions,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
