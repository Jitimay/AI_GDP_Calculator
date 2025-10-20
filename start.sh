#!/bin/bash
echo "🌍 AI GDP Calculator - Clean Setup"
echo "=================================="

# Start Elasticsearch
echo "🔍 Starting Elasticsearch..."
docker-compose up -d elasticsearch

# Wait for ES
echo "⏳ Waiting for Elasticsearch..."
sleep 15

# Start API
echo "🚀 Starting API..."
source venv/bin/activate
python api.py &

# Start Dashboard
echo "📊 Starting Dashboard..."
streamlit run dashboard.py --server.port 8501 &

echo "✅ System started!"
echo "API: http://localhost:5000"
echo "Dashboard: http://localhost:8501"
