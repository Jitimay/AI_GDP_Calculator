import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

class GDPPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.feature_columns = [
            'mobile_money_volume_normalized',
            'mobile_money_count_normalized', 
            'electricity_normalized',
            'internet_normalized',
            'social_score_normalized'
        ]
        self.is_trained = False
        self.model_path = 'gdp_model.pkl'
    
    def train_model(self, df):
        """Train the GDP prediction model"""
        # Prepare features and target
        X = df[self.feature_columns]
        y = df['informal_gdp_index']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        self.is_trained = True
        
        # Save model
        joblib.dump(self.model, self.model_path)
        
        return {
            'mse': mse,
            'r2_score': r2,
            'feature_importance': dict(zip(self.feature_columns, self.model.feature_importances_))
        }
    
    def load_model(self):
        """Load pre-trained model"""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.is_trained = True
            return True
        return False
    
    def predict(self, features):
        """Predict GDP index from features"""
        if not self.is_trained:
            if not self.load_model():
                raise ValueError("Model not trained and no saved model found")
        
        if isinstance(features, dict):
            # Convert dict to DataFrame
            features_df = pd.DataFrame([features])
            return self.model.predict(features_df[self.feature_columns])[0]
        else:
            # Assume DataFrame
            return self.model.predict(features[self.feature_columns])
    
    def predict_realtime(self, realtime_data):
        """Predict GDP for real-time data"""
        predictions = {}
        
        for province, data in realtime_data['data'].items():
            # Normalize features (simplified)
            features = {
                'mobile_money_volume_normalized': min(100, max(0, data['mobile_money'] / 20)),
                'mobile_money_count_normalized': min(100, max(0, data['mobile_money'] / 30)),
                'electricity_normalized': min(100, max(0, data['electricity'] / 10)),
                'internet_normalized': min(100, max(0, data['internet'] / 5)),
                'social_score_normalized': min(100, max(0, data['social_score']))
            }
            
            gdp_prediction = self.predict(features)
            predictions[province] = {
                'gdp_index': float(gdp_prediction),
                'confidence': np.random.uniform(0.7, 0.95),  # Simulated confidence
                'features': features
            }
        
        return predictions
    
    def get_feature_importance(self):
        """Get feature importance from trained model"""
        if not self.is_trained:
            return {}
        
        return dict(zip(self.feature_columns, self.model.feature_importances_))
