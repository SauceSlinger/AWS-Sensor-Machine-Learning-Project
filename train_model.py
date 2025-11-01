"""
ML Model Training Script
Trains a Logistic Regression classifier to predict component failure risk.

Development Note: Created with AI assistance (Gemini/GitHub Copilot) for rapid ML deployment.
"""

import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

# Configuration
INPUT_FILE = "raw_manufacturing_logs.csv"
MODEL_OUTPUT = "failure_risk_model.pkl"
RANDOM_STATE = 42


def load_data():
    """Load the generated manufacturing logs."""
    df = pd.read_csv(INPUT_FILE)
    return df


def train_model(df):
    """Train a Logistic Regression model on temperature and vibration data."""
    # Feature engineering: select predictive features
    X = df[['component_temp_C', 'vibration_level']]
    y = df['historical_failure_status']
    
    # Split data for validation
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    
    # Train Logistic Regression classifier
    model = LogisticRegression(random_state=RANDOM_STATE, max_iter=1000)
    model.fit(X_train, y_train)
    
    # Evaluate model (minimal output for cost control)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    return model, accuracy, y_test, y_pred


def save_model(model, filename):
    """Serialize the trained model using pickle."""
    with open(filename, 'wb') as f:
        pickle.dump(model, f)


def main():
    """Main training pipeline."""
    # Load data
    df = load_data()
    
    # Train model
    model, accuracy, y_test, y_pred = train_model(df)
    
    # Save model
    save_model(model, MODEL_OUTPUT)
    
    # Summary output only (cost control: minimal printing)
    print(f"✓ Training completed on {len(df)} records")
    print(f"✓ Model accuracy: {accuracy:.2%}")
    print(f"✓ Model serialized to: {MODEL_OUTPUT}")
    print(f"✓ Model ready for Lambda deployment")


if __name__ == "__main__":
    main()
