#!/bin/bash

echo "🌍 Starting AI-Powered Informal Sector GDP Calculator"
echo "======================================================"

# Create and activate virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Start API server
echo "🚀 Starting API server..."
nohup python api.py > api.log 2>&1 &
API_PID=$!

# Wait for API to start
sleep 5

# Test API
echo "🔍 Testing API connection..."
if curl -s http://localhost:5000/health > /dev/null; then
    echo "✅ API server running on http://localhost:5000"
else
    echo "❌ API server failed to start"
    exit 1
fi

# Start Streamlit dashboard
echo "📊 Starting dashboard..."
nohup streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0 --server.headless true > streamlit.log 2>&1 &
STREAMLIT_PID=$!

# Wait for Streamlit to start
sleep 10

echo ""
echo "🎯 System Status:"
echo "  API Server: http://localhost:5000"
echo "  Dashboard: http://localhost:8501"
echo ""
echo "📋 Available Endpoints:"
echo "  GET  /health        - Health check"
echo "  GET  /predict       - GDP predictions"
echo "  POST /train-model   - Train ML model"
echo "  GET  /alerts        - Active alerts"
echo "  GET  /dashboard-data - Dashboard data"
echo ""
echo "🛑 To stop the system:"
echo "  kill $API_PID $STREAMLIT_PID"
echo ""
echo "✨ System ready! Open http://localhost:8501 to view the dashboard"
