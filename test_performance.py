#!/usr/bin/env python3
import time
import requests
import concurrent.futures

def test_api_performance():
    """Test API performance under load"""
    print("⚡ Performance Testing")
    print("=" * 30)
    
    def make_request():
        try:
            start = time.time()
            response = requests.get("http://localhost:5000/predict", timeout=5)
            end = time.time()
            return response.status_code == 200, end - start
        except:
            return False, 0
    
    # Test concurrent requests
    num_requests = 10
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request) for _ in range(num_requests)]
        results = [future.result() for future in futures]
    
    successful = sum(1 for success, _ in results if success)
    response_times = [time for success, time in results if success]
    
    if response_times:
        avg_time = sum(response_times) / len(response_times)
        print(f"✅ {successful}/{num_requests} requests successful")
        print(f"📊 Average response time: {avg_time:.3f}s")
    else:
        print("❌ No successful requests")

if __name__ == "__main__":
    test_api_performance()
