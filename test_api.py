"""
API Test Suite for DataService
Tests all endpoints and saves results to JSON
"""
import requests
import json
from datetime import datetime


BASE_URL = "http://localhost:8000"
results = {
    "test_run": datetime.now().isoformat(),
    "base_url": BASE_URL,
    "tests": []
}


def test_endpoint(name, method, endpoint, **kwargs):
    """Test an API endpoint and record results"""
    print(f"\nTesting: {name}")
    print(f"  {method} {endpoint}")
    
    try:
        url = f"{BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, **kwargs)
        elif method == "POST":
            response = requests.post(url, **kwargs)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        result = {
            "name": name,
            "method": method,
            "endpoint": endpoint,
            "status_code": response.status_code,
            "success": response.status_code in [200, 201],
            "response_size": len(response.text),
            "timestamp": datetime.now().isoformat()
        }
        
        if response.status_code == 200:
            try:
                result["response_data"] = response.json()
                print(f"  ✓ Success - {response.status_code}")
            except:
                result["response_text"] = response.text[:200]
                print(f"  ✓ Success - {response.status_code} (non-JSON)")
        else:
            result["error"] = response.text[:500]
            print(f"  ✗ Failed - {response.status_code}")
        
        results["tests"].append(result)
        return result
        
    except Exception as e:
        result = {
            "name": name,
            "method": method,
            "endpoint": endpoint,
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
        results["tests"].append(result)
        print(f"  ✗ Error: {e}")
        return result


def run_tests():
    """Run all API tests"""
    print("=" * 70)
    print("DataService API Test Suite")
    print("=" * 70)
    
    # Test 1: Root endpoint
    test_endpoint(
        "Root Endpoint",
        "GET",
        "/"
    )
    
    # Test 2: Health check
    test_endpoint(
        "Health Check",
        "GET",
        "/health"
    )
    
    # Test 3: Quick schedule generation
    test_endpoint(
        "Quick Schedule Generation",
        "POST",
        "/api/v1/generate/quick?date=2025-10-26&num_trains=25&num_stations=25"
    )
    
    # Test 4: Full schedule generation
    test_endpoint(
        "Full Schedule Generation",
        "POST",
        "/api/v1/generate",
        json={
            "date": "2025-10-26",
            "num_trains": 30,
            "num_stations": 25,
            "min_service_trains": 22,
            "min_standby_trains": 3
        },
        headers={"Content-Type": "application/json"}
    )
    
    # Test 5: Example schedule
    test_endpoint(
        "Example Schedule",
        "GET",
        "/api/v1/schedule/example"
    )
    
    # Test 6: Route information
    test_endpoint(
        "Route Information (25 stations)",
        "GET",
        "/api/v1/route/25"
    )
    
    # Test 7: Train health data
    test_endpoint(
        "Train Health Data (30 trains)",
        "GET",
        "/api/v1/trains/health/30"
    )
    
    # Test 8: Depot layout
    test_endpoint(
        "Depot Layout",
        "GET",
        "/api/v1/depot/layout"
    )
    
    # Test 9: Custom schedule with all parameters
    test_endpoint(
        "Custom Schedule Full Parameters",
        "POST",
        "/api/v1/generate",
        json={
            "date": "2025-11-01",
            "num_trains": 35,
            "num_stations": 25,
            "route_name": "Aluva-Pettah Line",
            "depot_name": "Muttom_Depot",
            "min_service_trains": 25,
            "min_standby_trains": 5,
            "max_daily_km_per_train": 280,
            "balance_mileage": True,
            "prioritize_branding": True
        },
        headers={"Content-Type": "application/json"}
    )
    
    # Test 10: Quick generation with minimal params
    test_endpoint(
        "Quick Generation Minimal",
        "POST",
        "/api/v1/generate/quick?date=2025-10-27&num_trains=20"
    )


def save_results():
    """Save test results to JSON file"""
    # Summary
    total = len(results["tests"])
    passed = sum(1 for t in results["tests"] if t.get("success", False))
    
    results["summary"] = {
        "total_tests": total,
        "passed": passed,
        "failed": total - passed,
        "success_rate": f"{(passed/total)*100:.1f}%" if total > 0 else "0%"
    }
    
    filename = f"api_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {results['summary']['success_rate']}")
    print(f"\nResults saved to: {filename}")
    print("=" * 70)


if __name__ == "__main__":
    try:
        run_tests()
        save_results()
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        save_results()
    except Exception as e:
        print(f"\n\nError during testing: {e}")
        save_results()
