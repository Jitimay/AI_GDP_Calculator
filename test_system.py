#!/usr/bin/env python3
"""
Test script to demonstrate the AI-Powered Informal Sector GDP Calculator
"""

import requests
import json
import time

API_BASE = "http://localhost:5000"

def test_api_endpoints():
    """Test all API endpoints"""
    print("🚀 Testing AI-Powered Informal Sector GDP Calculator")
    print("=" * 60)
    
    # Test health endpoint
    print("\n1. Testing Health Endpoint...")
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Status: {response.json()['status']}")
        else:
            print("❌ Health check failed")
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return
    
    # Test prediction endpoint
    print("\n2. Testing GDP Prediction...")
    try:
        response = requests.get(f"{API_BASE}/predict")
        if response.status_code == 200:
            data = response.json()
            print("✅ GDP prediction successful")
            print(f"   National Index: {data['national_index']:.2f}")
            print("   Provincial Data:")
            for province, info in data['provincial_data'].items():
                print(f"     {province}: {info['composite_index']:.2f}")
        else:
            print("❌ GDP prediction failed")
    except Exception as e:
        print(f"❌ GDP prediction error: {e}")
    
    # Test model training
    print("\n3. Testing ML Model Training...")
    try:
        response = requests.post(f"{API_BASE}/train-model")
        if response.status_code == 200:
            data = response.json()
            print("✅ Model training successful")
            print(f"   R² Score: {data['training_results']['r2_score']:.4f}")
            print(f"   MSE: {data['training_results']['mse']:.2f}")
        else:
            print("❌ Model training failed")
    except Exception as e:
        print(f"❌ Model training error: {e}")
    
    # Test alerts
    print("\n4. Testing Alert System...")
    try:
        response = requests.get(f"{API_BASE}/alerts")
        if response.status_code == 200:
            data = response.json()
            print("✅ Alert system working")
            print(f"   Active alerts: {data['count']}")
        else:
            print("❌ Alert system failed")
    except Exception as e:
        print(f"❌ Alert system error: {e}")
    
    # Test dashboard data
    print("\n5. Testing Dashboard Data...")
    try:
        response = requests.get(f"{API_BASE}/dashboard-data")
        if response.status_code == 200:
            data = response.json()
            print("✅ Dashboard data available")
            print(f"   Historical data points: {len(data.get('historical', {}))}")
        else:
            print("❌ Dashboard data failed")
    except Exception as e:
        print(f"❌ Dashboard data error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 System Test Complete!")
    print("\nTo view the dashboard:")
    print("1. Run: streamlit run dashboard.py")
    print("2. Open: http://localhost:8501")
    print("\nAPI Documentation:")
    print("- Health: GET /health")
    print("- Predict: GET /predict") 
    print("- Train: POST /train-model")
    print("- Alerts: GET /alerts")
    print("- Dashboard: GET /dashboard-data")

if __name__ == "__main__":
    test_api_endpoints()
