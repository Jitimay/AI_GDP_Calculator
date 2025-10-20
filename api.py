from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from fusion_engine import FusionEngine
from data_ingestion import DataIngestion
from data_preprocessing import DataPreprocessor
from ml_model import GDPPredictor
app = Flask(__name__)
CORS(app)

# Initialize components
fusion_engine = FusionEngine()
data_ingestion = DataIngestion()
preprocessor = DataPreprocessor()
gdp_predictor = GDPPredictor()

# Initialize Elasticsearch client (REQUIRED for hackathon)
from es_client import SimpleElasticsearchClient
es_client = SimpleElasticsearchClient()
if not es_client.es_available:
    raise Exception("❌ Elasticsearch is REQUIRED for this hackathon project!")
print("✅ Elasticsearch client initialized - HACKATHON READY")

@app.route('/predict', methods=['GET'])
def predict():
    """Get current GDP predictions for all provinces - ELASTICSEARCH POWERED"""
    try:
        # Process real-time data
        provincial_results = fusion_engine.process_realtime_data()
        
        # Calculate national index
        national_index = fusion_engine.calculate_national_index(provincial_results)
        
        # Save to Elasticsearch (PRIMARY STORAGE)
        es_client.save_gdp_data(provincial_results, national_index)
        
        response = {
            'timestamp': datetime.now().isoformat(),
            'national_index': national_index,
            'provincial_data': provincial_results,
            'status': 'success',
            'data_source': 'elasticsearch'
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/dashboard-data', methods=['GET'])
def dashboard_data():
    """Get comprehensive dashboard data - ELASTICSEARCH POWERED"""
    try:
        # Get current predictions
        provincial_results = fusion_engine.process_realtime_data()
        national_index = fusion_engine.calculate_national_index(provincial_results)
        
        # Get alerts using real-time data
        alerts = []
        for province, data in provincial_results.items():
            gdp_val = data.get('composite_index', 0)
            if gdp_val > 50:  # Lower threshold to show alerts
                alerts.append({
                    'province': province,
                    'gdp_index': gdp_val,
                    'message': f"{province} showing high activity: {gdp_val:.1f}%"
                })
        
        # Simple historical data structure
        history_by_province = {}
        for province in provincial_results.keys():
            history_by_province[province] = [
                {"timestamp": datetime.now().isoformat(), "value": provincial_results[province]['composite_index']}
            ]
        
        response = {
            'timestamp': datetime.now().isoformat(),
            'current': {
                'national_index': national_index,
                'provincial_data': provincial_results
            },
            'historical': history_by_province,
            'alerts': alerts,
            'status': 'success',
            'data_source': 'elasticsearch'
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500
        
        # Format historical data
        history_by_province = {}
        for record in historical_data:
            province = record['province']
            if province not in history_by_province:
                history_by_province[province] = []
            history_by_province[province].append({
                'timestamp': record['timestamp'],
                'value': record['gdp_index']
            })
        
        # Get alerts using real-time data instead of ES
        alerts = []
        for province, data in provincial_results.items():
            gdp_val = data.get('composite_index', 0)
            if gdp_val > 70:  # Alert threshold
                alerts.append({
                    'province': province,
                    'gdp_index': gdp_val,
                    'message': f"{province} showing high activity: {gdp_val:.1f}%"
                })
        
        response = {
            'timestamp': datetime.now().isoformat(),
            'current': {
                'national_index': national_index,
                'provincial_data': provincial_results
            },
            'historical': history_by_province,
            'alerts': alerts,
            'status': 'success'
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/elasticsearch/health', methods=['GET'])
def elasticsearch_health():
    """Check Elasticsearch cluster health - HACKATHON REQUIREMENT"""
    health = es_client.health_check()
    return jsonify({
        'elasticsearch': health,
        'hackathon_compliance': 'ELASTICSEARCH_REQUIRED'
    })

@app.route('/elasticsearch/search/<province>', methods=['GET'])
def search_province_data(province):
    """Search province data using Elasticsearch - HACKATHON FEATURE"""
    hours = request.args.get('hours', 24, type=int)
    data = es_client.get_province_trends(province, hours)
    return jsonify({
        'province': province,
        'data': data,
        'powered_by': 'elasticsearch'
    })

@app.route('/elasticsearch/analytics', methods=['GET'])
def elasticsearch_analytics():
    """Advanced analytics using Elasticsearch aggregations"""
    recent_data = es_client.get_recent_data(hours=24)
    return jsonify({
        'total_records': len(recent_data),
        'data': recent_data[:10],  # Latest 10 records
        'analytics_engine': 'elasticsearch'
    })
    """Get current alerts"""
    try:
        provincial_results = fusion_engine.process_realtime_data()
        alerts = fusion_engine.detect_alerts(provincial_results)
        
        return jsonify({
            'alerts': alerts,
            'count': len(alerts),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/train-model', methods=['POST'])
def train_model():
    """Train the ML model with current data"""
    try:
        # Load and preprocess data
        data_dict = data_ingestion.load_data()
        processed_df = preprocessor.preprocess_data(data_dict)
        processed_df = preprocessor.create_target_variable(processed_df)
        
        # Train model
        training_results = gdp_predictor.train_model(processed_df)
        
        return jsonify({
            'status': 'success',
            'training_results': training_results,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    es_health = {"status": "not_available"}
    if es_client:
        es_health = es_client.health_check()
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'elasticsearch': es_health
    })

@app.route('/search/trends/<province>')
def search_province_trends(province):
    """Search province trends using Elasticsearch"""
    if not es_client:
        return jsonify({'error': 'Elasticsearch not available', 'status': 'error'}), 503
    
    hours = request.args.get('hours', 24, type=int)
    try:
        results = es_client.get_province_trends(province, hours)
        return jsonify({
            'province': province,
            'trends': results['aggregations']['gdp_over_time']['buckets'],
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/search/recent')
def search_recent_data():
    """Get recent data using Elasticsearch"""
    if not es_client:
        return jsonify({'error': 'Elasticsearch not available', 'status': 'error'}), 503
    
    hours = request.args.get('hours', 24, type=int)
    try:
        data = es_client.get_recent_data(hours)
        return jsonify({
            'data': data,
            'count': len(data),
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
