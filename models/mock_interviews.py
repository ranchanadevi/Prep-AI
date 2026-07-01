from datetime import datetime
from models import db

class MockInterview(db.Model):
    __tablename__ = 'mock_interviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    communication_score = db.Column(db.Integer, nullable=False) # 0 to 10
    technical_score = db.Column(db.Integer, nullable=False) # 0 to 10
    confidence_score = db.Column(db.Integer, nullable=False) # 0 to 10
    suggestions = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question': self.question,
            'answer': self.answer,
            'communication_score': self.communication_score,
            'technical_score': self.technical_score,
            'confidence_score': self.confidence_score,
            'suggestions': self.suggestions,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
