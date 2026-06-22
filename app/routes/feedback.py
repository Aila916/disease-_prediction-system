from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.prediction import Prediction
import json

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['POST'])
@login_required
def submit_feedback():
    try:
        data = request.get_json()
        prediction_id = data.get('prediction_id')
        is_correct = data.get('is_correct', False)
        correct_disease = data.get('correct_disease', None)
        
        prediction = Prediction.query.get(prediction_id)
        if not prediction:
            return jsonify({'error': 'Prediction not found'}), 404
        
        if prediction.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        prediction.user_feedback = is_correct
        prediction.feedback_disease = correct_disease
        db.session.commit()
        
        return jsonify({'message': 'Feedback recorded successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@feedback_bp.route('/feedback/stats', methods=['GET'])
@login_required
def feedback_stats():
    total = Prediction.query.filter_by(user_id=current_user.id).count()
    feedback_given = Prediction.query.filter_by(
        user_id=current_user.id
    ).filter(Prediction.user_feedback.isnot(None)).count()
    
    correct = Prediction.query.filter_by(
        user_id=current_user.id,
        user_feedback=True
    ).count()
    
    return jsonify({
        'total_predictions': total,
        'feedback_given': feedback_given,
        'correct_predictions': correct,
        'accuracy': correct / feedback_given if feedback_given > 0 else 0
    })