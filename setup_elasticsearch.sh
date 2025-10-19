#!/bin/bash

echo "🔍 Setting up Elasticsearch for GDP Calculator"

# Option 1: Docker (Recommended - Easy)
echo "Starting Elasticsearch with Docker..."
docker run -d \
  --name elasticsearch \
  -p 9200:9200 \
  -p 9300:9300 \
  -e "discovery.type=single-node" \
  -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" \
  docker.elastic.co/elasticsearch/elasticsearch:8.11.0

# Option 2: Local Installation (Ubuntu/Debian)
# wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
# echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
# sudo apt update && sudo apt install elasticsearch

echo "✅ Elasticsearch starting on http://localhost:9200"
echo "Wait 30 seconds, then test: curl http://localhost:9200"