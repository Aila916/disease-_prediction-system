import numpy as np
import joblib
import json
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

class DiseasePredictor:
    def __init__(self):
        self.model = None
        self.label_encoder = LabelEncoder()
        self.symptom_mapping = {}
        self.disease_classes = ['Common Cold', 'Influenza', 'COVID-19', 'Diabetes', 'Malaria', 
                                'Typhoid', 'Pneumonia', 'Hypertension', 'Gastroenteritis', 'Allergy']
        
        # Load or create symptom mapping
        self._load_symptom_mapping()
        
        # Load or create model
        self._load_or_create_model()
    
    def _load_symptom_mapping(self):
        """Load symptom mapping from file or create default"""
        mapping_path = 'data/symptoms_mapping.json'
        
        if os.path.exists(mapping_path):
            try:
                with open(mapping_path, 'r') as f:
                    content = f.read().strip()
                    if content:
                        self.symptom_mapping = json.loads(content)
                        print(f"✅ Loaded {len(self.symptom_mapping)} symptoms from mapping")
                    else:
                        print("⚠️ symptoms_mapping.json is empty, creating default")
                        self._create_default_mapping()
            except json.JSONDecodeError:
                print("⚠️ Invalid JSON, creating default mapping")
                self._create_default_mapping()
        else:
            print("⚠️ symptoms_mapping.json not found, creating default")
            self._create_default_mapping()
    
    def _create_default_mapping(self):
        """Create default symptom mapping"""
        symptoms = ['fever', 'headache', 'fatigue', 'cough', 'sore throat', 
                    'runny nose', 'body aches', 'chills', 'sweating', 'shortness of breath',
                    'loss of taste', 'loss of smell', 'frequent urination', 'excessive thirst',
                    'abdominal pain', 'nausea', 'dizziness', 'blurred vision', 'skin rash',
                    'weight loss', 'chest pain', 'joint pain', 'back pain', 'diarrhea']
        self.symptom_mapping = {symptom: i for i, symptom in enumerate(symptoms)}
        
        # Save it
        os.makedirs('data', exist_ok=True)
        with open('data/symptoms_mapping.json', 'w') as f:
            json.dump(self.symptom_mapping, f, indent=2)
        print(f"✅ Created default mapping with {len(self.symptom_mapping)} symptoms")
    
    def _load_or_create_model(self):
        """Load existing model or create a simple one"""
        models_dir = 'models'
        os.makedirs(models_dir, exist_ok=True)
        
        # Try to load existing model
        model_files = []
        if os.path.exists(models_dir):
            model_files = [f for f in os.listdir(models_dir) 
                          if f.startswith('disease_model_') and f.endswith('.pkl')]
        
        if model_files:
            # Load the latest model
            latest = sorted(model_files)[-1]
            try:
                self.model = joblib.load(os.path.join(models_dir, latest))
                print(f"✅ Loaded model: {latest}")
                return
            except Exception as e:
                print(f"⚠️ Could not load model: {e}")
        
        # Create a simple model
        print("🔄 Creating new model...")
        self._create_simple_model()
    
    def _create_simple_model(self):
        """Create a simple Random Forest model with dummy training"""
        # Create dummy training data
        num_features = len(self.symptom_mapping)
        num_samples = 500
        num_classes = len(self.disease_classes)
        
        # Generate synthetic training data
        X_train = np.random.rand(num_samples, num_features)
        
        # Assign labels based on symptom patterns
        y_train = []
        for i in range(num_samples):
            # Randomly assign a disease
            disease_idx = np.random.randint(0, num_classes)
            y_train.append(disease_idx)
            
            # Add pattern: certain symptoms increase probability of certain diseases
            if disease_idx == 0:  # Common Cold
                X_train[i, 3:6] += 0.7  # cough, sore throat, runny nose
            elif disease_idx == 1:  # Influenza
                X_train[i, 0:4] += 0.7  # fever, headache, fatigue, cough
                X_train[i, 6:9] += 0.5  # body aches, chills, sweating
            elif disease_idx == 2:  # COVID-19
                X_train[i, 0] += 0.8  # fever
                X_train[i, 3] += 0.6  # cough
                X_train[i, 9] += 0.7  # shortness of breath
                X_train[i, 10] += 0.7  # loss of taste
                X_train[i, 11] += 0.7  # loss of smell
            elif disease_idx == 3:  # Diabetes
                X_train[i, 12] += 0.9  # frequent urination
                X_train[i, 13] += 0.9  # excessive thirst
                X_train[i, 2] += 0.7  # fatigue
                X_train[i, 19] += 0.5  # weight loss
            elif disease_idx == 4:  # Malaria
                X_train[i, 0] += 0.9  # fever
                X_train[i, 7] += 0.8  # chills
                X_train[i, 8] += 0.8  # sweating
                X_train[i, 1] += 0.7  # headache
            elif disease_idx == 5:  # Typhoid
                X_train[i, 0] += 0.9  # fever
                X_train[i, 1] += 0.8  # headache
                X_train[i, 14] += 0.8  # abdominal pain
                X_train[i, 15] += 0.7  # nausea
            elif disease_idx == 6:  # Pneumonia
                X_train[i, 0] += 0.9  # fever
                X_train[i, 3] += 0.9  # cough
                X_train[i, 9] += 0.9  # shortness of breath
                X_train[i, 6] += 0.6  # body aches
            elif disease_idx == 7:  # Hypertension
                X_train[i, 1] += 0.7  # headache
                X_train[i, 16] += 0.6  # dizziness
                X_train[i, 17] += 0.5  # blurred vision
                X_train[i, 20] += 0.7  # chest pain
            elif disease_idx == 8:  # Gastroenteritis
                X_train[i, 14] += 0.9  # abdominal pain
                X_train[i, 15] += 0.8  # nausea
                X_train[i, 23] += 0.9  # diarrhea
                X_train[i, 0] += 0.5  # fever
            elif disease_idx == 9:  # Allergy
                X_train[i, 4] += 0.7  # sore throat
                X_train[i, 5] += 0.8  # runny nose
                X_train[i, 18] += 0.9  # skin rash
                X_train[i, 9] += 0.4  # shortness of breath
            
            # Clip values to [0, 1]
            X_train[i] = np.clip(X_train[i], 0, 1)
        
        # Create and train model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        self.model.classes_ = np.array(range(num_classes))
        
        # Save the model
        model_path = 'models/disease_model_v1.pkl'
        joblib.dump(self.model, model_path)
        print(f"✅ Created and saved new model to {model_path}")
    
    def predict(self, symptoms):
        """
        Predict disease based on symptoms
        
        Args:
            symptoms: List of symptom names (e.g., ['fever', 'headache'])
        
        Returns:
            dict: Prediction results with predicted_disease, confidence, and top_predictions
        """
        if not symptoms:
            return {
                'predicted_disease': 'Unknown',
                'confidence': 0,
                'top_predictions': [{'disease': 'No symptoms provided', 'confidence': 0}]
            }
        
        # Convert symptoms to feature vector
        feature_vector = self._prepare_features(symptoms)
        
        # Make prediction
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba([feature_vector])[0]
            prediction_idx = self.model.predict([feature_vector])[0]
            
            # Get disease names
            classes = self.disease_classes
            
            # Get top 3 predictions
            top_indices = np.argsort(probabilities)[::-1][:3]
            top_predictions = []
            for idx in top_indices:
                if idx < len(classes):
                    disease_name = classes[idx]
                else:
                    disease_name = f'Disease_{idx}'
                top_predictions.append({
                    'disease': disease_name,
                    'confidence': float(probabilities[idx])
                })
            
            # Get the predicted disease name
            if prediction_idx < len(classes):
                predicted_disease = classes[prediction_idx]
            else:
                predicted_disease = f'Disease_{prediction_idx}'
            
            confidence = float(probabilities[prediction_idx]) if prediction_idx < len(probabilities) else 0
            
            return {
                'predicted_disease': predicted_disease,
                'confidence': confidence,
                'top_predictions': top_predictions
            }
        else:
            # Fallback for models without predict_proba
            prediction = self.model.predict([feature_vector])[0]
            if prediction < len(self.disease_classes):
                predicted_disease = self.disease_classes[prediction]
            else:
                predicted_disease = f'Disease_{prediction}'
            
            return {
                'predicted_disease': predicted_disease,
                'confidence': 0.5,
                'top_predictions': [{'disease': predicted_disease, 'confidence': 0.5}]
            }
    
    def _prepare_features(self, symptoms):
        """
        Convert symptom list to feature vector
        
        Args:
            symptoms: List of symptom names
        
        Returns:
            numpy array: Feature vector
        """
        num_features = len(self.symptom_mapping)
        feature_vector = np.zeros(num_features)
        
        if isinstance(symptoms, list):
            for symptom in symptoms:
                symptom_lower = symptom.lower().strip()
                
                # Exact match
                if symptom_lower in self.symptom_mapping:
                    idx = self.symptom_mapping[symptom_lower]
                    if idx < num_features:
                        feature_vector[idx] = 1.0
                else:
                    # Try partial match
                    for key in self.symptom_mapping:
                        if symptom_lower in key or key in symptom_lower:
                            idx = self.symptom_mapping[key]
                            if idx < num_features:
                                feature_vector[idx] = 0.7
                            break
        
        return feature_vector
    
    def get_available_symptoms(self):
        """
        Get list of all available symptoms
        
        Returns:
            list: All symptom names
        """
        return list(self.symptom_mapping.keys())
    
    def get_disease_classes(self):
        """
        Get list of all disease classes
        
        Returns:
            list: All disease names
        """
        return self.disease_classes