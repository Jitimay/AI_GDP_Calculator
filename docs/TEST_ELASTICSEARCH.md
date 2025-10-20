# Testing Elasticsearch-Only Setup

## Quick Test (No Dependencies)
```bash
python3 test_simple.py
```
✅ Verifies SQLite removal and Elasticsearch usage

## Full System Test

### 1. Start Elasticsearch
```bash
docker-compose up -d elasticsearch
```

### 2. Wait for ES to be ready (30 seconds)
```bash
curl http://localhost:9202/_cluster/health
```

### 3. Start API
```bash
source venv/bin/activate
python api.py
```

### 4. Test API Endpoints
```bash
# Health check
curl http://localhost:5000/health

# Get predictions (saves to Elasticsearch)
curl http://localhost:5000/predict

# Get dashboard data
curl http://localhost:5000/dashboard-data
```

### 5. Start Dashboard
```bash
streamlit run dashboard.py
```
Visit: http://localhost:8501

## Verification
- ✅ No SQLite imports in code
- ✅ All data goes to Elasticsearch
- ✅ API works without .db files
- ✅ Dashboard shows real-time data
