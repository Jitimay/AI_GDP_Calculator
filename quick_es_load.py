#!/usr/bin/env python3
from es_client import SimpleElasticsearchClient
from fusion_engine import FusionEngine
import time

print("🚀 Loading data into Elasticsearch for hackathon...")

# Initialize
es_client = SimpleElasticsearchClient()
fusion_engine = FusionEngine()

# Wait for ES to be ready
time.sleep(5)

# Generate and save sample data
for i in range(10):
    print(f"Loading batch {i+1}/10...")
    provincial_results = fusion_engine.process_realtime_data()
    national_index = fusion_engine.calculate_national_index(provincial_results)
    es_client.save_gdp_data(provincial_results, national_index)
    time.sleep(1)

print("✅ Sample data loaded into Elasticsearch!")
print("🎯 Hackathon ready - Elasticsearch is now the primary data store!")
