# 🎯 Final Testing Guide - AWS Lambda Integration

## 🌐 Live URLs

### Main Dashboard
**URL:** https://sauceslinger.github.io/AWS-Sensor-Machine-Learning-Project/

### Debug/Test Pages
- **API Debug Tool:** https://sauceslinger.github.io/AWS-Sensor-Machine-Learning-Project/debug-api.html
- **Simple API Test:** https://sauceslinger.github.io/AWS-Sensor-Machine-Learning-Project/test-api.html

---

## ✅ How to Test Live AWS Connection

### Step 1: Clear Browser Cache
To see the latest changes:
- **Windows/Linux:** Press `Ctrl + Shift + R` or `Ctrl + F5`
- **Mac:** Press `Cmd + Shift + R`

### Step 2: Open Developer Console
Press `F12` to open browser DevTools and switch to **Console** tab

### Step 3: Load Data
Click the **"Load Data from Lambda"** button

### Step 4: Verify Connection
Watch for these indicators:

#### ✅ Success Indicators:
1. **Header Badge Changes:**
   - Before: `⚪ Offline Mode` (gray)
   - After: `🟢 Live - AWS Connected` (green, pulsing)

2. **Console Messages:**
   ```
   Starting API data load from: https://0wpit90c06...
   API Connection Test Response: {statusCode: 200, ...}
   Successfully received 50 predictions from AWS Lambda
   ```

3. **Success Message:**
   ```
   🚀 SUCCESS! Loaded 50 records with REAL ML predictions from AWS Lambda (us-west-2)
   ```

4. **Status Messages Sequence:**
   - `🔄 Connecting to AWS Lambda API...`
   - `🔌 Testing API connection...`
   - `✅ API Connection Verified! Loading sensor data...`
   - `⏳ Processing 50 sensor predictions from AWS Lambda...`
   - `🚀 SUCCESS! Loaded 50 records with REAL ML predictions...`

#### ❌ Failure Indicators:
1. **Header Badge:**
   - Shows: `🔴 Offline - Sample Data` (red)

2. **Error Message:**
   ```
   ❌ API Connection Failed: [error message]. Using offline sample data.
   ```

---

## 🧪 Quick API Test (Without Loading Data)

### Method 1: Using curl
```bash
curl -X POST https://0wpit90c06.execute-api.us-west-2.amazonaws.com/prod/predict \
  -H "Content-Type: application/json" \
  -d '{"sensor_id": "TEST-001", "temperature": 95.5, "vibration": 3.2, "pressure": 98.1, "speed": 1500}'
```

**Expected Response:**
```json
{
  "statusCode": 200,
  "body": "{\"risk_score\": 0.9915, \"risk_level\": \"Critical\", ...}"
}
```

### Method 2: Visit Debug Page
Go to: https://sauceslinger.github.io/AWS-Sensor-Machine-Learning-Project/debug-api.html

This page will:
- Auto-run API test on load
- Show detailed request/response logs
- Display timing information
- Parse and format all responses

---

## 🔍 Troubleshooting

### Problem: Still Shows "Offline Mode"

**Solutions:**
1. **Hard refresh** the page (Ctrl+Shift+R)
2. **Clear browser cache completely**
3. Try in **Incognito/Private window**
4. Wait 2-3 minutes for GitHub Pages CDN to update
5. Check console (F12) for JavaScript errors

### Problem: Badge Doesn't Change Color

**Check:**
1. Open Console (F12)
2. Look for error messages
3. Verify you clicked "Load Data from Lambda" button
4. Check if `getElementById('connectionStatus')` returns null

### Problem: API Connection Fails

**Verify:**
1. Lambda function is running in AWS console
2. API Gateway endpoint is active
3. CORS is enabled on API Gateway
4. No AWS account issues (billing, permissions)

---

## 📊 What's Happening Behind the Scenes

When you click "Load Data from Lambda":

1. **Connection Test** (1 API call)
   - Tests `/predict` endpoint with sample data
   - Verifies response format
   - Updates badge to green on success

2. **Data Loading** (50 API calls in parallel)
   - Generates 50 sensor readings
   - Sends each to Lambda for ML prediction
   - Collects all responses
   - Sorts by risk score

3. **Dashboard Update**
   - Updates statistics
   - Renders chart with predictions
   - Populates table
   - Shows failure alerts if any

**Total API Calls:** 51 (1 test + 50 predictions)
**Expected Time:** 2-5 seconds
**Lambda Cost:** $0.00 (within free tier)

---

## 📈 Current Deployment Status

| Component | Status | Details |
|-----------|--------|---------|
| **GitHub Pages** | ✅ Live | https://sauceslinger.github.io/AWS-Sensor-Machine-Learning-Project/ |
| **AWS Lambda** | ✅ Active | us-west-2, manufacturing-risk-predictor |
| **API Gateway** | ✅ Active | REST API, prod stage |
| **Connection Badge** | ✅ Deployed | Shows real-time status |
| **Error Handling** | ✅ Enabled | Falls back to sample data |
| **CORS** | ✅ Configured | Allows browser requests |

---

## 🎯 Success Criteria

You'll know everything is working when:
- ✅ Badge shows `🟢 Live - AWS Connected`
- ✅ Console shows 50 successful API calls
- ✅ Chart displays varying risk scores (0.0 - 1.0)
- ✅ Some sensors show "Critical" or "High" risk
- ✅ Success message mentions "REAL ML predictions from AWS Lambda"

---

## 📝 Latest Changes (Committed)

1. **API Integration** - Connects to real AWS Lambda
2. **Connection Status Badge** - Visual indicator in header
3. **Enhanced Logging** - Detailed console messages
4. **Error Handling** - Graceful fallback to sample data
5. **Debug Tools** - Two test pages for verification

**Last Commit:** `79bdc97` - Add detailed API debugging page
**Branch:** `main`
**All changes pushed:** ✅ Yes

---

## 🚀 Next Steps

1. Visit the dashboard
2. Hard refresh (Ctrl+Shift+R)
3. Click "Load Data from Lambda"
4. Confirm green badge appears
5. Enjoy real-time ML predictions! 🎉

---

**Note:** GitHub Pages may take 1-3 minutes to deploy the latest changes after each push.
