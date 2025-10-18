import json
import numpy as np
from datetime import datetime
from data_ingestion import DataIngestion
from satellite_module import SatelliteAnalyzer
from social_media_module import SocialMediaAnalyzer
from ml_model import GDPPredictor

class FusionEngine:
    def __init__(self, config_path='config.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.data_ingestion = DataIngestion()
        self.satellite_analyzer = SatelliteAnalyzer()
        self.social_analyzer = SocialMediaAnalyzer()
        self.gdp_predictor = GDPPredictor()
        
    def calculate_composite_index(self, province_data):
        """Calculate composite GDP index using weighted fusion"""
        weights = self.config['weights']
        
        # Normalize all indicators to 0-100 scale
        indicators = {
            'mobile_money': min(100, max(0, province_data.get('mobile_money', 0) / 20)),
            'electricity': min(100, max(0, province_data.get('electricity', 0) / 10)),
            'internet': min(100, max(0, province_data.get('internet', 0) / 5)),
            'satellite': province_data.get('satellite_score', 50),
            'social_media': province_data.get('social_score', 0)
        }
        
        # Calculate weighted average
        composite_score = sum(indicators[key] * weights[key] for key in weights.keys())
        
        return {
            'composite_index': composite_score,
            'indicators': indicators,
            'timestamp': datetime.now()
        }
    
    def process_realtime_data(self):
        """Process all data sources and generate real-time GDP estimates"""
        # Get real-time data from all sources
        realtime_data = self.data_ingestion.simulate_realtime_data()
        satellite_data = self.satellite_analyzer.analyze_market_activity()
        social_data = self.social_analyzer.analyze_social_signals()
        
        results = {}
        
        for province in self.data_ingestion.provinces:
            # Combine all data sources
            province_data = realtime_data['data'][province].copy()
            
            # Add satellite data
            sat_info = next((s for s in satellite_data.values() if isinstance(s, dict) and s.get('province') == province), {})
            province_data['satellite_score'] = sat_info.get('market_density_score', 50)
            
            # Add social media data
            social_info = next((s for s in social_data if s['province'] == province), {})
            province_data['social_score'] = social_info.get('commercial_score', 0)
            
            # Calculate composite index
            composite_result = self.calculate_composite_index(province_data)
            
            # Get ML prediction if model is available
            try:
                ml_features = {
                    'mobile_money_volume_normalized': composite_result['indicators']['mobile_money'],
                    'mobile_money_count_normalized': composite_result['indicators']['mobile_money'] * 0.8,
                    'electricity_normalized': composite_result['indicators']['electricity'],
                    'internet_normalized': composite_result['indicators']['internet'],
                    'social_score_normalized': composite_result['indicators']['social_media']
                }
                ml_prediction = self.gdp_predictor.predict(ml_features)
                composite_result['ml_prediction'] = float(ml_prediction)
            except:
                composite_result['ml_prediction'] = composite_result['composite_index']
            
            results[province] = composite_result
        
        return results
    
    def calculate_national_index(self, provincial_results):
        """Calculate national GDP index from provincial results"""
        # Population-weighted average (simplified weights)
        province_weights = {
            'Bujumbura': 0.3,
            'Gitega': 0.2,
            'Ngozi': 0.15,
            'Kayanza': 0.15,
            'Bururi': 0.1,
            'Cibitoke': 0.1
        }
        
        national_index = 0
        for province, weight in province_weights.items():
            if province in provincial_results:
                national_index += provincial_results[province]['composite_index'] * weight
        
        return national_index
    
    def detect_alerts(self, provincial_results):
        """Detect provinces with significant activity spikes"""
        alerts = []
        threshold = self.config['alert_threshold']
        
        for province, data in provincial_results.items():
            if data['composite_index'] >= threshold:
                alerts.append({
                    'province': province,
                    'index_value': data['composite_index'],
                    'alert_type': 'high_activity',
                    'timestamp': datetime.now()
                })
        
        return alerts
