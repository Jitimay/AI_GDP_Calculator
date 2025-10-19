from flask import Flask, jsonify, request
from elasticsearch_client import ElasticsearchClient
from fusion_engine import FusionEngine

app = Flask(__name__)
es_client = ElasticsearchClient()
fusion_engine = FusionEngine()

@app.route('/predict', methods=['GET'])
def predict():
    """Get predictions and index to Elasticsearch"""
    provincial_results = fusion_engine.process_realtime_data()
    national_index = fusion_engine.calculate_national_index(provincial_results)
    
    # Index to Elasticsearch instead of SQLite
    es_client.index_gdp_data(provincial_results)
    
    return jsonify({
        'national_index': national_index,
        'provincial_data': provincial_results
    })

@app.route('/search/trends/<province>')
def search_trends(province):
    """Search GDP trends using Elasticsearch"""
    hours = request.args.get('hours', 24, type=int)
    results = es_client.search_gdp_trends(province, hours)
    
    return jsonify(results)

@app.route('/analytics/anomalies')
def detect_anomalies():
    """Use Elasticsearch ML for anomaly detection"""
    query = {
        "query": {"range": {"timestamp": {"gte": "now-7d"}}},
        "aggs": {
            "gdp_anomalies": {
                "percentiles": {"field": "gdp_index", "percents": [95, 99]}
            }
        }
    }
    
    results = es_client.es.search(index=es_client.gdp_index, body=query)
    return jsonify(results)
