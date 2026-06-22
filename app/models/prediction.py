from app import db
from datetime import datetime

class Prediction(db.Model):
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    symptoms_input = db.Column(db.Text, nullable=False)
    predicted_disease = db.Column(db.String(100))
    confidence_score = db.Column(db.Float)
    top_predictions = db.Column(db.Text)
    user_feedback = db.Column(db.Boolean, nullable=True)
    feedback_disease = db.Column(db.String(100))
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Prediction {self.id} - {self.predicted_disease}>'