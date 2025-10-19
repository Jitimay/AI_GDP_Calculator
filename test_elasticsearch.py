#!/usr/bin/env python3
import requests
import json
from elasticsearch import Elasticsearch

def test_elasticsearch():
    """Test Elasticsearch integration"""
    print("🔍 Testing Elasticsearch Integration")
    print("=" * 40)
    
    # 1. Test Elasticsearch connection
    try:
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        if es.ping():
            print("✅ Elasticsearch connected")
        else:
            print("❌ Elasticsearch not accessible")
            return
    except Exception as e:
        print(f"❌ Elasticsearch error: {e}")
        return
    
    # 2. Test index creation
    try:
        es.indices.create(index='test-gdp', ignore=400)
        print("✅ Index creation successful")
    except Exception as e:
        print(f"❌ Index creation failed: {e}")
    
    # 3. Test document indexing
    try:
        doc = {
            'province': 'Bujumbura',
            'gdp_index': 75.5,
            'timestamp': '2024-01-01T12:00:00'
        }
        es.index(index='test-gdp', body=doc)
        print("✅ Document indexing successful")
    except Exception as e:
        print(f"❌ Document indexing failed: {e}")
    
    # 4. Test search
    try:
        result = es.search(index='test-gdp', body={'query': {'match_all': {}}})
        print(f"✅ Search successful - {result['hits']['total']['value']} docs")
    except Exception as e:
        print(f"❌ Search failed: {e}")
    
    # Cleanup
    es.indices.delete(index='test-gdp', ignore=404)

if __name__ == "__main__":
    test_elasticsearch()
