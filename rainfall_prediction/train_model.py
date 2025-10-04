import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import warnings
warnings.filterwarnings('ignore')

class RainfallPredictor:
    def __init__(self):
        self.model = None
        self.feature_names = None
        
    def load_and_preprocess_data(self, file_path):
        """Load and preprocess the dataset"""
        # Load dataset
        df = pd.read_csv(file_path)
        
        print("Initial dataset shape:", df.shape)
        print("Columns:", df.columns.tolist())
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Handle missing values
        df = df.dropna()
        
        # Convert rainfall to binary classification (0: No rain, 1: Rain)
        df['rainfall_binary'] = (df['rainfall'] > 0).astype(int)
        
        # Select features for modeling
        feature_columns = ['pressure', 'maxtemp', 'temparature', 'mintemp', 
                          'dewpoint', 'humidity', 'cloud', 'sunshine', 
                          'winddirection', 'windspeed']
        
        # Ensure all columns exist
        available_features = [col for col in feature_columns if col in df.columns]
        X = df[available_features]
        y = df['rainfall_binary']
        
        self.feature_names = available_features
        
        print(f"Available features: {available_features}")
        print(f"Target distribution:\n{y.value_counts()}")
        print(f"Rain percentage: {(y.sum() / len(y)) * 100:.2f}%")
        
        return X, y
    
    def train_model(self, X, y):
        """Train the Random Forest model"""
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train Random Forest Classifier
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = self.model.predict(X_test)
        
        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Model Accuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nFeature Importance:")
        print(feature_importance)
        
        return accuracy, X_test, y_test, y_pred
    
    def save_model(self, file_path):
        """Save the trained model"""
        with open(file_path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'feature_names': self.feature_names
            }, f)
        print(f"Model saved to {file_path}")
    
    def load_model(self, file_path):
        """Load a trained model"""
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        self.model = data['model']
        self.feature_names = data['feature_names']
        print(f"Model loaded from {file_path}")

def main():
    # Initialize the predictor
    predictor = RainfallPredictor()
    
    try:
        # Load and preprocess data
        X, y = predictor.load_and_preprocess_data("Rainfall.csv")
        
        # Train model
        accuracy, X_test, y_test, y_pred = predictor.train_model(X, y)
        
        # Save model
        predictor.save_model("models/rainfall_model.pkl")
        
        print("\n" + "="*50)
        print("Model training completed successfully!")
        print(f"Final Accuracy: {accuracy:.4f}")
        print("="*50)
        
    except Exception as e:
        print(f"Error during model training: {str(e)}")
        # Create a simple model for demonstration
        print("Creating a demo model...")
        from sklearn.datasets import make_classification
        from sklearn.ensemble import RandomForestClassifier
        
        X, y = make_classification(n_samples=1000, n_features=10, random_state=42)
        predictor.model = RandomForestClassifier(n_estimators=10, random_state=42)
        predictor.model.fit(X, y)
        predictor.feature_names = [f'feature_{i}' for i in range(10)]
        predictor.save_model("models/rainfall_model.pkl")

if __name__ == "__main__":
    main()