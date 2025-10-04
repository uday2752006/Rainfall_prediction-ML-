# 🌧️ Rainfall Prediction AI

A machine learning web application that predicts rainfall probability based on weather parameters using Logistic Regression.

## 📋 Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Model Details](#model-details)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)

## ✨ Features

- **🔐 User Authentication** - Login/Signup system (session-based)
- **🤖 ML Predictions** - Real-time rainfall probability predictions
- **📊 Visual Results** - Interactive probability charts and feature analysis
- **🌐 REST API** - JSON endpoints for programmatic access
- **📱 Responsive Design** - Works on desktop and mobile devices
- **🔍 Model Insights** - Feature importance and confidence scores

## 🗂️ Project Structure

```
rainfall-prediction/
├── __pycache__/
├── models/
│   └── rainfall_model.pkl          # Trained ML model
├── static/
│   ├── css/
│   │   └── style.css               # Styling
│   └── js/
│       └── script.js               # Frontend logic
├── templates/
│   ├── index.html                  # Main prediction interface
│   ├── results.html                # Prediction results
│   ├── login.html                  # Login page
│   └── signup.html                 # Registration page
├── app.py                          # Flask application
├── model.py                        # ML model handler
├── train_model.py                  # Model training script
└── requirements.txt                # Python dependencies
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step-by-Step Setup

1. **Clone or download the project**
   ```bash
   # If using git
   git clone <repository-url>
   cd rainfall-prediction
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify model file**
   - Ensure `models/rainfall_model.pkl` exists
   - If missing, run: `python train_model.py`

## 🎯 Usage

### Starting the Application

1. **Run the Flask server**
   ```bash
   python app.py
   ```

2. **Access the application**
   - Open browser and go to: `http://localhost:5000`
   - You'll be redirected to login page

3. **First-time setup**
   - Click "Sign up here" to create account
   - Enter username, email, and password
   - You'll be automatically logged in

### Making Predictions

1. **Navigate to prediction interface** after login
2. **Fill in weather parameters**:
   - Pressure (980-1040 hPa)
   - Temperature values (°C)
   - Humidity (0-100%)
   - Cloud cover (0-100%)
   - Sunshine hours (0-12)
   - Wind direction (0-360°)
   - Wind speed (0-100 km/h)

3. **Click "Predict Rainfall"** to get results
4. **View prediction** with confidence percentage and probability distribution

## 🤖 Model Details

### Machine Learning Model
- **Algorithm**: Logistic Regression
- **Type**: Binary Classification (Rain/No Rain)
- **Features**: 10 weather parameters
- **Output**: Probability of rainfall (0-1)

### Feature Set
| Feature | Description | Typical Range |
|---------|-------------|---------------|
| pressure | Atmospheric pressure | 980-1040 hPa |
| maxtemp | Maximum temperature | 0-40°C |
| temparature | Current temperature | -10-35°C |
| mintemp | Minimum temperature | -10-30°C |
| dewpoint | Dew point temperature | -10-30°C |
| humidity | Relative humidity | 0-100% |
| cloud | Cloud cover percentage | 0-100% |
| sunshine | Sunshine hours | 0-12 hours |
| winddirection | Wind direction | 0-360° |
| windspeed | Wind speed | 0-100 km/h |

## 🌐 API Endpoints

### Get Available Features
```http
GET /features
```
**Response:**
```json
{
  "features": ["pressure", "maxtemp", ...],
  "status": "success"
}
```

### Make Prediction (API)
```http
POST /api/predict
```
**Request Body:**
```json
{
  "pressure": 1013.0,
  "maxtemp": 26.0,
  "temparature": 23.7,
  "mintemp": 21.9,
  "dewpoint": 20.0,
  "humidity": 80.0,
  "cloud": 71.0,
  "sunshine": 4.4,
  "winddirection": 102,
  "windspeed": 21.5
}
```

**Response:**
```json
{
  "prediction": 0,
  "probability": [0.85, 0.15],
  "rain_chance": 0.15,
  "status": "success"
}
```

## 🧪 Testing

### Sample Values for Testing

**Values that predict RAIN:**
```python
pressure = 1005.0
maxtemp = 22.0
temparature = 19.5
mintemp = 18.0
dewpoint = 18.5
humidity = 95.0
cloud = 90.0
sunshine = 1.2
winddirection = 180
windspeed = 15.0
```

**Values that predict NO RAIN:**
```python
pressure = 1018.0
maxtemp = 28.0
temparature = 25.0
mintemp = 22.0
dewpoint = 16.0
humidity = 60.0
cloud = 20.0
sunshine = 8.5
winddirection = 90
windspeed = 10.0
```

### Manual Testing
1. Start the application
2. Login with credentials
3. Use the sample values above
4. Check prediction results and probabilities

## 🔧 Troubleshooting

### Common Issues

1. **"Model not loaded" error**
   - Ensure `rainfall_model.pkl` exists in `models/` folder
   - Run `python train_model.py` to generate model

2. **Import errors**
   - Verify all dependencies in `requirements.txt` are installed
   - Check Python version (requires 3.8+)

3. **Prediction always shows "No Rain"**
   - Check input values - use rain-inducing values provided above
   - Verify model training data quality

4. **Authentication issues**
   - Clear browser cookies/session storage
   - Restart the Flask application

### Debug Mode
Enable debug logging by checking the console output when running:
```bash
python app.py
```

## 📊 Model Performance

The logistic regression model provides:
- Binary classification (Rain/No Rain)
- Probability scores for both classes
- Feature importance analysis
- Confidence intervals

## 🔒 Security Notes

- This uses session-based authentication (in-memory)
- For production use, implement proper database authentication
- The secret key should be changed in production
- Consider adding rate limiting for API endpoints

## 📝 License

This project is for educational and demonstration purposes.

## 🤝 Contributing

Feel free to submit issues and enhancement requests


## VIDEO 
https://github.com/user-attachments/assets/632a7bbe-f12a-44b7-90be-4b05a065a1cd

