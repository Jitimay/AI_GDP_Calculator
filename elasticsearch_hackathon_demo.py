#!/usr/bin/env python3
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import time

print("🏆 HACKATHON: Elasticsearch GDP Analytics Demo")
print("=" * 55)

# Connect to Elasticsearch
es = Elasticsearch(['http://localhost:9202'], request_timeout=60)

# Create optimized index
mapping = {
    "mappings": {
        "properties": {
            "timestamp": {"type": "date"},
            "province": {"type": "keyword"},
            "district": {"type": "keyword"},
            "gdp_index": {"type": "float"},
            "mobile_money": {"type": "float"},
            "electricity": {"type": "float"},
            "internet": {"type": "float"},
            "social_media": {"type": "float"}
        }
    },
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    }
}

# Delete and create fresh index
try:
    es.indices.delete(index="gdp-hackathon")
except:
    pass

es.indices.create(index="gdp-hackathon", body=mapping)
print("✅ Created optimized Elasticsearch index")

# Load subset of massive dataset for demo
print("📊 Loading 50K records from massive dataset...")
mobile_df = pd.read_csv('mobile_money_massive.csv').head(50000)
electricity_df = pd.read_csv('electricity_massive.csv').head(50000)
internet_df = pd.read_csv('internet_massive.csv').head(50000)
social_df = pd.read_csv('social_massive.csv').head(50000)

print(f"   Processing {len(mobile_df):,} records per dataset")

# Prepare documents
docs = []
for i in range(len(mobile_df)):
    gdp_index = (
        mobile_df.iloc[i]['transaction_volume'] / 15 * 0.3 +
        electricity_df.iloc[i]['consumption_kwh'] / 6 * 0.25 +
        internet_df.iloc[i]['data_usage_gb'] / 3 * 0.2 +
        75 * 0.15 +  # satellite
        social_df.iloc[i]['commercial_keywords'] * 0.1
    )
    
    docs.append({
        "_index": "gdp-hackathon",
        "_source": {
            "timestamp": mobile_df.iloc[i]['timestamp'],
            "province": mobile_df.iloc[i]['province'],
            "district": mobile_df.iloc[i]['district'],
            "gdp_index": min(100, max(0, gdp_index)),
            "mobile_money": mobile_df.iloc[i]['transaction_volume'],
            "electricity": electricity_df.iloc[i]['consumption_kwh'],
            "internet": internet_df.iloc[i]['data_usage_gb'],
            "social_media": social_df.iloc[i]['commercial_keywords']
        }
    })

print(f"🚀 Bulk indexing {len(docs):,} documents...")
start_time = time.time()

# Bulk index in optimized chunks
chunk_size = 1000
indexed_count = 0

for i in range(0, len(docs), chunk_size):
    chunk = docs[i:i+chunk_size]
    try:
        bulk(es, chunk, request_timeout=60)
        indexed_count += len(chunk)
        if indexed_count % 10000 == 0:
            print(f"   ✅ Indexed {indexed_count:,} documents...")
    except Exception as e:
        print(f"   ⚠️  Error in chunk {i}: {str(e)[:100]}")

load_time = time.time() - start_time
print(f"⚡ Indexing completed in {load_time:.1f} seconds")

# Refresh and verify
es.indices.refresh(index="gdp-hackathon")
time.sleep(2)

try:
    count = es.count(index="gdp-hackathon")['count']
    print(f"✅ SUCCESS: {count:,} documents indexed in Elasticsearch")
    
    # Demo analytics
    print(f"\n🔍 ELASTICSEARCH ANALYTICS DEMO:")
    
    # 1. Top GDP provinces
    agg_result = es.search(
        index="gdp-hackathon",
        body={
            "size": 0,
            "aggs": {
                "top_provinces": {
                    "terms": {"field": "province", "size": 5},
                    "aggs": {"avg_gdp": {"avg": {"field": "gdp_index"}}}
                }
            }
        }
    )
    
    print("   Top 5 Provinces by GDP:")
    for bucket in agg_result['aggregations']['top_provinces']['buckets']:
        print(f"     {bucket['key']}: {bucket['avg_gdp']['value']:.1f} GDP")
    
    # 2. High GDP regions
    high_gdp = es.search(
        index="gdp-hackathon",
        body={
            "query": {"range": {"gdp_index": {"gte": 70}}},
            "size": 0
        }
    )
    
    print(f"\n   High GDP regions (>70): {high_gdp['hits']['total']['value']:,} records")
    
    # 3. Time-based analysis
    time_agg = es.search(
        index="gdp-hackathon",
        body={
            "size": 0,
            "aggs": {
                "gdp_over_time": {
                    "date_histogram": {
                        "field": "timestamp",
                        "calendar_interval": "month"
                    },
                    "aggs": {"avg_gdp": {"avg": {"field": "gdp_index"}}}
                }
            }
        }
    )
    
    monthly_data = time_agg['aggregations']['gdp_over_time']['buckets']
    print(f"\n   Monthly GDP trends ({len(monthly_data)} months analyzed)")
    
    print(f"\n🎉 HACKATHON DEMO SUCCESS!")
    print(f"   📊 {count:,} economic records in Elasticsearch")
    print(f"   ⚡ Load speed: {count/load_time:.0f} docs/second")
    print(f"   🔍 Real-time analytics working")
    print(f"   🏆 Ready for presentation!")
    
except Exception as e:
    print(f"❌ Verification failed: {e}")
    print("   But indexing process completed - data may still be available")
