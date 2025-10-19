#!/usr/bin/env python3
"""
Test the API (assumes it's already running)
"""

import requests
import json
import time

def test_api():
    print("🧪 Testing GDP Calculator API")
    print("=" * 35)
    print("   (Make sure API is running: python run_project.py)")
    print()
    
    base_url = "http://localhost:5001"
    
    tests = [
        ("Health Check", f"{base_url}/health"),
        ("GDP Prediction", f"{base_url}/predict"),
        ("Dashboard Data", f"{base_url}/dashboard-data"),
        ("Alerts", f"{base_url}/alerts"),
        ("Elasticsearch Search", f"{base_url}/search/recent?hours=1")
    ]
    
    for test_name, url in tests:
        print(f"🔍 {test_name}...")
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {test_name} - SUCCESS")
                
                # Show relevant info
                if "health" in url:
                    print(f"   Status: {data.get('status')}")
                    es_status = data.get('elasticsearch', {}).get('status', 'unknown')
                    print(f"   Elasticsearch: {es_status}")
                elif "predict" in url:
                    print(f"   National Index: {data.get('national_index', 0):.2f}")
                    print(f"   Provinces: {len(data.get('provincial_data', {}))}")
                elif "dashboard" in url:
                    current = data.get('current', {})
                    print(f"   National Index: {current.get('national_index', 0):.2f}")
                    print(f"   Alerts: {len(data.get('alerts', []))}")
                elif "alerts" in url:
                    print(f"   Alert Count: {data.get('count', 0)}")
                elif "search" in url:
                    print(f"   Records Found: {data.get('count', 0)}")
                    
            elif response.status_code == 503:
                print(f"⚠️  {test_name} - Service Unavailable (expected for ES if not running)")
            else:
                print(f"❌ {test_name} - FAILED ({response.status_code})")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ {test_name} - CONNECTION REFUSED")
            print("   Make sure API is running: python run_project.py")
            break
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
        
        time.sleep(0.5)  # Small delay between tests
    
    print("\n" + "=" * 35)
    print("🎯 Test Complete!")

if __name__ == "__main__":
    test_api()