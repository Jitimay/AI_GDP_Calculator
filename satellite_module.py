import numpy as np
from datetime import datetime

class SatelliteAnalyzer:
    def __init__(self):
        self.provinces = ['Bujumbura', 'Gitega', 'Ngozi', 'Kayanza', 'Bururi', 'Cibitoke']
    
    def analyze_market_activity(self, province=None):
        """Simulate satellite analysis of market density and activity"""
        if province:
            return self._simulate_market_analysis(province)
        
        results = {}
        for prov in self.provinces:
            results[prov] = self._simulate_market_analysis(prov)
        
        return results
    
    def _simulate_market_analysis(self, province):
        """Simulate image analysis returning market activity score"""
        # Simulate different market activity levels by province
        base_activity = {
            'Bujumbura': 75,  # Capital, highest activity
            'Gitega': 60,     # Political capital
            'Ngozi': 55,      # Commercial hub
            'Kayanza': 50,    # Agricultural region
            'Bururi': 45,     # Rural area
            'Cibitoke': 40    # Border region
        }
        
        # Add random variation
        activity_score = base_activity.get(province, 50) + np.random.normal(0, 10)
        activity_score = max(0, min(100, activity_score))
        
        return {
            'province': province,
            'market_density_score': activity_score,
            'vehicle_count_estimate': int(activity_score * 2 + np.random.normal(0, 5)),
            'crowd_density_score': activity_score * 0.8 + np.random.normal(0, 8),
            'timestamp': datetime.now()
        }
    
    def generate_synthetic_image_data(self):
        """Generate synthetic satellite-like data for all provinces"""
        results = []
        for province in self.provinces:
            analysis = self._simulate_market_analysis(province)
            results.append(analysis)
        
        return results
