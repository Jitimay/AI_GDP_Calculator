#!/usr/bin/env python3
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json

print("🚀 Loading MASSIVE dataset into Elasticsearch")
print("=" * 50)

# Connect to Elasticsearch
es = Elasticsearch(['http://localhost:9202'], request_timeout=120)

# Create index
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
            "social_keywords": {"type": "integer"},
            "gdp_composite": {"type": "float"}
        }
    }
}

# Delete and create index
try:
    es.indices.delete(index="gdp-massive")
except:
    pass

es.indices.create(index="gdp-massive", body=mapping)
print("✅ Created Elasticsearch index")

# Load massive datasets
print("📊 Loading massive CSV files...")
mobile_df = pd.read_csv('mobile_money_massive.csv')
electricity_df = pd.read_csv('electricity_massive.csv')
internet_df = pd.read_csv('internet_massive.csv')
social_df = pd.read_csv('social_massive.csv')

print(f"   Mobile: {len(mobile_df):,} records")
print(f"   Electricity: {len(electricity_df):,} records")
print(f"   Internet: {len(internet_df):,} records")
print(f"   Social: {len(social_df):,} records")

# Prepare documents for bulk indexing - FULL DATASET
print("🔄 Preparing ALL documents for Elasticsearch...")
docs = []

# Use ALL records from massive dataset
for i in range(len(mobile_df)):
    # Calculate composite GDP
    gdp_composite = (
        mobile_df.iloc[i]['transaction_volume'] * 0.3 +
        electricity_df.iloc[i]['consumption_kwh'] * 0.25 +
        internet_df.iloc[i]['data_usage_gb'] * 0.2 +
        social_df.iloc[i]['commercial_keywords'] * 0.25
    ) / 100
    
    doc = {
        "_index": "gdp-massive",
        "_source": {
            "timestamp": mobile_df.iloc[i]['timestamp'],
            "province": mobile_df.iloc[i]['province'],
            "district": mobile_df.iloc[i]['district'],
            "mobile_volume": mobile_df.iloc[i]['transaction_volume'],
            "mobile_count": mobile_df.iloc[i]['transaction_count'],
            "electricity": electricity_df.iloc[i]['consumption_kwh'],
            "internet": internet_df.iloc[i]['data_usage_gb'],
            "social_keywords": social_df.iloc[i]['commercial_keywords'],
            "gdp_composite": gdp_composite
        }
    }
    docs.append(doc)

print(f"🚀 Bulk indexing {len(docs):,} documents...")

# Bulk index in larger chunks for speed
chunk_size = 2000
for i in range(0, len(docs), chunk_size):
    chunk = docs[i:i+chunk_size]
    try:
        bulk(es, chunk)
        print(f"   Indexed {min(i+chunk_size, len(docs)):,}/{len(docs):,} documents")
    except Exception as e:
        print(f"   Error indexing chunk {i}: {e}")

# Refresh index
es.indices.refresh(index="gdp-massive")

# Verify
count = es.count(index="gdp-massive")['count']
print(f"\n✅ SUCCESS! {count:,} documents indexed in Elasticsearch")

# Demo query
print("\n🔍 Demo Query - Top GDP Provinces:")
result = es.search(
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

for bucket in result['aggregations']['top_provinces']['buckets']:
    print(f"   {bucket['key']}: {bucket['avg_gdp']['value']:.2f} GDP")

print(f"\n🎉 Elasticsearch is now powering your GDP calculator!")
print(f"   📊 {count:,} economic records indexed")
print(f"   ⚡ Ready for real-time analytics")
print(f"   🏆 Perfect for hackathon demo!")
