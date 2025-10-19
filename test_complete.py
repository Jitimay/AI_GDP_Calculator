#!/usr/bin/env python3
import subprocess
import time
import requests
import json

def test_system():
    print("🧪 Complete System Test")
    print("=" * 50)
    
    # 1. Start the system
    print("\n1. Starting system...")
    try:
        subprocess.run(["./start_system.sh"], check=True, timeout=10)
        time.sleep(5)  # Wait for services to start
    except:
        print("❌ Failed to start system")
        return
    
    # 2. Test API endpoints
    print("\n2. Testing API...")
    endpoints = [
        ("/health", "GET"),
        ("/predict", "GET"), 
        ("/alerts", "GET"),
        ("/train-model", "POST")
    ]
    
    for endpoint, method in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"http://localhost:5000{endpoint}")
            else:
                response = requests.post(f"http://localhost:5000{endpoint}")
            
            if response.status_code == 200:
                print(f"✅ {endpoint} - OK")
            else:
                print(f"❌ {endpoint} - Failed ({response.status_code})")
        except Exception as e:
            print(f"❌ {endpoint} - Error: {e}")
    
    # 3. Test dashboard
    print("\n3. Testing dashboard...")
    try:
        response = requests.get("http://localhost:8501")
        print("✅ Dashboard accessible" if response.status_code == 200 else "❌ Dashboard failed")
    except:
        print("❌ Dashboard not accessible")

if __name__ == "__main__":
    test_system()
