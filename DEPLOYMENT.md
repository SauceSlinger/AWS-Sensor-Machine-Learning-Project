# AWS Lambda Deployment Instructions

## 📦 Creating the Lambda Deployment Package

AWS Lambda requires all dependencies to be packaged together with your function code. Follow these steps:

### Step 1: Prepare the Deployment Directory

```bash
# Create deployment directory
mkdir lambda_deployment
cd lambda_deployment
```

### Step 2: Install Dependencies for Lambda

Lambda runs on Amazon Linux 2, so we need to install packages in a compatible way:

```bash
# Install dependencies to a 'package' directory
pip install --target ./package pandas scikit-learn

# Copy your Lambda function
cp ../lambda_function.py package/
cp ../failure_risk_model.pkl package/
```

### Step 3: Create the Deployment ZIP

```bash
# Navigate to package directory and create zip
cd package
zip -r ../lambda_deployment.zip .
cd ..
```

Your `lambda_deployment.zip` is now ready for upload to AWS Lambda!

### Step 4: Upload to AWS Lambda

#### Option A: AWS Console
1. Go to AWS Lambda Console
2. Create a new function (Python 3.12 runtime)
3. Upload `lambda_deployment.zip` under "Code source"
4. Set Handler to: `lambda_function.lambda_handler`
5. Increase timeout to 30 seconds (Configuration → General)
6. Increase memory to 512 MB (for scikit-learn)

#### Option B: AWS CLI
```bash
# Create Lambda function
aws lambda create-function \
  --function-name manufacturing-risk-predictor \
  --runtime python3.12 \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-execution-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://lambda_deployment.zip \
  --timeout 30 \
  --memory-size 512

# Update existing function
aws lambda update-function-code \
  --function-name manufacturing-risk-predictor \
  --zip-file fileb://lambda_deployment.zip
```

## 📊 Testing Your Lambda Function

### Test Event JSON

```json
{
  "records": [
    {
      "timestamp": "2025-10-31 12:00:00",
      "serial_number": "SN-100001",
      "component_temp_C": 75.5,
      "vibration_level": 1.2
    },
    {
      "timestamp": "2025-10-31 12:10:00",
      "serial_number": "SN-100002",
      "component_temp_C": 105.3,
      "vibration_level": 5.8
    },
    {
      "timestamp": "2025-10-31 12:20:00",
      "serial_number": "SN-100003",
      "component_temp_C": 68.2,
      "vibration_level": 1.5
    }
  ]
}
```

## 🔧 Free Tier Configuration

### CloudWatch Logs (REQUIRED)
1. Go to CloudWatch → Log groups
2. Find `/aws/lambda/manufacturing-risk-predictor`
3. Actions → Edit retention setting → 7 days

### Environment Variables (Optional)
- `LOG_LEVEL`: `WARNING` (reduces log verbosity)
- `MODEL_FILE`: `failure_risk_model.pkl`

## 🌐 API Gateway Setup (Optional - for Frontend Integration)

To connect your frontend to Lambda:

1. Create REST API in API Gateway
2. Create resource `/predict`
3. Create POST method → Link to Lambda function
4. Enable CORS
5. Deploy API to stage (e.g., `prod`)
6. Update `index.html` with API endpoint URL

## 📈 Monitoring & Cost Control

### CloudWatch Alarms
```bash
# Create billing alarm (set up via AWS Console → Billing → Budgets)
# Or use CloudWatch:
aws cloudwatch put-metric-alarm \
  --alarm-name lambda-invocations-limit \
  --alarm-description "Alert if Lambda invocations exceed free tier" \
  --metric-name Invocations \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 2592000 \
  --threshold 1000000 \
  --comparison-operator GreaterThanThreshold
```

### Free Tier Limits
- ✅ Lambda: 1M requests/month + 400,000 GB-seconds compute
- ✅ API Gateway: 1M requests/month (12 months)
- ✅ CloudWatch: 5GB logs (Always Free)

## 🚀 Expected Package Size

- scikit-learn: ~40 MB
- pandas: ~35 MB
- Lambda function: <1 MB
- ML model: ~1 KB
- **Total: ~76 MB** (well under 250 MB unzipped limit)

## 🧪 Local Testing

Test your Lambda function locally before deployment:

```bash
# Activate virtual environment
source .venv/bin/activate

# Run Lambda function locally
python lambda_function.py
```

This will execute the test event at the bottom of `lambda_function.py`.
