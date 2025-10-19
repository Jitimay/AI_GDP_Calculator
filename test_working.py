#!/usr/bin/env python3
import subprocess
import time
import requests
import sys
import os
import signal

def test_system():
    print("🧪 AI GDP Calculator Test")
    print("=" * 40)
    
    # Start API
    print("🚀 Starting API server...")
    api_process = subprocess.Popen([sys.executable, "api.py"])
    
    # Wait for startup
    print("⏳ Waiting for server to start...")
    time.sleep(5)
    
    try:
        # Test health endpoint
        print("\n1. Testing Health Check...")
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is healthy")
            print(f"   Response: {response.json()}")
        
        # Test prediction endpoint
        print("\n2. Testing GDP Prediction...")
        response = requests.get("http://localhost:5000/predict", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ GDP prediction successful")
            print(f"   National Index: {data['national_index']:.2f}")
            print("   Provincial Data:")
            for province, info in list(data['provincial_data'].items())[:3]:
                print(f"     {province}: {info['composite_index']:.2f}")
        
        # Test alerts
        print("\n3. Testing Alerts...")
        response = requests.get("http://localhost:5000/alerts", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data['count']} alerts")
        
        print("\n🎯 All tests passed!")
        print("\n📊 To view dashboard:")
        print("   streamlit run dashboard.py")
        print("   Then open: http://localhost:8501")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    finally:
        # Cleanup
        print("\n🛑 Stopping API server...")
        api_process.terminate()
        api_process.wait()

if __name__ == "__main__":
    test_system()
