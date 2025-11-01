"""
AWS Lambda Function: Intelligent Manufacturing Validator with ML Risk Prediction
Validates sensor data and predicts failure risk using pre-trained ML model.

Development Note: Created with AI assistance (Gemini/GitHub Copilot) for serverless ML deployment.
Cost Control: Minimal logging, efficient data structures, optimized for AWS Free Tier.
"""

import json
import pickle
import os

# Validation thresholds
MIN_TEMP_TOLERANCE = 50.0  # Celsius
MAX_TEMP_TOLERANCE = 120.0
MIN_VIBRATION_TOLERANCE = 0.0
MAX_VIBRATION_TOLERANCE = 10.0

# Model file path (in Lambda deployment package)
MODEL_FILE = "failure_risk_model.pkl"


def load_model():
    """Load the pre-trained ML model from the deployment package."""
    model_path = os.path.join(os.path.dirname(__file__), MODEL_FILE)
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model


def validate_record(record):
    """
    Validate a single record for type safety and range compliance.
    Returns: (is_valid, error_message)
    """
    try:
        # Type conversion and extraction
        temp = float(record.get('component_temp_C', 0))
        vibration = float(record.get('vibration_level', 0))
        
        # Range validation
        if not (MIN_TEMP_TOLERANCE <= temp <= MAX_TEMP_TOLERANCE):
            return False, f"Temperature {temp}°C out of range"
        
        if not (MIN_VIBRATION_TOLERANCE <= vibration <= MAX_VIBRATION_TOLERANCE):
            return False, f"Vibration {vibration} out of range"
        
        return True, None
        
    except (ValueError, TypeError) as e:
        return False, f"Invalid data type: {str(e)}"


def predict_failure_risk(model, record):
    """
    Predict failure risk score (0-1 probability) for a single record.
    Returns: float between 0 and 1
    """
    temp = float(record['component_temp_C'])
    vibration = float(record['vibration_level'])
    
    # Create feature array matching training format
    features = [[temp, vibration]]
    
    # Get probability of failure (class 1)
    failure_probability = model.predict_proba(features)[0][1]
    
    return round(failure_probability, 4)


def lambda_handler(event, context):
    """
    Main Lambda handler function.
    
    Expected event format:
    {
        "records": [
            {
                "timestamp": "2025-10-01 12:00:00",
                "serial_number": "SN-100001",
                "component_temp_C": 75.5,
                "vibration_level": 1.2
            },
            ...
        ]
    }
    
    Returns: JSON with validated records, failure risk scores, and summary statistics.
    """
    try:
        # Load ML model (cached after first invocation due to container reuse)
        model = load_model()
        
        # Extract records from event
        records = event.get('records', [])
        
        if not records:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No records provided'})
            }
        
        # Process records
        validated_records = []
        failed_records = []
        pass_count = 0
        fail_count = 0
        
        for record in records:
            is_valid, error_msg = validate_record(record)
            
            if is_valid:
                # Predict failure risk
                risk_score = predict_failure_risk(model, record)
                
                # Add risk score to record
                enriched_record = {
                    **record,
                    'failure_risk_score': risk_score,
                    'validation_status': 'PASS'
                }
                validated_records.append(enriched_record)
                pass_count += 1
            else:
                # Record validation failure
                failed_record = {
                    **record,
                    'validation_status': 'FAIL',
                    'error': error_msg
                }
                failed_records.append(failed_record)
                fail_count += 1
        
        # Sort by risk score (highest first) for frontend convenience
        validated_records.sort(key=lambda x: x['failure_risk_score'], reverse=True)
        
        # Build response payload
        response_payload = {
            'summary': {
                'total_records': len(records),
                'passed': pass_count,
                'failed': fail_count,
                'pass_rate': round(pass_count / len(records) * 100, 2) if records else 0
            },
            'validated_records': validated_records,
            'failed_records': failed_records,
            'top_risk_components': validated_records[:10]  # Top 10 highest risk
        }
        
        # Minimal logging for cost control
        print(f"Processed {len(records)} records: {pass_count} passed, {fail_count} failed")
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # Enable CORS for GitHub Pages
            },
            'body': json.dumps(response_payload)
        }
        
    except Exception as e:
        # High-level error logging only
        print(f"ERROR: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal processing error'})
        }


# For local testing (not used in Lambda)
if __name__ == "__main__":
    # Sample test event
    test_event = {
        "records": [
            {
                "timestamp": "2025-10-01 12:00:00",
                "serial_number": "SN-100001",
                "component_temp_C": 75.5,
                "vibration_level": 1.2
            },
            {
                "timestamp": "2025-10-01 12:10:00",
                "serial_number": "SN-100002",
                "component_temp_C": 105.3,
                "vibration_level": 5.8
            }
        ]
    }
    
    result = lambda_handler(test_event, None)
    print(json.dumps(json.loads(result['body']), indent=2))
