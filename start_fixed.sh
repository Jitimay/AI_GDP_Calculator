#!/bin/bash
echo "🌍 Starting AI GDP Calculator"
echo "=============================="

cd /home/josh/Kiro/ai-gdp-calculator
source venv/bin/activate

# Generate sample data if needed
python -c "from data_ingestion import DataIngestion; DataIngestion().generate_sample_data()"

echo "🚀 Starting API server..."
python api.py &
API_PID=$!

sleep 5

echo "🔍 Testing API..."
if curl -s http://localhost:5000/health > /dev/null; then
    echo "✅ API running on http://localhost:5000"
    echo ""
    echo "📊 Start dashboard with:"
    echo "   streamlit run dashboard.py"
    echo ""
    echo "🛑 Stop API with:"
    echo "   kill $API_PID"
else
    echo "❌ API failed to start"
    kill $API_PID 2>/dev/null
fi
