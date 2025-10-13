import pickle
import numpy as np
import sklearn
from sklearn.ensemble import RandomForestClassifier

print("=== Model Feature Analysis ===")
print(f"scikit-learn version: {sklearn.__version__}")

try:
    with open('rainfall_prediction_model.pkl', 'rb') as file:
        loaded_data = pickle.load(file)
    
    print(f"✅ File loaded successfully!")
    print(f"Type: {type(loaded_data)}")
    
    # Extract the actual model
    model = None
    if hasattr(loaded_data, 'predict'):
        model = loaded_data
    elif isinstance(loaded_data, dict):
        # Look for the model in common keys
        for key in ['model', 'estimator', 'classifier', 'regressor', 'clf', 'rf']:
            if key in loaded_data and hasattr(loaded_data[key], 'predict'):
                model = loaded_data[key]
                print(f"Found model in key: '{key}'")
                break
    
    if model:
        print(f"✅ Model type: {type(model)}")
        
        # Check model attributes to find expected features
        if hasattr(model, 'n_features_in_'):
            print(f"Expected number of features: {model.n_features_in_}")
        
        if hasattr(model, 'feature_names_in_'):
            print(f"Feature names: {list(model.feature_names_in_)}")
        
        if hasattr(model, 'estimators_'):
            print(f"Number of trees: {len(model.estimators_)}")
            
        # Try to get feature importance
        if hasattr(model, 'feature_importances_'):
            print(f"Feature importances available: Yes")
            print(f"Number of feature importances: {len(model.feature_importances_)}")
        
        # Test what happens with wrong number of features
        print("\nTesting feature requirements:")
        try:
            # Test with 8 features (current)
            test_8 = np.random.random((1, 8))
            prediction = model.predict(test_8)
            print("✅ Model works with 8 features")
        except Exception as e:
            print(f"❌ 8 features failed: {e}")
            
        try:
            # Test with 12 features (expected)
            test_12 = np.random.random((1, 12))
            prediction = model.predict(test_12)
            print("✅ Model works with 12 features")
        except Exception as e:
            print(f"❌ 12 features failed: {e}")
            
    else:
        print("❌ No model found in the file")
        if isinstance(loaded_data, dict):
            print(f"Dictionary keys: {list(loaded_data.keys())}")
            
except Exception as e:
    print(f"❌ Error: {e}")