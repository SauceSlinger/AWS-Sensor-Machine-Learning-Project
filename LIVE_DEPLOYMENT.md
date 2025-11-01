# 🚀 Live Deployment Information

## Project Status: **FULLY DEPLOYED AND OPERATIONAL**

This AWS Serverless Machine Learning Pipeline is now live and operational!

---

## 🌐 Live Dashboard

**URL:** https://sauceslinger.github.io/AWS-Sensor-Machine-Learning-Project/

The dashboard provides:
- Real-time ML-powered failure risk predictions
- Interactive visualization with Chart.js
- Failure alert system with detailed diagnostics
- Search and filtering capabilities
- Live sensor monitoring for 100+ components

---

## ⚡ AWS Lambda Function

**Region:** us-west-2  
**Function Name:** `manufacturing-risk-predictor`  
**Runtime:** Python 3.12  
**Deployment Size:** 1.3 KB (optimized, no dependencies)  
**Memory:** 512 MB  
**Timeout:** 30 seconds

### Model Details:
- **Algorithm:** Logistic Regression (hardcoded coefficients)
- **Features:** Temperature, Vibration
- **Training Accuracy:** 100% on test set
- **Deployment:** Coefficients extracted from `failure_risk_model.pkl`

---

## 🔌 API Gateway

**Endpoint:** https://0wpit90c06.execute-api.us-west-2.amazonaws.com/prod/predict  
**Method:** POST  
**Type:** REST API  
**Stage:** prod

### Request Format:
```json
{
  "sensor_id": "SENSOR-001",
  "temperature": 95.5,
  "vibration": 3.2,
  "pressure": 98.1,
  "speed": 1500
}
```

### Response Format:
```json
{
  "risk_score": 0.9915,
  "risk_level": "Critical",
  "sensor_id": "SENSOR-001",
  "inputs": {
    "temperature": 95.5,
    "vibration": 3.2,
    "pressure": 98.1,
    "speed": 1500.0
  }
}
```

---

## 📊 Architecture

```
┌─────────────────┐
│  GitHub Pages   │  ← Frontend Dashboard (index.html)
│  (User Browser) │
└────────┬────────┘
         │ HTTPS
         ↓
┌─────────────────┐
│  API Gateway    │  ← REST API Endpoint
│   (us-west-2)   │
└────────┬────────┘
         │ Invoke
         ↓
┌─────────────────┐
│  Lambda Function│  ← ML Prediction Logic
│ manufacturing-  │     (No dependencies!)
│ risk-predictor  │
└─────────────────┘
```

---

## 💰 Cost Optimization

**Target:** Stay within AWS Free Tier
- Lambda: 1M requests/month free
- API Gateway: 1M requests/month free (first 12 months)
- CloudWatch Logs: 7-day retention configured
- **Estimated Monthly Cost:** $0.00 (within free tier limits)

### Billing Alert Configured:
- Budget: $1.00/month
- Alert Threshold: 50% ($0.50)
- Email notifications enabled

---

## 🧪 Testing the Live System

### Test via curl:
```bash
curl -X POST https://0wpit90c06.execute-api.us-west-2.amazonaws.com/prod/predict \
  -H "Content-Type: application/json" \
  -d '{"sensor_id": "TEST-001", "temperature": 105.5, "vibration": 6.2, "pressure": 98.1, "speed": 1500}'
```

### Test via Dashboard:
1. Visit: https://sauceslinger.github.io/AWS-Sensor-Machine-Learning-Project/
2. Click **"Load Data from Lambda"** button
3. Dashboard will fetch 100 real predictions from AWS Lambda
4. View results in interactive charts and tables

---

## 📈 Model Performance

- **Training Data:** 5,000 sensor records
- **Features:** Temperature, Vibration, Pressure, Speed
- **Model Type:** Logistic Regression
- **Test Accuracy:** 100%
- **Failure Rate in Training Data:** 5% (250 failures)

### Risk Classification:
- **Critical:** Risk Score ≥ 0.7
- **High:** Risk Score ≥ 0.4
- **Medium:** Risk Score ≥ 0.2
- **Low:** Risk Score < 0.2

---

## 🔧 Development Timeline

1. ✅ Local model training (scikit-learn)
2. ✅ Lambda deployment package optimization
3. ✅ Size limit bypass (extracted coefficients)
4. ✅ API Gateway configuration
5. ✅ GitHub Pages activation
6. ✅ Frontend-backend integration
7. ✅ Live deployment verification

---

## 📝 Key Files

- `index.html` - Interactive dashboard (GitHub Pages)
- `lambda_function_simple.py` - AWS Lambda handler (deployed)
- `train_model.py` - Model training script
- `failure_risk_model.pkl` - Trained model (857 bytes)
- `raw_manufacturing_logs.csv` - Training data (210 KB)

---

## 🎯 Project Achievements

✅ Full serverless ML pipeline on AWS  
✅ 100% test accuracy ML model  
✅ Real-time predictions via API Gateway  
✅ Interactive dashboard with failure alerts  
✅ Cost-optimized (free tier compliant)  
✅ No dependency Lambda deployment  
✅ CORS-enabled for browser integration  
✅ Production-ready monitoring & alerts  

---

## 🚀 Next Steps (Optional Enhancements)

- [ ] Add authentication (API keys/Cognito)
- [ ] Implement caching (DynamoDB/ElastiCache)
- [ ] Add CloudWatch dashboards
- [ ] Set up CI/CD pipeline (GitHub Actions)
- [ ] Implement A/B testing for model versions
- [ ] Add WebSocket support for real-time updates
- [ ] Expand to multi-region deployment
- [ ] Add SageMaker integration for model retraining

---

**Deployment Date:** November 1, 2025  
**Status:** ✅ LIVE AND OPERATIONAL  
**Maintained By:** Sebastian Velasco (Sauce Slinger)
