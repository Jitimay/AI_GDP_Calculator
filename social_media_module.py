import pandas as pd
import numpy as np
from datetime import datetime
import re

class SocialMediaAnalyzer:
    def __init__(self):
        self.commercial_keywords = {
            'selling': ['sell', 'selling', 'sale', 'vendre', 'gucuruza'],
            'buying': ['buy', 'buying', 'purchase', 'acheter', 'kugura'],
            'market': ['market', 'marché', 'isoko', 'shop', 'store', 'magasin']
        }
        self.provinces = ['Bujumbura', 'Gitega', 'Ngozi', 'Kayanza', 'Bururi', 'Cibitoke']
    
    def analyze_social_signals(self, text_data=None):
        """Analyze social media text for commercial activity indicators"""
        if text_data is None:
            return self._simulate_social_analysis()
        
        return self._process_real_text(text_data)
    
    def _simulate_social_analysis(self):
        """Simulate social media analysis for all provinces"""
        results = []
        
        for province in self.provinces:
            # Simulate different social media activity by province
            base_activity = {
                'Bujumbura': 80,
                'Gitega': 60,
                'Ngozi': 55,
                'Kayanza': 45,
                'Bururi': 40,
                'Cibitoke': 35
            }
            
            activity_level = base_activity.get(province, 50)
            
            selling_mentions = max(0, int(np.random.poisson(activity_level * 0.3)))
            buying_mentions = max(0, int(np.random.poisson(activity_level * 0.25)))
            market_mentions = max(0, int(np.random.poisson(activity_level * 0.2)))
            
            commercial_score = (selling_mentions * 1.2 + buying_mentions * 1.0 + market_mentions * 1.5)
            
            results.append({
                'province': province,
                'selling_mentions': selling_mentions,
                'buying_mentions': buying_mentions,
                'market_mentions': market_mentions,
                'commercial_score': min(100, commercial_score),
                'timestamp': datetime.now()
            })
        
        return results
    
    def _process_real_text(self, text_data):
        """Process actual text data for commercial keywords"""
        results = {}
        
        for category, keywords in self.commercial_keywords.items():
            count = 0
            for keyword in keywords:
                count += len(re.findall(r'\b' + keyword + r'\b', text_data.lower()))
            results[f'{category}_mentions'] = count
        
        results['commercial_score'] = (
            results['selling_mentions'] * 1.2 + 
            results['buying_mentions'] * 1.0 + 
            results['market_mentions'] * 1.5
        )
        
        return results
    
    def get_trending_commercial_terms(self):
        """Simulate trending commercial terms analysis"""
        trending_terms = [
            'mobile money', 'digital payment', 'online shop', 'delivery',
            'wholesale', 'retail', 'marketplace', 'e-commerce'
        ]
        
        return {
            'trending_terms': np.random.choice(trending_terms, 3, replace=False).tolist(),
            'growth_rate': np.random.uniform(5, 25),
            'timestamp': datetime.now()
        }
