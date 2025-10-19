#!/usr/bin/env python3
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import time

print("🏆 HACKATHON: Loading 100K+ records into Elasticsearch")
print("=" * 60)

# Connect to Elasticsearch
es = Elasticsearch(['http://localhost:9202'], request_timeout=60)

# Create optimized index
mapping = {
    "mappings": {
        "properties": {
            "timestamp": {"type": "date"},
            "province": {"type": "keyword"},
            "district": {"type": "keyword"},
            "mobile_volume": {"type": "float"},
            "mobile_count": {"type": "integer"},
            "electricity": {"type": "float"},
            "internet": {"type": "float"},
            "social_media": {"type": "integer"},
            "gdp_composite": {"type": "float"}
        }
    },
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0,
        "refresh_interval": "30s"
    }
}

# Delete and create index
try:
    es.indices.delete(index="gdp-massive")
except:
    pass

es.indices.create(index="gdp-massive", body=mapping)
print("✅ Created optimized Elasticsearch index")

# Load massive datasets
print("📊 Loading massive datasets...")
mobile_df = pd.read_csv('mobile_money_massive.csv')
electricity_df = pd.read_csv('electricity_massive.csv')
internet_df = pd.read_csv('internet_massive.csv')
social_df = pd.read_csv('social_massive.csv')

print(f"   Mobile Money: {len(mobile_df):,} records")
print(f"   Electricity: {len(electricity_df):,} records")
print(f"   Internet: {len(internet_df):,} records")
print(f"   Social Media: {len(social_df):,} records")

# Merge datasets for bulk loading
print("🔄 Merging datasets...")
merged_data = []

for i in range(len(mobile_df)):
    doc = {
        "timestamp": mobile_df.iloc[i]['timestamp'],
        "province": mobile_df.iloc[i]['province'],
        "district": mobile_df.iloc[i]['district'],
        "mobile_volume": mobile_df.iloc[i]['transaction_volume'],
        "mobile_count": mobile_df.iloc[i]['transaction_count'],
        "electricity": electricity_df.iloc[i]['consumption_kwh'],
        "internet": internet_df.iloc[i]['data_usage_gb'],
        "social_media": social_df.iloc[i]['commercial_keywords'],
        "gdp_composite": (
            mobile_df.iloc[i]['transaction_volume'] * 0.3 +
            electricity_df.iloc[i]['consumption_kwh'] * 0.25 +
            internet_df.iloc[i]['data_usage_gb'] * 0.2 +
            social_df.iloc[i]['commercial_keywords'] * 0.25
        ) / 100
    }
    merged_data.append({"_index": "gdp-massive", "_source": doc})

print(f"🚀 Bulk loading {len(merged_data):,} documents...")
start_time = time.time()

# Bulk load in chunks
chunk_size = 1000
for i in range(0, len(merged_data), chunk_size):
    chunk = merged_data[i:i+chunk_size]
    bulk(es, chunk)
    if (i + chunk_size) % 10000 == 0:
        print(f"   Loaded {i + chunk_size:,} documents...")

load_time = time.time() - start_time
print(f"✅ Bulk load complete in {load_time:.1f} seconds")

# Force refresh
es.indices.refresh(index="gdp-massive")

# Verify and show stats
count = es.count(index="gdp-massive")['count']
print(f"📊 ELASTICSEARCH STATS:")
print(f"   Total documents: {count:,}")
print(f"   Load speed: {count/load_time:.0f} docs/second")

# Demo queries
print(f"\n🔍 HACKATHON DEMO QUERIES:")

# Top provinces by GDP
agg_result = es.search(
    index="gdp-massive",
    body={
        "size": 0,
        "aggs": {
            "top_provinces": {
                "terms": {"field": "province", "size": 5},
                "aggs": {"avg_gdp": {"avg": {"field": "gdp_composite"}}}
            }
        }
    }
)

print("   Top 5 Provinces by GDP:")
for bucket in agg_result['aggregations']['top_provinces']['buckets']:
    print(f"     {bucket['key']}: {bucket['avg_gdp']['value']:.2f} (GDP Index)")

# Time-based analysis
time_agg = es.search(
    index="gdp-massive",
    body={
        "size": 0,
        "aggs": {
            "gdp_over_time": {
                "date_histogram": {
                    "field": "timestamp",
                    "calendar_interval": "day"
                },
                "aggs": {"daily_gdp": {"avg": {"field": "gdp_composite"}}}
            }
        }
    }
)

daily_buckets = time_agg['aggregations']['gdp_over_time']['buckets']
print(f"\n   Daily GDP Trend ({len(daily_buckets)} days analyzed)")
print(f"     First day: {daily_buckets[0]['daily_gdp']['value']:.2f}")
print(f"     Last day: {daily_buckets[-1]['daily_gdp']['value']:.2f}")

print(f"\n🎉 HACKATHON SUCCESS!")
print(f"   ✅ {count:,} records in Elasticsearch")
print(f"   ✅ Real-time analytics working")
print(f"   ✅ Fast aggregations and search")
print(f"   ✅ Multi-dimensional GDP analysis")
