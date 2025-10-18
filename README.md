# 🌍 AI-Powered Informal Sector GDP Calculator

A real-time AI platform that estimates and visualizes the GDP of Burundi's informal economy by analyzing multi-source signals including mobile money transactions, electricity consumption, internet usage, satellite imagery, and social media commerce indicators.

## 🎯 Features

- **Real-time GDP Estimation**: Live calculation of informal economy index
- **Multi-source Data Fusion**: Combines 5 different economic indicators
- **ML-Powered Predictions**: Random Forest model for GDP forecasting
- **Interactive Dashboard**: Live visualization with maps and charts
- **Alert System**: Automatic detection of economic activity spikes
- **RESTful API**: JSON endpoints for data access

## 🚀 Quick Start

### 1. Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Start the System
```bash
./start_system.sh
```

### 3. Access the System
- **API**: http://localhost:5000
- **Dashboard**: http://localhost:8501
- **Test**: `python test_system.py`

## 📊 API Endpoints

- `GET /health` - Health check
- `GET /predict` - Real-time GDP predictions
- `GET /dashboard-data` - Dashboard data with history
- `GET /alerts` - Activity alerts
- `POST /train-model` - Train ML model

## 🏗️ Architecture

```
Data Sources → Fusion Engine → ML Model → API → Dashboard
```

## 🧠 ML Model

- **Algorithm**: Random Forest Regressor
- **Features**: 5 normalized economic indicators
- **Performance**: R² score ~0.66
- **Target**: Informal GDP Index (0-100 scale)

## 🌍 Data Sources

1. **Mobile Money**: Transaction volumes and counts
2. **Electricity**: Consumption patterns (kWh)
3. **Internet**: Data usage (GB)
4. **Satellite**: Market density analysis
5. **Social Media**: Commercial keyword detection

## 📈 Sample Response

```json
{
  "national_index": 67.5,
  "provincial_data": {
    "Bujumbura": {
      "composite_index": 75.2,
      "ml_prediction": 73.8,
      "indicators": {
        "mobile_money": 80.5,
        "electricity": 70.2,
        "internet": 85.1,
        "satellite": 75.0,
        "social_media": 65.3
      }
    }
  }
}
```

## 🎮 Demo

The system generates live economic insights like:
- "Bujumbura showing 85% activity spike"
- "National informal GDP index: 67.5/100"
- "Mobile money transactions up 15% in Gitega"

## 🏆 Impact

Makes invisible informal economic activity visible in real-time, enabling:
- Better policy decisions
- Economic monitoring
- Development planning
- Crisis response

---

**Built for making the invisible economy visible through AI.**
# AI_GDP_Calculator
