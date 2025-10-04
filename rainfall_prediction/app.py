from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import os
import logging
from model import RainfallModel
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Initialize model
model_handler = RainfallModel()

# Simple in-memory user storage (reset on server restart)
users = {}

@app.route('/')
def home():
    """Home page - redirect to login if not authenticated"""
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple authentication - for demo purposes only
        if username and password:
            # Check if user exists in our simple storage
            if username in users and users[username] == password:
                session['user'] = username
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password', 'error')
        else:
            flash('Please fill all fields', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Simple validation
        if not all([username, email, password, confirm_password]):
            flash('Please fill all fields', 'error')
        elif password != confirm_password:
            flash('Passwords do not match', 'error')
        elif username in users:
            flash('Username already exists', 'error')
        else:
            # Store user (in memory)
            users[username] = password
            session['user'] = username
            flash('Account created successfully!', 'success')
            return redirect(url_for('home'))
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.pop('user', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests from form"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    try:
        # Collect features from form
        features = {k: float(request.form.get(k, 0)) for k in model_handler.feature_names}
        logger.info(f"Received features: {features}")

        # Make prediction
        prediction, probability, feature_importance = model_handler.predict(features)

        # Ensure scalar and list types for safety
        if isinstance(prediction, np.ndarray):
            prediction = prediction.item()
        if isinstance(probability, np.ndarray):
            probability = probability.tolist()

        # Prepare result dictionary
        result = {
            'prediction': 'Rain' if prediction == 1 else 'No Rain',
            'probability': probability,
            'confidence': f"{max(probability):.2%}" if probability else "N/A",
            'feature_importance': feature_importance
        }

        logger.info(f"Prediction result: {result}")

        return render_template('results.html',
                               result=result,
                               features=features,
                               feature_names=model_handler.feature_names)

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return render_template('index.html', error=f"Prediction failed: {str(e)}")

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for predictions"""
    if 'user' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Make prediction
        prediction, probability, _ = model_handler.predict(data)

        # Ensure scalar and list types
        if isinstance(prediction, np.ndarray):
            prediction = prediction.item()
        if isinstance(probability, np.ndarray):
            probability = probability.tolist()

        return jsonify({
            'prediction': int(prediction),
            'probability': probability,
            'rain_chance': float(probability[1]) if probability else None,
            'status': 'success'
        })

    except Exception as e:
        logger.error(f"API prediction error: {str(e)}")
        return jsonify({'error': str(e), 'status': 'error'}), 400

@app.route('/features')
def get_features():
    """Get available features"""
    if 'user' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    return jsonify({
        'features': model_handler.feature_names,
        'status': 'success'
    })

@app.errorhandler(404)
def not_found(error):
    return render_template('login.html', error="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('login.html', error="Internal server error"), 500

if __name__ == '__main__':
    # Ensure models directory exists
    os.makedirs('models', exist_ok=True)

    # Try to load the model
    try:
        model_handler.load_model('models/rainfall_model.pkl')
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.warning(f"Could not load model: {str(e)}")
        logger.info("Please train the model first by running train_model.py")

    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)