from elasticsearch import Elasticsearch
from datetime import datetime
import json

class ElasticsearchClient:
    def __init__(self, host='localhost', port=9200):
        self.es = Elasticsearch([{'host': host, 'port': port}])
        self.gdp_index = 'gdp-data'
        self.alerts_index = 'gdp-alerts'
        
    def index_gdp_data(self, provincial_results):
        """Index GDP data for real-time search"""
        timestamp = datetime.now()
        
        for province, data in provincial_results.items():
            doc = {
                'timestamp': timestamp,
                'province': province,
                'gdp_index': data.get('ml_prediction', data['composite_index']),
                'composite_index': data['composite_index'],
                'indicators': data['indicators']
            }
            
            self.es.index(
                index=self.gdp_index,
                body=doc
            )
    
    def search_gdp_trends(self, province=None, hours=24):
        """Search GDP trends with aggregations"""
        query = {
            "query": {
                "range": {
                    "timestamp": {
                        "gte": f"now-{hours}h"
                    }
                }
            },
            "aggs": {
                "provinces": {
                    "terms": {"field": "province.keyword"},
                    "aggs": {
                        "avg_gdp": {"avg": {"field": "gdp_index"}},
                        "trend": {
                            "date_histogram": {
                                "field": "timestamp",
                                "interval": "1h"
                            },
                            "aggs": {
                                "gdp_avg": {"avg": {"field": "gdp_index"}}
                            }
                        }
                    }
                }
            }
        }
        
        if province:
            query["query"] = {
                "bool": {
                    "must": [
                        {"range": {"timestamp": {"gte": f"now-{hours}h"}}},
                        {"term": {"province.keyword": province}}
                    ]
                }
            }
        
        return self.es.search(index=self.gdp_index, body=query)
