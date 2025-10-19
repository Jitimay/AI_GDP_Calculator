#!/usr/bin/env python3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

class MassDataGenerator:
    def __init__(self):
        # Expand to more provinces and districts for millions of records
        self.provinces = ['Bujumbura', 'Gitega', 'Ngozi', 'Kayanza', 'Bururi', 'Cibitoke', 
                         'Bubanza', 'Karusi', 'Kirundo', 'Makamba', 'Muramvya', 'Muyinga',
                         'Mwaro', 'Rutana', 'Ruyigi', 'Cankuzo', 'Rumonge', 'Bujumbura_Rural']
        
        # Add districts for each province (3-5 per province = ~70 locations)
        self.districts = []
        for province in self.provinces:
            for i in range(np.random.randint(3, 6)):
                self.districts.append(f"{province}_District_{i+1}")
    
    def generate_massive_dataset(self, target_records=1000000):
        """Generate millions of GDP records"""
        print(f"🚀 Generating {target_records:,} GDP records...")
        
        # Calculate time range needed
        locations = len(self.districts)  # ~70 locations
        days_needed = target_records // locations // 24  # Hourly data
        
        # Generate hourly data over multiple years
        start_date = datetime(2020, 1, 1)
        end_date = start_date + timedelta(days=days_needed)
        
        print(f"📅 Time range: {start_date} to {end_date}")
        print(f"📍 Locations: {locations}")
        print(f"⏰ Generating hourly data...")
        
        # Generate in chunks to avoid memory issues
        chunk_size = 50000
        total_generated = 0
        
        # Initialize CSV files
        files = {
            'mobile_money_massive.csv': ['timestamp', 'province', 'district', 'transaction_volume', 'transaction_count'],
            'electricity_massive.csv': ['timestamp', 'province', 'district', 'consumption_kwh'],
            'internet_massive.csv': ['timestamp', 'province', 'district', 'data_usage_gb'],
            'social_massive.csv': ['timestamp', 'province', 'district', 'commercial_keywords']
        }
        
        # Write headers
        for filename, headers in files.items():
            pd.DataFrame(columns=headers).to_csv(filename, index=False)
        
        current_date = start_date
        
        while total_generated < target_records and current_date < end_date:
            chunk_data = {key: [] for key in files.keys()}
            
            # Generate chunk_size records
            for _ in range(min(chunk_size, target_records - total_generated)):
                # Random location and time
                district = np.random.choice(self.districts)
                province = district.split('_District_')[0]
                
                # Add some time variation
                timestamp = current_date + timedelta(
                    hours=np.random.randint(0, 24),
                    minutes=np.random.randint(0, 60)
                )
                
                # Generate correlated economic indicators
                base_activity = np.random.normal(100, 20)  # Base economic activity
                seasonal_factor = 1 + 0.3 * np.sin(timestamp.timetuple().tm_yday / 365 * 2 * np.pi)
                
                # Mobile money data
                mobile_volume = max(0, base_activity * 10 * seasonal_factor + np.random.normal(0, 100))
                mobile_count = max(1, int(base_activity * 0.5 + np.random.poisson(20)))
                
                chunk_data['mobile_money_massive.csv'].append({
                    'timestamp': timestamp,
                    'province': province,
                    'district': district,
                    'transaction_volume': mobile_volume,
                    'transaction_count': mobile_count
                })
                
                # Electricity data
                electricity = max(0, base_activity * 5 * seasonal_factor + np.random.normal(0, 50))
                chunk_data['electricity_massive.csv'].append({
                    'timestamp': timestamp,
                    'province': province,
                    'district': district,
                    'consumption_kwh': electricity
                })
                
                # Internet data
                internet = max(0, base_activity * 2 * seasonal_factor + np.random.normal(0, 20))
                chunk_data['internet_massive.csv'].append({
                    'timestamp': timestamp,
                    'province': province,
                    'district': district,
                    'data_usage_gb': internet
                })
                
                # Social media data
                social = max(0, base_activity * 0.8 + np.random.poisson(10))
                chunk_data['social_massive.csv'].append({
                    'timestamp': timestamp,
                    'province': province,
                    'district': district,
                    'commercial_keywords': social
                })
            
            # Append chunks to CSV files
            for filename, data in chunk_data.items():
                if data:
                    pd.DataFrame(data).to_csv(filename, mode='a', header=False, index=False)
            
            total_generated += len(chunk_data['mobile_money_massive.csv'])
            current_date += timedelta(hours=1)
            
            if total_generated % 100000 == 0:
                print(f"✅ Generated {total_generated:,} records...")
        
        print(f"🎉 MASSIVE DATASET COMPLETE!")
        print(f"📊 Total records: {total_generated:,}")
        
        # Show file sizes
        for filename in files.keys():
            if os.path.exists(filename):
                size_mb = os.path.getsize(filename) / (1024 * 1024)
                records = len(pd.read_csv(filename))
                print(f"   {filename}: {records:,} records ({size_mb:.1f} MB)")

if __name__ == "__main__":
    generator = MassDataGenerator()
    generator.generate_massive_dataset(1000000)  # 1 million records
