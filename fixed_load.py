from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import time

es = Elasticsearch(['http://localhost:9202'])

# Smaller batches, longer timeouts
docs = []
for i in range(1000):  # Just 1K records for demo
    doc = {
        "_index": "demo-gdp",
        "_source": {
            "province": f"Province_{i%5}",
            "gdp_index": 65 + (i % 30),
            "timestamp": "2024-01-20T10:00:00"
        }
    }
    docs.append(doc)
    
    if len(docs) >= 50:  # Tiny batches
        try:
            bulk(es, docs, timeout=30)
            print(f"✅ Loaded {i}")
            docs = []
            time.sleep(0.1)  # Give ES a break
        except:
            docs = []

print("✅ Demo data loaded successfully!")
