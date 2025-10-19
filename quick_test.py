#!/usr/bin/env python3
import subprocess
import time
import requests
import sys

def test_system():
    print("🧪 Quick System Test")
    print("=" * 30)
    
    # 1. Start API in background
    print("🚀 Starting API...")
    api_process = subprocess.Popen([sys.executable, "api.py"], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
    
    # Wait for API to start
    time.sleep(3)
    
    # 2. Test endpoints
    tests = [
        ("Health Check", "GET", "/health"),
        ("GDP Prediction", "GET", "/predict"),
        ("Alerts", "GET", "/alerts")
    ]
    
    for name, method, endpoint in tests:
        try:
            url = f"http://localhost:5000{endpoint}"
            if method == "GET":
                response = requests.get(url, timeout=5)
            else:
                response = requests.post(url, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {name} - OK")
                if endpoint == "/predict":
                    data = response.json()
                    print(f"   National GDP Index: {data.get('national_index', 'N/A')}")
            else:
                print(f"❌ {name} - Failed ({response.status_code})")
        except Exception as e:
            print(f"❌ {name} - Error: {e}")
    
    # 3. Cleanup
    api_process.terminate()
    print("\n🎯 Test Complete!")

if __name__ == "__main__":
    test_system()
