#!/usr/bin/env python3
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json
from datetime import datetime

print("🚀 Loading ALL MASSIVE datasets into Elasticsearch")
print("📊 Total data: ~25MB across 4 datasets")
print("=" * 60)

# Connect to Elasticsearch
es = Elasticsearch(['http://localhost:9202'], request_timeout=300)

# Create comprehensive index
mapping = {
    "mappings": {
        "properties": {
            "timestamp": {"type": "date"},
            "province": {"type": "keyword"},
            "district": {"type": "keyword"},
            "data_type": {"type": "keyword"},
            "mobile_volume": {"type": "float"},
            "mobile_count": {"type": "integer"},
            "electricity_kwh": {"type": "float"},
            "internet_gb": {"type": "float"},
            "social_score": {"type": "float"},
            "gdp_index": {"type": "float"},
            "composite_index": {"type": "float"}
        }
    }
}

# Create index
index_name = "massive-gdp-data"
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
es.indices.create(index=index_name, body=mapping)
print(f"✅ Created index: {index_name}")

# Load each massive dataset
datasets = [
    ("mobile_money_massive.csv", "mobile_money"),
    ("electricity_massive.csv", "electricity"), 
    ("internet_massive.csv", "internet"),
    ("social_massive.csv", "social_media")
]

total_records = 0

for filename, data_type in datasets:
    print(f"\n📥 Loading {filename}...")
    
    try:
        df = pd.read_csv(filename)
        print(f"   Records: {len(df):,}")
        
        # Prepare documents for bulk insert
        docs = []
        for _, row in df.iterrows():
            doc = {
                "_index": index_name,
                "_source": {
                    "timestamp": datetime.now().isoformat(),
                    "province": row.get('province', 'Unknown'),
                    "district": row.get('district', 'Unknown'),
                    "data_type": data_type,
                    **{col: row[col] for col in df.columns if col not in ['province', 'district']}
                }
            }
            docs.append(doc)
            
            # Bulk insert in batches of 1000
            if len(docs) >= 1000:
                bulk(es, docs)
                docs = []
        
        # Insert remaining docs
        if docs:
            bulk(es, docs)
            
        total_records += len(df)
        print(f"   ✅ Loaded {len(df):,} records")
        
    except Exception as e:
        print(f"   ❌ Error loading {filename}: {e}")

print(f"\n🎯 HACKATHON READY!")
print(f"📊 Total records loaded: {total_records:,}")
print(f"🔍 Index: {index_name}")
print(f"⚡ Elasticsearch powered with MASSIVE dataset!")
