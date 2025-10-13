# 🌧️ Rainfall Prediction Web Application

A beautiful, interactive web application that predicts rainfall probability using machine learning. Built with Flask, featuring user authentication, real-time predictions, and a stunning dark-mode interface.

![Rainfall Prediction App](https://img.shields.io/badge/ML-Prediction-blue) ![Flask](https://img.shields.io/badge/Framework-Flask-green) ![Python](https://img.shields.io/badge/Python-3.9%2B-yellow)

## ✨ Features

- 🔐 **User Authentication** - Secure login/signup system
- 🤖 **ML-Powered Predictions** - Random Forest classifier for rainfall prediction
- 🎨 **Beautiful UI** - Dark mode with animations and transitions
- 📱 **Responsive Design** - Works on desktop and mobile devices
- 📊 **Real-time Results** - Instant prediction with confidence scores
- 🔧 **Model Diagnostics** - Built-in tools to verify model compatibility
- 💾 **SQLite Database** - Secure user data storage

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Anaconda/Miniconda
- Modern web browser

### Installation

1. **Clone or download the project**
   ```bash
   # Create project directory
   mkdir rainfall-prediction-app
   cd rainfall-prediction-app
   ```

2. **Create and activate Conda environment**
   ```bash
   conda create -n rainfall-app python=3.9 -y
   conda activate rainfall-app
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up project structure**
   ```bash
   # Create folders
   mkdir -p static/{css,js,images} templates
   
   # Create required files (copy the provided code files)
   ```

5. **Add your ML model**
   - Place your `rainfall_prediction_model.pkl` file in the root directory

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   - Open your browser and go to: `http://localhost:5000`

## 📁 Project Structure

```
rainfall-prediction-app/
│
├── app.py                          # Main Flask application
├── check_model.py                  # Model diagnostics script
├── requirements.txt                # Python dependencies
├── rainfall_prediction_model.pkl   # Your trained ML model
├── users.db                       # SQLite database (auto-created)
│
├── static/
│   ├── css/
│   │   ├── style.css              # Main stylesheet
│   │   └── auth.css               # Authentication styles
│   ├── js/
│   │   ├── script.js              # Main JavaScript
│   │   └── auth.js                # Authentication JavaScript
│   └── images/                    # Background images
│
└── templates/
    ├── base.html                  # Base template
    ├── login.html                 # Login page
    ├── signup.html                # Registration page
    └── index.html                 # Main dashboard
```

## 🔧 Configuration

### Model Requirements
- **Algorithm**: Random Forest Classifier
- **Expected Features**: 12 meteorological parameters
- **Input Format**: NumPy array with specific feature order

### Required 12 Features:
1. **Temperature** (°C) - Air temperature
2. **Humidity** (%) - Relative humidity
3. **Wind Speed** (km/h) - Wind velocity
4. **Pressure** (hPa) - Atmospheric pressure
5. **Cloud Cover** (%) - Sky cloud coverage
6. **Precipitation** (mm) - Current rainfall
7. **Visibility** (km) - Visual range
8. **Dew Point** (°C) - Dew point temperature
9. **Wind Direction** (degrees) - Wind compass direction
10. **Solar Radiation** (W/m²) - Sunlight intensity
11. **UV Index** - Ultraviolet radiation level
12. **Precipitation 3hr** (mm) - Recent rainfall amount

## 🎯 Usage Guide

### 1. User Registration
- Navigate to the signup page
- Create a new account with username and email
- Login with your credentials

### 2. Making Predictions
- Fill in all 12 weather parameters in the form
- Click "Predict Rainfall"
- View real-time results with confidence percentage

### 3. Understanding Results
- **Rainfall Expected** 🌧️: High probability of rain
- **No Rainfall Expected** ☀️: Low probability of rain
- **Confidence Score**: Model's certainty in prediction

### Sample Input for No Rainfall:
```python
temperature = 28.0
humidity = 45.0
wind_speed = 10.0
pressure = 1018.0
cloud_cover = 15.0
precipitation = 0.0
visibility = 25.0
dew_point = 12.0
wind_direction = 270.0
solar_radiation = 850.0
uv_index = 8.0
precipitation_3hr = 0.0
```

## 🛠️ Troubleshooting

### Common Issues:

1. **Module Not Found Errors**
   ```bash
   # Reinstall dependencies
   pip install --upgrade -r requirements.txt
   ```

2. **Model Loading Issues**
   ```bash
   # Run diagnostics
   python check_model.py
   ```

3. **Port Already in Use**
   ```python
   # Change port in app.py
   app.run(debug=True, port=5001)
   ```

4. **NumPy Compatibility**
   ```bash
   # Fix NumPy version
   pip install "numpy<2" --upgrade
   ```

### Model Compatibility:
- Ensure your `.pkl` file contains a scikit-learn model
- Model should have `.predict()` method
- Expected: 12 input features as listed above

## 🔍 Model Diagnostics

Check your model compatibility:
```bash
python check_model_features.py
```

This script will:
- Verify model structure
- Check expected feature count
- Test prediction capability
- Provide compatibility report

## 📊 API Endpoints

- `GET /` - Home page (redirects to login)
- `GET /login` - User login page
- `GET /signup` - User registration page
- `GET /index` - Main prediction dashboard
- `POST /predict` - Rainfall prediction endpoint
- `GET /model_info` - Model information
- `GET /logout` - User logout

## 🎨 Customization

### Changing Theme Colors
Edit `static/css/style.css`:
```css
:root {
    --primary-color: #2563eb;      /* Main blue */
    --bg-dark: #0f172a;           /* Dark background */
    --success-color: #10b981;     /* Success green */
    /* Add your custom colors */
}
```

### Adding New Features
1. Update `FEATURE_NAMES` in `app.py`
2. Add form fields in `templates/index.html`
3. Update validation in JavaScript files

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- Machine Learning with [scikit-learn](https://scikit-learn.org/)
- Icons by [Font Awesome](https://fontawesome.com/)
- UI inspired by modern web design principles

## 📞 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Run the diagnostic scripts
3. Ensure all dependencies are installed
4. Verify your model file compatibility

---

**Happy Predicting!** 🌦️

*Remember: This tool provides probabilistic predictions and should be used alongside official weather forecasts for critical decisions.*
