import json
from datetime import datetime
from models import db

class ResumeReport(db.Model):
    __tablename__ = 'resume_reports'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    ats_score = db.Column(db.Integer, nullable=False)
    analysis_json = db.Column(db.Text, nullable=False) # JSON output containing missing skills, feedback etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def get_analysis_data(self):
        try:
            return json.loads(self.analysis_json)
        except Exception:
            return {}

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'filename': self.filename,
            'ats_score': self.ats_score,
            'analysis': self.get_analysis_data(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
