import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class DataPreprocessor:
    def __init__(self):
        self.scalers = {}
    
    def preprocess_data(self, data_dict):
        """Normalize and merge all data sources"""
        processed_data = []
        
        # Convert timestamps
        for key, df in data_dict.items():
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Get common date range
        dates = data_dict['mobile_money']['timestamp'].unique()
        provinces = data_dict['mobile_money']['province'].unique()
        
        for date in dates:
            for province in provinces:
                row = {'timestamp': date, 'province': province}
                
                # Mobile money features
                mm_data = data_dict['mobile_money'][
                    (data_dict['mobile_money']['timestamp'] == date) & 
                    (data_dict['mobile_money']['province'] == province)
                ]
                if not mm_data.empty:
                    row['mobile_money_volume'] = mm_data['transaction_volume'].iloc[0]
                    row['mobile_money_count'] = mm_data['transaction_count'].iloc[0]
                else:
                    row['mobile_money_volume'] = 0
                    row['mobile_money_count'] = 0
                
                # Electricity features
                elec_data = data_dict['electricity'][
                    (data_dict['electricity']['timestamp'] == date) & 
                    (data_dict['electricity']['province'] == province)
                ]
                row['electricity'] = elec_data['consumption_kwh'].iloc[0] if not elec_data.empty else 0
                
                # Internet features
                internet_data = data_dict['internet'][
                    (data_dict['internet']['timestamp'] == date) & 
                    (data_dict['internet']['province'] == province)
                ]
                row['internet'] = internet_data['data_usage_gb'].iloc[0] if not internet_data.empty else 0
                
                # Social media features
                social_data = data_dict['social'][
                    (data_dict['social']['timestamp'] == date) & 
                    (data_dict['social']['province'] == province)
                ]
                if not social_data.empty:
                    row['social_score'] = (
                        social_data['selling_mentions'].iloc[0] + 
                        social_data['buying_mentions'].iloc[0] + 
                        social_data['market_mentions'].iloc[0]
                    )
                else:
                    row['social_score'] = 0
                
                processed_data.append(row)
        
        df = pd.DataFrame(processed_data)
        return self.normalize_features(df)
    
    def normalize_features(self, df):
        """Normalize features to 0-100 scale"""
        feature_cols = ['mobile_money_volume', 'mobile_money_count', 'electricity', 'internet', 'social_score']
        
        for col in feature_cols:
            if col not in self.scalers:
                self.scalers[col] = MinMaxScaler(feature_range=(0, 100))
                df[f'{col}_normalized'] = self.scalers[col].fit_transform(df[[col]])
            else:
                df[f'{col}_normalized'] = self.scalers[col].transform(df[[col]])
        
        return df
    
    def create_target_variable(self, df):
        """Create synthetic GDP index target variable"""
        # Weighted combination of normalized features
        weights = {
            'mobile_money_volume_normalized': 0.3,
            'electricity_normalized': 0.25,
            'internet_normalized': 0.2,
            'mobile_money_count_normalized': 0.15,
            'social_score_normalized': 0.1
        }
        
        df['informal_gdp_index'] = 0
        for feature, weight in weights.items():
            df['informal_gdp_index'] += df[feature] * weight
        
        # Add some noise
        df['informal_gdp_index'] += np.random.normal(0, 5, len(df))
        df['informal_gdp_index'] = np.clip(df['informal_gdp_index'], 0, 100)
        
        return df
