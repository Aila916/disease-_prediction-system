from app import create_app, db
from app.models.user import User
from app.models.disease import Disease
from app.models.symptom import Symptom
from app.models.prediction import Prediction

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Disease': Disease,
        'Symptom': Symptom,
        'Prediction': Prediction
    }

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")
        
        if not User.query.filter_by(email='admin@admin.com').first():
            from flask_bcrypt import Bcrypt
            bcrypt = Bcrypt()
            admin = User(
                username='admin',
                email='admin@admin.com',
                password_hash=bcrypt.generate_password_hash('admin123').decode('utf-8'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created: admin@admin.com / admin123")
    
    app.run(host='0.0.0.0', port=5000, debug=True)