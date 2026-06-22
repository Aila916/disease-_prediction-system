from app import db
from datetime import datetime

class Symptom(db.Model):
    __tablename__ = 'symptoms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    is_common = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Symptom {self.name}>'