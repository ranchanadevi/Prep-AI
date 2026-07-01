from datetime import datetime
from models import db

class UserProgress(db.Model):
    __tablename__ = 'user_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    completed_count = db.Column(db.Integer, default=0)
    average_score = db.Column(db.Float, default=0.0) # in percentage (0-100)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Ensure uniqueness of user_id + category
    __table_args__ = (
        db.UniqueConstraint('user_id', 'category', name='uq_user_category'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category': self.category,
            'completed_count': self.completed_count,
            'average_score': self.average_score,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
