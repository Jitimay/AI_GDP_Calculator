#!/usr/bin/env python3
import pandas as pd
from elasticsearch import Elasticsearch
import json
from datetime import datetime

# Connect to Elasticsearch
es = Elasticsearch(['http://localhost:9202'])

# Create index with optimized mapping
mapping = {
    "mappings": {
        "properties": {
            "timestamp": {"type": "date"},
            "province": {"type": "keyword"},
            "gdp_index": {"type": "float"},
            "composite_index": {"type": "float"},
            "mobile_money": {"type": "float"},
            "electricity": {"type": "float"},
            "internet": {"type": "float"},
            "satellite": {"type": "float"},
            "social_media": {"type": "float"}
        }
    }
}

# Delete and recreate index
try:
    es.indices.delete(index="gdp-data")
except:
    pass

es.indices.create(index="gdp-data", body=mapping)

# Load and index data
mobile_df = pd.read_csv('mobile_money.csv')
electricity_df = pd.read_csv('electricity.csv')
internet_df = pd.read_csv('internet_usage.csv')
social_df = pd.read_csv('social_signals.csv')

print("📊 Indexing GDP data to Elasticsearch...")

# Bulk index data
docs = []
for i in range(len(mobile_df)):
    doc = {
        "timestamp": mobile_df.iloc[i]['timestamp'],
        "province": mobile_df.iloc[i]['province'],
        "mobile_money": mobile_df.iloc[i]['transaction_volume'],
        "electricity": electricity_df.iloc[i]['consumption_kwh'],
        "internet": internet_df.iloc[i]['data_usage_gb'],
        "social_media": social_df.iloc[i]['commercial_keywords'],
        "satellite": 50.0,  # Default value
        "composite_index": (
            mobile_df.iloc[i]['transaction_volume'] * 0.3 +
            electricity_df.iloc[i]['consumption_kwh'] * 0.25 +
            internet_df.iloc[i]['data_usage_gb'] * 0.2 +
            50.0 * 0.15 +
            social_df.iloc[i]['commercial_keywords'] * 0.1
        ) / 5
    }
    docs.append({"index": {"_index": "gdp-data"}})
    docs.append(doc)

# Bulk insert
from elasticsearch.helpers import bulk
bulk(es, [{"_index": "gdp-data", "_source": doc} for doc in docs[1::2]])

print(f"✅ Indexed {len(docs)//2} documents")
print(f"🔍 Search test: {es.count(index='gdp-data')['count']} documents in index")
