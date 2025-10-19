# Manual Testing Guide

## Step 1: Start the API Server
```bash
cd /home/josh/Kiro/ai-gdp-calculator
source venv/bin/activate
python api.py
```
Keep this terminal open. You should see:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

## Step 2: Test API (New Terminal)
```bash
# Test health
curl http://localhost:5000/health

# Test GDP prediction
curl http://localhost:5000/predict

# Test alerts
curl http://localhost:5000/alerts

# Train model
curl -X POST http://localhost:5000/train-model
```

## Step 3: Start Dashboard (New Terminal)
```bash
cd /home/josh/Kiro/ai-gdp-calculator
source venv/bin/activate
streamlit run dashboard.py
```

## Step 4: View Dashboard
Open browser: http://localhost:8501

## Expected Results:
- ✅ API returns JSON responses
- ✅ GDP index values between 0-100
- ✅ Dashboard shows charts and maps
- ✅ Real-time data updates

## Troubleshooting:
- If API fails: Check `api.log` for errors
- If dashboard fails: Check `streamlit.log` for errors
- If missing data: Run `python -c "from data_ingestion import DataIngestion; DataIngestion().generate_sample_data()"`
