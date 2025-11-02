import json
import math

# Extracted from trained model (failure_risk_model.pkl)
# Model coefficients for [temperature, vibration]
COEFFICIENTS = [1.11367186, 0.29908045]
INTERCEPT = -102.55495755

def sigmoid(z):
    """Sigmoid activation function"""
    return 1 / (1 + math.exp(-z))

def predict_failure_risk(temperature, vibration, pressure, speed):
    """
    Predict failure risk using logistic regression formula
    Risk = sigmoid(intercept + coef1*temp + coef2*vibration)
    
    Note: Model only uses temperature and vibration (pressure/speed had low importance)
    """
    # Calculate linear combination
    z = INTERCEPT + (COEFFICIENTS[0] * temperature) + (COEFFICIENTS[1] * vibration)
    
    # Apply sigmoid to get probability
    risk_score = sigmoid(z)
    
    return risk_score

def lambda_handler(event, context):
    """AWS Lambda handler function"""
    try:
        # Parse input - handle both direct invocation and API Gateway proxy format
        if 'body' in event:
            # API Gateway proxy integration - body is a JSON string
            data = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        elif isinstance(event, str):
            # Direct string input
            data = json.loads(event)
        else:
            # Direct dict input
            data = event
        
        # Debug logging (will appear in CloudWatch)
        print(f"Parsed data: {data}")
            
        # Extract sensor readings
        temperature = float(data.get('temperature', 0))
        vibration = float(data.get('vibration', 0))
        pressure = float(data.get('pressure', 0))
        speed = float(data.get('speed', 0))
        
        print(f"Extracted values - temp: {temperature}, vib: {vibration}, pressure: {pressure}, speed: {speed}")
        
        # Validate inputs
        if temperature <= 0 or vibration <= 0:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Invalid sensor readings. Temperature and vibration must be positive.'
                })
            }
        
        # Calculate risk
        risk_score = predict_failure_risk(temperature, vibration, pressure, speed)
        
        # Determine risk level
        if risk_score >= 0.7:
            risk_level = 'Critical'
        elif risk_score >= 0.4:
            risk_level = 'High'
        elif risk_score >= 0.2:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
        
        # Return prediction
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'risk_score': round(risk_score, 4),
                'risk_level': risk_level,
                'sensor_id': data.get('sensor_id', 'unknown'),
                'inputs': {
                    'temperature': temperature,
                    'vibration': vibration,
                    'pressure': pressure,
                    'speed': speed
                }
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Internal server error during prediction'
            })
        }
