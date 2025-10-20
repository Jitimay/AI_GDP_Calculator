from elasticsearch import Elasticsearch
from datetime import datetime
import json

class SimpleElasticsearchClient:
    def __init__(self):
        # Connect to local Elasticsearch (updated syntax)
        try:
            self.es = Elasticsearch(
                hosts=['http://localhost:9202'],  # Using port 9202 where ES container is running
                verify_certs=False,
                ssl_show_warn=False,
                request_timeout=5
            )
            self.gdp_index = 'gdp-data'
            self.es_available = self._test_connection()
            if self.es_available:
                self.setup_index()
            else:
                print("⚠️  Elasticsearch not available - using fallback mode")
        except Exception as e:
            print(f"⚠️  Elasticsearch connection failed: {e}")
            self.es_available = False
    
    def _test_connection(self):
        """Test if Elasticsearch is available"""
        try:
            # Quick timeout test
            info = self.es.info(request_timeout=2)
            return True
        except Exception as e:
            print(f"   ES connection test failed: {e}")
            return False
    
    def setup_index(self):
        """Create index if it doesn't exist"""
        if not self.es_available:
            return
            
        try:
            if not self.es.indices.exists(index=self.gdp_index):
                mapping = {
                    "mappings": {
                        "properties": {
                            "timestamp": {"type": "date"},
                            "province": {"type": "keyword"},
                            "gdp_index": {"type": "float"},
                            "composite_index": {"type": "float"},
                            "indicators": {
                                "properties": {
                                    "mobile_money": {"type": "float"},
                                    "electricity": {"type": "float"},
                                    "internet": {"type": "float"},
                                    "satellite": {"type": "float"},
                                    "social_media": {"type": "float"}
                                }
                            }
                        }
                    }
                }
                self.es.indices.create(index=self.gdp_index, body=mapping)
                print(f"✅ Created Elasticsearch index: {self.gdp_index}")
        except Exception as e:
            print(f"⚠️  Could not create Elasticsearch index: {e}")
            self.es_available = False
    
    def save_gdp_data(self, provincial_results, national_index):
        """Save GDP data to Elasticsearch (replaces SQLite)"""
        if not self.es_available:
            print("⚠️  Elasticsearch not available - skipping save")
            return
            
        try:
            timestamp = datetime.now()
            
            # Save national data
            national_doc = {
                "timestamp": timestamp,
                "province": "NATIONAL",
                "gdp_index": national_index,
                "composite_index": national_index,
                "data_type": "national"
            }
            self.es.index(index=self.gdp_index, body=national_doc)
            
            # Save provincial data
            for province, data in provincial_results.items():
                doc = {
                    "timestamp": timestamp,
                    "province": province,
                    "gdp_index": data.get('ml_prediction', data['composite_index']),
                    "composite_index": data['composite_index'],
                    "indicators": data['indicators'],
                    "data_type": "provincial"
                }
                self.es.index(index=self.gdp_index, body=doc)
            
            print(f"✅ Saved GDP data to Elasticsearch at {timestamp}")
        except Exception as e:
            print(f"⚠️  Failed to save to Elasticsearch: {e}")
    
    def get_recent_data(self, hours=24):
        """Get recent GDP data (replaces SQLite queries)"""
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"range": {"timestamp": {"gte": f"now-{hours}h"}}},
                        {"term": {"data_type": "provincial"}}
                    ]
                }
            },
            "sort": [{"timestamp": {"order": "desc"}}],
            "size": 1000
        }
        
        result = self.es.search(index=self.gdp_index, body=query)
        return [hit['_source'] for hit in result['hits']['hits']]
    
    def get_province_trends(self, province, hours=24):
        """Get trends for specific province"""
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"range": {"timestamp": {"gte": f"now-{hours}h"}}},
                        {"term": {"province": province}}
                    ]
                }
            },
            "aggs": {
                "gdp_over_time": {
                    "date_histogram": {
                        "field": "timestamp",
                        "fixed_interval": "1h"
                    },
                    "aggs": {
                        "avg_gdp": {"avg": {"field": "gdp_index"}}
                    }
                }
            }
        }
        
        return self.es.search(index=self.gdp_index, body=query)
    
    def get_alerts(self, threshold=80):
        """Get provinces with high GDP activity"""
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"range": {"timestamp": {"gte": "now-1h"}}},
                        {"range": {"gdp_index": {"gte": threshold}}},
                        {"term": {"data_type": "provincial"}}
                    ]
                }
            },
            "aggs": {
                "alert_provinces": {
                    "terms": {"field": "province"},
                    "aggs": {
                        "max_gdp": {"max": {"field": "gdp_index"}},
                        "latest": {
                            "top_hits": {
                                "sort": [{"timestamp": {"order": "desc"}}],
                                "size": 1
                            }
                        }
                    }
                }
            }
        }
        
        return self.es.search(index=self.gdp_index, body=query)
    
    def health_check(self):
        """Check if Elasticsearch is running"""
        try:
            info = self.es.info()
            return {"status": "healthy", "version": info['version']['number']}
        except Exception as e:
            return {"status": "error", "message": str(e)}