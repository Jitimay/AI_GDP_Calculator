# 🌍 AI-Powered GDP Calculator

Real-time AI platform that estimates Burundi's informal economy GDP using multi-source data fusion and machine learning.

## 🚀 Quick Start

```bash
# Install dependencies
source venv/bin/activate
pip install -r requirements.txt

# Start system
./start.sh
```

**Access:**
- API: http://localhost:5000
- Dashboard: http://localhost:8501

## 📊 Features

- **Real-time GDP estimation** using 5 data sources
- **ML predictions** with Random Forest model
- **Interactive dashboard** with live charts
- **Elasticsearch storage** for scalable data handling
- **RESTful API** for data access

## 🏗️ Architecture

```
Data Sources → Fusion Engine → ML Model → Elasticsearch → API → Dashboard
```

## 📁 Project Structure

```
├── api.py              # Flask API server
├── dashboard.py        # Streamlit dashboard
├── config.json         # Configuration
├── start.sh           # Start script
├── modules/           # Core modules
│   ├── fusion_engine.py
│   ├── ml_model.py
│   ├── es_client.py
│   └── ...
├── data/             # CSV data files
└── docs/             # Documentation
```

## 🔧 API Endpoints

- `GET /health` - Health check
- `GET /predict` - Real-time GDP predictions
- `GET /dashboard-data` - Dashboard data

## 🌍 Data Sources

1. **Mobile Money** (30%) - Transaction volumes
2. **Electricity** (25%) - Consumption patterns  
3. **Internet** (20%) - Usage data
4. **Satellite** (15%) - Market density
5. **Social Media** (10%) - Commercial activity

Built for making invisible economies visible through AI.
