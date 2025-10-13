import pickle
import sklearn
import numpy as np

print("Python version info:")
print(f"scikit-learn version: {sklearn.__version__}")

try:
    with open('rainfall_prediction_model.pkl', 'rb') as file:
        loaded_data = pickle.load(file)
    
    print("\n✅ File loaded successfully!")
    print(f"Type of loaded object: {type(loaded_data)}")
    print(f"Object keys (if dictionary): {list(loaded_data.keys()) if isinstance(loaded_data, dict) else 'Not a dictionary'}")
    
    # Check if it's a scikit-learn model
    if hasattr(loaded_data, 'predict'):
        print("✅ Object has predict method - it's a model!")
        print(f"Model type: {type(loaded_data)}")
    elif isinstance(loaded_data, dict):
        print("📁 Object is a dictionary. Checking contents...")
        for key, value in loaded_data.items():
            print(f"  {key}: {type(value)}")
            if hasattr(value, 'predict'):
                print(f"    ✅ '{key}' has predict method - it's the model!")
    
except Exception as e:
    print(f"❌ Error: {e}")