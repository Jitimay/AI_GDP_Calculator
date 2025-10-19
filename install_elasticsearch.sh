#!/bin/bash

echo "🚀 Installing Elasticsearch for GDP Calculator"

# Step 1: Install Python dependencies
echo "📦 Installing Python packages..."
pip install elasticsearch==8.11.0

# Step 2: Start Elasticsearch with Docker
echo "🐳 Starting Elasticsearch with Docker..."
docker run -d \
  --name gdp-elasticsearch \
  -p 9200:9200 \
  -p 9300:9300 \
  -e "discovery.type=single-node" \
  -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" \
  -e "xpack.security.enabled=false" \
  docker.elastic.co/elasticsearch/elasticsearch:8.11.0

echo "⏳ Waiting for Elasticsearch to start..."
sleep 30

# Step 3: Test connection
echo "🔍 Testing Elasticsearch connection..."
curl -X GET "localhost:9200/_cluster/health?pretty"

echo ""
echo "✅ Elasticsearch Setup Complete!"
echo ""
echo "🎯 Next Steps:"
echo "1. Run: python api.py"
echo "2. Test: curl http://localhost:5000/health"
echo "3. Check Elasticsearch: curl http://localhost:9200"
echo ""
echo "📊 Your GDP data will now be stored in Elasticsearch for fast analytics!"