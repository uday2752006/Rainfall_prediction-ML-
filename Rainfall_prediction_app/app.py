from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pickle
import numpy as np
import pandas as pd
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Load the model
def load_model():
    try:
        with open('rainfall_prediction_model.pkl', 'rb') as file:
            loaded_data = pickle.load(file)
        
        print(f"Loaded object type: {type(loaded_data)}")
        
        # Extract model from dictionary
        model = None
        if isinstance(loaded_data, dict) and 'model' in loaded_data:
            model = loaded_data['model']
            print("✅ Model loaded from dictionary key 'model'")
        
        if model and hasattr(model, 'predict'):
            print(f"✅ Model type: {type(model)}")
            print(f"✅ Expected features: {model.n_features_in_}")
            return model
        else:
            print("❌ No valid model found")
            return None
            
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None

# Load the model
model = load_model()

# 12 Features that your model expects (based on common meteorological data)
FEATURE_NAMES = [
    'temperature',           # °C - Air temperature
    'humidity',              # % - Relative humidity
    'wind_speed',            # km/h - Wind speed
    'pressure',              # hPa - Atmospheric pressure
    'cloud_cover',           # % - Cloud coverage
    'precipitation',         # mm - Current precipitation
    'visibility',            # km - Visibility distance
    'dew_point',             # °C - Dew point temperature
    'wind_direction',        # degrees - Wind direction (0-360)
    'solar_radiation',       # W/m² - Solar radiation intensity
    'uv_index',              # index - UV radiation level
    'precipitation_3hr'      # mm - Precipitation in last 3 hours
]

print(f"✅ Using {len(FEATURE_NAMES)} features: {FEATURE_NAMES}")

# Helper function to get icons for features
def get_feature_icon(feature_name):
    icons = {
        'temperature': 'thermometer-half',
        'humidity': 'tint',
        'wind_speed': 'wind',
        'wind_direction': 'compass',
        'pressure': 'tachometer-alt',
        'cloud_cover': 'cloud',
        'precipitation': 'cloud-rain',
        'precipitation_3hr': 'cloud-showers-heavy',
        'visibility': 'eye',
        'dew_point': 'snowflake',
        'solar_radiation': 'sun',
        'uv_index': 'sun'
    }
    
    for key, icon in icons.items():
        if key in feature_name.lower():
            return icon
    return 'chart-line'

# Helper function to get default values and units
def get_default_value(feature_name):
    defaults = {
        'temperature': 25.0,
        'humidity': 65.0,
        'wind_speed': 12.0,
        'pressure': 1013.0,
        'cloud_cover': 45.0,
        'precipitation': 0.0,
        'visibility': 10.0,
        'dew_point': 18.0,
        'wind_direction': 180.0,
        'solar_radiation': 500.0,
        'uv_index': 5.0,
        'precipitation_3hr': 0.0
    }
    return defaults.get(feature_name, 0.0)

def get_feature_units(feature_name):
    units = {
        'temperature': '°C',
        'humidity': '%',
        'wind_speed': 'km/h',
        'pressure': 'hPa',
        'cloud_cover': '%',
        'precipitation': 'mm',
        'visibility': 'km',
        'dew_point': '°C',
        'wind_direction': 'degrees',
        'solar_radiation': 'W/m²',
        'uv_index': 'index',
        'precipitation_3hr': 'mm'
    }
    return units.get(feature_name, 'units')

# Make helpers available to templates
app.jinja_env.globals.update(
    get_feature_icon=get_feature_icon,
    get_default_value=get_default_value,
    get_feature_units=get_feature_units
)
def get_feature_description(feature_name):
    descriptions = {
        'temperature': 'Air temperature in Celsius',
        'humidity': 'Relative humidity percentage',
        'wind_speed': 'Wind speed in kilometers per hour',
        'pressure': 'Atmospheric pressure in hectopascals',
        'cloud_cover': 'Percentage of sky covered by clouds',
        'precipitation': 'Current precipitation in millimeters',
        'visibility': 'Visibility distance in kilometers',
        'dew_point': 'Dew point temperature in Celsius',
        'wind_direction': 'Wind direction in degrees (0-360)',
        'solar_radiation': 'Solar radiation intensity in watts per square meter',
        'uv_index': 'Ultraviolet radiation index',
        'precipitation_3hr': 'Precipitation in last 3 hours in millimeters'
    }
    return descriptions.get(feature_name, 'Weather parameter')

