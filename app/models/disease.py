from app import db
from datetime import datetime

class Disease(db.Model):
    __tablename__ = 'diseases'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    severity_level = db.Column(db.String(20))
    common_symptoms = db.Column(db.Text)
    recommended_action = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Disease {self.name}>'