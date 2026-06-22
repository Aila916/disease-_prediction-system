from app import db
from datetime import datetime

class Feedback(db.Model):
    __tablename__ = 'feedback_log'
    
    id = db.Column(db.Integer, primary_key=True)
    prediction_id = db.Column(db.Integer, db.ForeignKey('predictions.id'))
    previous_model_version = db.Column(db.String(20))
    retraining_trigger = db.Column(db.String(50))
    status = db.Column(db.String(20), default='PENDING')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Feedback {self.id}>'