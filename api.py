from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta
import json
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

# Initialize database
def init_db():
    conn = sqlite3.connect('gdp_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gdp_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            province TEXT,
            gdp_index REAL,
            composite_index REAL,
            mobile_money REAL,
            electricity REAL,
            internet REAL,
            satellite REAL,
            social_media REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def save_to_db(provincial_results):
    """Save results to database"""
    conn = sqlite3.connect('gdp_data.db')
    cursor = conn.cursor()
    
    timestamp = datetime.now().isoformat()
    
    for province, data in provincial_results.items():
        cursor.execute('''
            INSERT INTO gdp_history 
            (timestamp, province, gdp_index, composite_index, mobile_money, electricity, internet, satellite, social_media)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            timestamp,
            province,
            data.get('ml_prediction', data['composite_index']),
            data['composite_index'],
            data['indicators']['mobile_money'],
            data['indicators']['electricity'],
            data['indicators']['internet'],
            data['indicators']['satellite'],
            data['indicators']['social_media']
        ))
    
    conn.commit()
    conn.close()

@app.route('/predict', methods=['GET'])
def predict():
    """Get current GDP predictions for all provinces"""
    try:
        # Process real-time data
        provincial_results = fusion_engine.process_realtime_data()
        
        # Calculate national index
        national_index = fusion_engine.calculate_national_index(provincial_results)
        
        # Save to database
        save_to_db(provincial_results)
        
        response = {
            'timestamp': datetime.now().isoformat(),
            'national_index': national_index,
            'provincial_data': provincial_results,
            'status': 'success'
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/dashboard-data', methods=['GET'])
def dashboard_data():
    """Get comprehensive dashboard data"""
    try:
        # Get current predictions
        provincial_results = fusion_engine.process_realtime_data()
        national_index = fusion_engine.calculate_national_index(provincial_results)
        
        # Get historical data
        conn = sqlite3.connect('gdp_data.db')
        cursor = conn.cursor()
        
        # Last 24 hours of data
        yesterday = (datetime.now() - timedelta(hours=24)).isoformat()
        cursor.execute('''
            SELECT timestamp, province, gdp_index 
            FROM gdp_history 
            WHERE timestamp > ? 
            ORDER BY timestamp
        ''', (yesterday,))
        
        historical_data = cursor.fetchall()
        conn.close()
        
        # Format historical data
        history_by_province = {}
        for timestamp, province, gdp_index in historical_data:
            if province not in history_by_province:
                history_by_province[province] = []
            history_by_province[province].append({
                'timestamp': timestamp,
                'value': gdp_index
            })
        
        # Get alerts
        alerts = fusion_engine.detect_alerts(provincial_results)
        
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

@app.route('/alerts', methods=['GET'])
def get_alerts():
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
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
