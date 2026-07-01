from datetime import datetime
from models import db

class CodingQuestion(db.Model):
    __tablename__ = 'coding_questions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    difficulty = db.Column(db.Enum('Easy', 'Medium', 'Hard', name='coding_difficulties'), nullable=False)
    topic = db.Column(db.String(100), nullable=False, index=True) # Arrays, Strings, Linked List, Stack, Queue, Trees, Graph, Dynamic Programming
    description = db.Column(db.Text, nullable=False)
    constraints = db.Column(db.Text, nullable=False)
    sample_input = db.Column(db.Text, nullable=False)
    sample_output = db.Column(db.Text, nullable=False)
    hints = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'difficulty': self.difficulty,
            'topic': self.topic,
            'description': self.description,
            'constraints': self.constraints,
            'sample_input': self.sample_input,
            'sample_output': self.sample_output,
            'hints': self.hints
        }
