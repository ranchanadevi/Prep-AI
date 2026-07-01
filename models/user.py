from datetime import datetime
from models import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    college_name = db.Column(db.String(200), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    year_of_study = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    chats = db.relationship('ChatHistory', backref='user', lazy=True, cascade="all, delete-orphan")
    quiz_scores = db.relationship('QuizScore', backref='user', lazy=True, cascade="all, delete-orphan")
    progress = db.relationship('UserProgress', backref='user', lazy=True, cascade="all, delete-orphan")
    resume_reports = db.relationship('ResumeReport', backref='user', lazy=True, cascade="all, delete-orphan")
    mock_interviews = db.relationship('MockInterview', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'college_name': self.college_name,
            'department': self.department,
            'year_of_study': self.year_of_study,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