# Update the template globals
app.jinja_env.globals.update(
    get_feature_icon=get_feature_icon,
    get_default_value=get_default_value,
    get_feature_units=get_feature_units,
    get_feature_description=get_feature_description
)

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('signup.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('signup.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('signup.html')
        
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/index')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    model_status = "✅ Model loaded and ready" if model else "❌ Model not available (using demo mode)"
    feature_info = f"({len(FEATURE_NAMES)} features expected)"
    
    return render_template('index.html', 
                         username=session['username'], 
                         model_status=model_status,
                         feature_info=feature_info,
                         feature_names=FEATURE_NAMES)

@app.route('/predict', methods=['POST'])
def predict():
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first'}), 401
    
    try:
        # Get form data for all 12 features
        features = []
        submitted_features = {}
        
        for feature in FEATURE_NAMES:
            value = float(request.form[feature])
            features.append(value)
            submitted_features[feature] = value
        
        # Convert to numpy array and reshape for prediction
        features_array = np.array(features).reshape(1, -1)
        
        print(f"✅ Features submitted: {len(features)}")
        print(f"✅ Features array shape: {features_array.shape}")
        
        # Make prediction
        if model and hasattr(model, 'predict'):
            # Use actual model
            prediction = model.predict(features_array)[0]
            if hasattr(model, 'predict_proba'):
                probability = model.predict_proba(features_array)[0]
                confidence = probability[1] * 100 if prediction == 1 else probability[0] * 100
            else:
                confidence = 85.0 if prediction == 1 else 75.0
                
            demo_mode = False
            print(f"✅ Prediction: {prediction}, Confidence: {confidence:.2f}%")
        else:
            # Demo mode - simple rule based on humidity and cloud cover
            humidity = features[1]  # humidity is 2nd feature
            cloud_cover = features[4]  # cloud_cover is 5th feature
            precipitation_3hr = features[11]  # precipitation_3hr is 12th feature
            
            # More sophisticated demo logic
            rain_probability = (humidity * 0.3 + cloud_cover * 0.3 + precipitation_3hr * 2.0)
            prediction = 1 if rain_probability > 60 else 0
            confidence = min(rain_probability, 95.0)
            demo_mode = True
            flash('⚠️ Using demo mode - actual model not available', 'warning')
        
        # Determine rainfall status
        if prediction == 1:
            result = "Rainfall Expected 🌧️"
            result_class = "rain-expected"
        else:
            result = "No Rainfall Expected ☀️"
            result_class = "no-rain"
        
        return jsonify({
            'prediction': result,
            'confidence': round(confidence, 2),
            'features': submitted_features,
            'demo_mode': demo_mode,
            'feature_count': len(features),
            'result_class': result_class
        })
        
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/model_info')
def model_info():
    """Endpoint to get model information"""
    info = {
        'model_loaded': model is not None,
        'expected_features': model.n_features_in_ if model else 12,
        'feature_names': FEATURE_NAMES,
        'feature_count': len(FEATURE_NAMES),
        'model_type': str(type(model)) if model else 'None',
        'model_ready': model is not None and hasattr(model, 'predict')
    }
    return jsonify(info)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    print("=== Rainfall Prediction App ===")
    print(f"✅ Model loaded: {model is not None}")
    if model:
        print(f"✅ Model type: {type(model)}")
        print(f"✅ Expected features: {model.n_features_in_}")
        print(f"✅ Has predict method: {hasattr(model, 'predict')}")
    print(f"✅ Using {len(FEATURE_NAMES)} features")
    print("✅ Starting server on http://localhost:5000")
    app.run(debug=True, port=5000)