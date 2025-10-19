#!/usr/bin/env python3
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fusion_engine import FusionEngine
from ml_model import GDPPredictor
from data_ingestion import DataIngestion

class TestGDPCalculator(unittest.TestCase):
    
    def setUp(self):
        self.fusion_engine = FusionEngine()
        self.gdp_predictor = GDPPredictor()
        self.data_ingestion = DataIngestion()
    
    def test_fusion_engine(self):
        """Test fusion engine calculations"""
        test_data = {
            'mobile_money': 100,
            'electricity': 50,
            'internet': 75,
            'satellite_score': 60,
            'social_score': 40
        }
        
        result = self.fusion_engine.calculate_composite_index(test_data)
        
        self.assertIn('composite_index', result)
        self.assertIn('indicators', result)
        self.assertGreaterEqual(result['composite_index'], 0)
        self.assertLessEqual(result['composite_index'], 100)
    
    def test_ml_model_features(self):
        """Test ML model feature requirements"""
        required_features = [
            'mobile_money_volume_normalized',
            'mobile_money_count_normalized', 
            'electricity_normalized',
            'internet_normalized',
            'social_score_normalized'
        ]
        
        self.assertEqual(self.gdp_predictor.feature_columns, required_features)
    
    def test_data_ingestion(self):
        """Test data ingestion provinces"""
        expected_provinces = ['Bujumbura', 'Gitega', 'Ngozi', 'Kayanza', 'Bururi', 'Cibitoke']
        self.assertEqual(self.data_ingestion.provinces, expected_provinces)
    
    def test_realtime_processing(self):
        """Test real-time data processing"""
        results = self.fusion_engine.process_realtime_data()
        
        self.assertIsInstance(results, dict)
        self.assertGreater(len(results), 0)
        
        for province, data in results.items():
            self.assertIn('composite_index', data)
            self.assertIn('indicators', data)

if __name__ == '__main__':
    unittest.main()
