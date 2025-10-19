from es_client import SimpleElasticsearchClient
from datetime import datetime
import json

es = SimpleElasticsearchClient()

# Load 5 sample records quickly
for i in range(5):
    doc = {
        "timestamp": datetime.now(),
        "province": f"Province_{i}",
        "gdp_index": 65 + i * 5,
        "composite_index": 70 + i * 3,
        "indicators": {"mobile_money": 80, "electricity": 70, "internet": 85, "satellite": 75, "social_media": 65}
    }
    es.es.index(index="gdp-data", body=doc)

print("✅ Fast data loaded!")
