# 🚀 Quick Demo URLs

## 🎯 **Instant Demo Links:**

### **Main Dashboard**
http://localhost:8501

### **API Endpoints**
- **Health Check**: http://localhost:5000/health
- **Real-time Predictions**: http://localhost:5000/predict  
- **Search Bujumbura**: http://localhost:5000/search?province=Bujumbura&metric=electricity&days=5
- **6-Month Forecast**: http://localhost:5000/forecast?province=Bujumbura&months=6
- **All Provinces Forecast**: http://localhost:5000/forecast?province=all&months=3

### **Terminal Tests**
```bash
# Test Google Cloud + Elasticsearch
curl localhost:5000/health | jq '.hackathon_compliant'

# Test Vertex AI predictions  
curl localhost:5000/predict | jq '.google_cloud_vertex_ai'

# Test search functionality
curl "localhost:5000/search?province=Gitega&metric=mobile_money&days=7"

# Test forecasting
curl "localhost:5000/forecast?months=12" | jq '.vertex_ai_powered'
```

## 🏆 **Demo Flow:**
1. **Show Dashboard** → http://localhost:8501
2. **Show Health** → http://localhost:5000/health  
3. **Show Search** → Sidebar search panel
4. **Show Forecast** → Sidebar forecast panel
5. **Show API** → Terminal commands above

**Total Demo Time: 2 minutes** ⏱️
