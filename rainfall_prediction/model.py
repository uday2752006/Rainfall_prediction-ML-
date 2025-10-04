import pickle
import numpy as np
import logging

logger = logging.getLogger(__name__)

class RainfallModel:
    def __init__(self):
        self.model = None
        self.feature_names = None

    def load_model(self, model_path):
        """Load the trained model"""
        try:
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)

            if isinstance(model_data, dict):
                self.model = model_data['model']
                self.feature_names = model_data['feature_names']
            else:
                self.model = model_data
                # Default feature order (must match your training order)
                self.feature_names = [
                    'pressure', 'maxtemp', 'temparature', 'mintemp',
                    'dewpoint', 'humidity', 'cloud', 'sunshine',
                    'winddirection', 'windspeed'
                ]

            logger.info(f"Model loaded successfully with {len(self.feature_names)} features")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def predict(self, features_dict):
        """Make prediction based on input features"""
        if self.model is None:
            raise Exception("Model not loaded. Please train and save the model first.")

        # Ensure all required features are present
        feature_array = []
        for feature in self.feature_names:
            if feature in features_dict:
                feature_array.append(float(features_dict[feature]))
            else:
                raise ValueError(f"Missing feature: {feature}")

        # Convert to 2D array for prediction (single sample)
        X = np.array([feature_array])

        # Predict
        prediction = self.model.predict(X)
        if isinstance(prediction, np.ndarray):
            prediction = prediction.item()  # Convert 1-element array to scalar

        # Probability
        probability = None
        if hasattr(self.model, 'predict_proba'):
            prob_array = self.model.predict_proba(X)
            probability = prob_array[0]  # first row as 1D array

        # Feature importance if available
        feature_importance = None
        if hasattr(self.model, 'feature_importances_'):
            feature_importance = dict(zip(self.feature_names, self.model.feature_importances_))

        return prediction, probability, feature_importance

    def get_feature_ranges(self):
        """Return typical ranges for features (for validation)"""
        ranges = {
            'pressure': (980, 1040),
            'maxtemp': (0, 40),
            'temparature': (-10, 35),
            'mintemp': (-10, 30),
            'dewpoint': (-10, 30),
            'humidity': (0, 100),
            'cloud': (0, 100),
            'sunshine': (0, 12),
            'winddirection': (0, 360),
            'windspeed': (0, 100)
        }
        return ranges
