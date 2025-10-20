import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

class DataIngestion:
    def __init__(self):
        self.provinces = ['Bujumbura', 'Gitega', 'Ngozi', 'Kayanza', 'Bururi', 'Cibitoke']
        self.data_dir = 'data'  # Relative to project root
    
    def generate_sample_data(self):
        """Generate sample datasets if they don't exist"""
        if not os.path.exists(f'{self.data_dir}/mobile_money.csv'):
            self._create_mobile_money_data()
        if not os.path.exists(f'{self.data_dir}/electricity.csv'):
            self._create_electricity_data()
        if not os.path.exists(f'{self.data_dir}/internet_usage.csv'):
            self._create_internet_data()
        if not os.path.exists(f'{self.data_dir}/social_signals.csv'):
            self._create_social_data()
    
    def _create_mobile_money_data(self):
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        data = []
        for date in dates:
            for province in self.provinces:
                volume = np.random.normal(1000, 200) + np.sin(date.dayofyear/365 * 2 * np.pi) * 100
                data.append({
                    'timestamp': date,
                    'province': province,
                    'transaction_volume': max(0, volume),
                    'transaction_count': np.random.poisson(50)
                })
        pd.DataFrame(data).to_csv('mobile_money.csv', index=False)
    
    def _create_electricity_data(self):
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        data = []
        for date in dates:
            for province in self.provinces:
                consumption = np.random.normal(500, 100) + np.sin(date.dayofyear/365 * 2 * np.pi) * 50
                data.append({
                    'timestamp': date,
                    'province': province,
                    'consumption_kwh': max(0, consumption)
                })
        pd.DataFrame(data).to_csv('electricity.csv', index=False)
    
    def _create_internet_data(self):
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        data = []
        for date in dates:
            for province in self.provinces:
                usage = np.random.normal(200, 50) + np.sin(date.dayofyear/365 * 2 * np.pi) * 30
                data.append({
                    'timestamp': date,
                    'province': province,
                    'data_usage_gb': max(0, usage)
                })
        pd.DataFrame(data).to_csv('internet_usage.csv', index=False)
    
    def _create_social_data(self):
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        data = []
        for date in dates:
            for province in self.provinces:
                selling_mentions = np.random.poisson(20)
                buying_mentions = np.random.poisson(15)
                market_mentions = np.random.poisson(10)
                data.append({
                    'timestamp': date,
                    'province': province,
                    'selling_mentions': selling_mentions,
                    'buying_mentions': buying_mentions,
                    'market_mentions': market_mentions
                })
        pd.DataFrame(data).to_csv('social_signals.csv', index=False)
    
    def load_data(self):
        """Load all data sources - prioritize massive data if available"""
        # Check for massive data files first
        massive_files = {
            'mobile_money': f'{self.data_dir}/mobile_money_massive.csv',
            'electricity': f'{self.data_dir}/electricity_massive.csv',
            'internet': f'{self.data_dir}/internet_massive.csv',
            'social': f'{self.data_dir}/social_massive.csv'
        }
        
        regular_files = {
            'mobile_money': f'{self.data_dir}/mobile_money.csv',
            'electricity': f'{self.data_dir}/electricity.csv',
            'internet': f'{self.data_dir}/internet_usage.csv',
            'social': f'{self.data_dir}/social_signals.csv'
        }
        
        data = {}
        
        for key in massive_files:
            if os.path.exists(massive_files[key]):
                print(f"📊 Loading MASSIVE {key} data...")
                df = pd.read_csv(massive_files[key])
                data[key] = df.tail(1000)  # Use last 1000 records for performance
            elif os.path.exists(regular_files[key]):
                print(f"📊 Loading regular {key} data...")
                data[key] = pd.read_csv(regular_files[key])
            else:
                print(f"⚠️ No data file found for {key}, generating sample...")
                self.generate_sample_data()
                if os.path.exists(regular_files[key]):
                    data[key] = pd.read_csv(regular_files[key])
        
        return data
    
    def simulate_realtime_data(self):
        """Generate new data point for current timestamp"""
        current_time = datetime.now()
        data = {}
        
        for province in self.provinces:
            data[province] = {
                'mobile_money': max(0, np.random.normal(1000, 200)),
                'electricity': max(0, np.random.normal(500, 100)),
                'internet': max(0, np.random.normal(200, 50)),
                'social_score': np.random.poisson(45)
            }
        
        return {'timestamp': current_time, 'data': data}
