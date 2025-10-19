from elasticsearch import Elasticsearch
from datetime import datetime

class SocialMediaElasticsearch:
    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        self.social_index = 'social-commerce'
        
    def index_social_posts(self, posts):
        """Index social media posts for commerce analysis"""
        for post in posts:
            doc = {
                'timestamp': datetime.now(),
                'province': post['province'],
                'text': post['content'],
                'commercial_score': self._calculate_score(post['content']),
                'keywords_found': self._extract_keywords(post['content'])
            }
            
            self.es.index(index=self.social_index, body=doc)
    
    def search_commerce_activity(self, province, hours=24):
        """Search for commercial activity patterns"""
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"range": {"timestamp": {"gte": f"now-{hours}h"}}},
                        {"term": {"province.keyword": province}},
                        {"range": {"commercial_score": {"gte": 0.5}}}
                    ]
                }
            },
            "aggs": {
                "commerce_trend": {
                    "date_histogram": {
                        "field": "timestamp",
                        "interval": "1h"
                    },
                    "aggs": {
                        "avg_score": {"avg": {"field": "commercial_score"}}
                    }
                }
            }
        }
        
        return self.es.search(index=self.social_index, body=query)
    
    def _calculate_score(self, text):
        # Simplified scoring logic
        keywords = ['sell', 'buy', 'market', 'shop', 'business']
        return sum(1 for word in keywords if word in text.lower()) / len(keywords)
