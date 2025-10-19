#!/usr/bin/env python3
"""
Start the API and test it
"""

import subprocess
import time
import requests
import signal
import sys
import os

def start_and_test():
    print("🚀 Starting GDP Calculator API and Testing")
    print("=" * 50)
    
    api_process = None
    try:
        # Start the API
        print("\n1. Starting API server...")
        api_process = subprocess.Popen(
            [sys.executable, 'run_project.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for startup
        print("   Waiting for API to start...")
        time.sleep(5)
        
        # Check if process is running
        if api_process.poll() is not None:
            stdout, stderr = api_process.communicate()
            print("❌ API failed to start")
            print(f"   stdout: {stdout}")
            print(f"   stderr: {stderr}")
            return
        
        print("✅ API process started")
        
        # Test endpoints
        print("\n2. Testing API endpoints...")
        
        # Health check
        try:
            response = requests.get("http://localhost:5001/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print("✅ Health check passed")
                print(f"   Status: {data['status']}")
                es_status = data.get('elasticsearch', {}).get('status', 'unknown')
                print(f"   Elasticsearch: {es_status}")
            else:
                print(f"❌ Health check failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Health check error: {e}")
        
        # GDP Prediction
        try:
            response = requests.get("http://localhost:5001/predict", timeout=15)
            if response.status_code == 200:
                data = response.json()
                print("✅ GDP prediction working")
                print(f"   National Index: {data['national_index']:.2f}")
                print(f"   Provinces: {len(data['provincial_data'])}")
            else:
                print(f"❌ GDP prediction failed: {response.status_code}")
        except Exception as e:
            print(f"❌ GDP prediction error: {e}")
        
        # Elasticsearch search test
        try:
            response = requests.get("http://localhost:5001/search/recent?hours=1", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print("✅ Elasticsearch search working")
                print(f"   Records found: {data['count']}")
            elif response.status_code == 503:
                print("⚠️  Elasticsearch not available")
            else:
                print(f"❌ Elasticsearch search failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Elasticsearch search error: {e}")
        
        print("\n" + "=" * 50)
        print("🎯 Test Complete!")
        print("\n📊 Your GDP Calculator is running on:")
        print("   http://localhost:5001/health")
        print("   http://localhost:5001/predict")
        print("   http://localhost:5001/dashboard-data")
        print("\n⚠️  Press Ctrl+C to stop the API")
        
        # Keep running
        try:
            api_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping API...")
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping API...")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Clean up
        if api_process:
            try:
                api_process.terminate()
                api_process.wait(timeout=5)
                print("✅ API stopped cleanly")
            except:
                api_process.kill()
                print("🔪 API force killed")

if __name__ == "__main__":
    start_and_test()