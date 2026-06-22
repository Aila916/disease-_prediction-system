from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app import db
from app.models.prediction import Prediction
from app.ml.predictor import DiseasePredictor
import json
import traceback

prediction_bp = Blueprint('prediction', __name__)
predictor = DiseasePredictor()

@prediction_bp.route('/predict', methods=['POST'])
@login_required
def predict():
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', [])
        
        if not symptoms:
            return jsonify({'error': 'No symptoms provided'}), 400
        
        # Make prediction
        result = predictor.predict(symptoms)
        
        # Store in database
        prediction = Prediction(
            user_id=current_user.id,
            symptoms_input=json.dumps(symptoms),
            predicted_disease=result['predicted_disease'],
            confidence_score=result['confidence'],
            top_predictions=json.dumps(result['top_predictions'])
        )
        db.session.add(prediction)
        db.session.commit()
        
        result['prediction_id'] = prediction.id
        
        return jsonify(result), 200
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@prediction_bp.route('/predict', methods=['GET'])
def predict_page():
    return render_template('predict.html')

@prediction_bp.route('/symptoms/search', methods=['GET'])
def search_symptoms():
    query = request.args.get('q', '').lower()
    
    # Get symptoms from predictor
    all_symptoms = predictor.get_available_symptoms() if hasattr(predictor, 'get_available_symptoms') else []
    
    if not all_symptoms:
        # Fallback list
        all_symptoms = ['fever', 'headache', 'fatigue', 'cough', 'sore throat', 
                       'runny nose', 'body aches', 'chills', 'sweating', 'shortness of breath',
                       'loss of taste', 'loss of smell', 'frequent urination', 'excessive thirst',
                       'abdominal pain', 'nausea', 'dizziness', 'blurred vision', 'skin rash',
                       'weight loss', 'chest pain', 'joint pain', 'back pain', 'diarrhea']
    
    if query:
        all_symptoms = [s for s in all_symptoms if query in s.lower()]
    
    return jsonify(all_symptoms[:10])

@prediction_bp.route('/history', methods=['GET'])
@login_required
def prediction_history():
    predictions = Prediction.query.filter_by(user_id=current_user.id)\
        .order_by(Prediction.created_at.desc()).all()
    
    return jsonify({
        'predictions': [
            {
                'id': p.id,
                'symptoms': json.loads(p.symptoms_input),
                'predicted_disease': p.predicted_disease,
                'confidence': p.confidence_score,
                'created_at': p.created_at.isoformat()
            }
            for p in predictions
        ]
    })