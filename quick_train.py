import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# Create synthetic training data
data = []
for i in range(1000):
    row = {
        'mobile_money_volume_normalized': np.random.uniform(0, 100),
        'mobile_money_count_normalized': np.random.uniform(0, 100),
        'electricity_normalized': np.random.uniform(0, 100),
        'internet_normalized': np.random.uniform(0, 100),
        'social_score_normalized': np.random.uniform(0, 100)
    }
    # Realistic GDP calculation
    gdp = (row['mobile_money_volume_normalized'] * 0.3 + 
           row['electricity_normalized'] * 0.25 + 
           row['internet_normalized'] * 0.2 + 
           row['social_score_normalized'] * 0.15 + 
           row['mobile_money_count_normalized'] * 0.1)
    row['informal_gdp_index'] = gdp
    data.append(row)

df = pd.DataFrame(data)

# Train model
features = ['mobile_money_volume_normalized', 'mobile_money_count_normalized', 
           'electricity_normalized', 'internet_normalized', 'social_score_normalized']
X = df[features]
y = df['informal_gdp_index']

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model
joblib.dump(model, 'gdp_model.pkl')
print("✅ Model trained and saved as gdp_model.pkl")
