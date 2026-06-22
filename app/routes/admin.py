from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.models.prediction import Prediction
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/models')
@login_required
@admin_required
def models():
    return render_template('admin/models.html')

@admin_bp.route('/feedback/review')
@login_required
@admin_required
def review_feedback():
    return render_template('admin/feedback_review.html')