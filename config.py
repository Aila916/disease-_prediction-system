import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///disease.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MODEL_PATH = os.environ.get('MODEL_PATH') or 'models/disease_model_v1.pkl'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False