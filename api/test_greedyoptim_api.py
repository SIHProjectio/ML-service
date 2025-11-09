#!/usr/bin/env python3
"""
Test script for GreedyOptim API
Tests all endpoints with sample data
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8001"


def test_health():
    """Test health check endpoint"""
    print("\n" + "="*70)
    print("Testing Health Check")
    print("="*70)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_methods():
    """Test methods listing endpoint"""
    print("\n" + "="*70)
    print("Testing Methods Listing")
    print("="*70)
    
    response = requests.get(f"{BASE_URL}/methods")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        methods = response.json()
        print(f"\nAvailable Methods: {len(methods['available_methods'])}")
        for method, info in methods['available_methods'].items():
            print(f"  {method}: {info['name']}")
    
    return response.status_code == 200


def test_generate_synthetic():
    """Test synthetic data generation"""
    print("\n" + "="*70)
    print("Testing Synthetic Data Generation")
    print("="*70)
    
    payload = {
        "num_trainsets": 20,
        "maintenance_rate": 0.1,
        "availability_rate": 0.8
    }
    
    response = requests.post(f"{BASE_URL}/generate-synthetic", json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nGenerated Data:")
        print(f"  Trainsets: {result['metadata']['num_trainsets']}")
        print(f"  Fitness Certificates: {result['metadata']['num_fitness_certificates']}")
        print(f"  Job Cards: {result['metadata']['num_job_cards']}")
        print(f"  Component Health: {result['metadata']['num_component_health']}")
        return result['data']  # Return for use in other tests
    
    return None


def test_validate(data):
    """Test data validation endpoint"""
    print("\n" + "="*70)
    print("Testing Data Validation")
    print("="*70)
    
    # Create request from synthetic data
    request_data = {
        "trainset_status": data['trainset_status'],
        "fitness_certificates": data['fitness_certificates'],
        "job_cards": data['job_cards'],
        "component_health": data['component_health'],
        "method": "ga"
    }
    
    response = requests.post(f"{BASE_URL}/validate", json=request_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nValidation Result:")
        print(f"  Valid: {result['valid']}")
        if result['valid']:
            print(f"  Trainsets: {result['num_trainsets']}")
            print(f"  Certificates: {result['num_certificates']}")
            print(f"  Job Cards: {result['num_job_cards']}")
            print(f"  Component Health: {result['num_component_health']}")
        else:
            print(f"  Errors: {len(result.get('validation_errors', []))}")
    
    return response.status_code == 200


def test_optimize(data):
    """Test optimization endpoint"""
    print("\n" + "="*70)
    print("Testing Schedule Optimization")
    print("="*70)
    
    # Create optimization request
    request_data = {
        "trainset_status": data['trainset_status'],
        "fitness_certificates": data['fitness_certificates'],
        "job_cards": data['job_cards'],
        "component_health": data['component_health'],
        "method": "ga",
        "config": {
            "required_service_trains": 15,
            "min_standby": 2,
            "population_size": 30,
            "generations": 50
        }
    }
    
    print(f"Optimizing with method: {request_data['method']}")
    print(f"Trainsets: {len(request_data['trainset_status'])}")
    
    response = requests.post(f"{BASE_URL}/optimize", json=request_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nOptimization Results:")
        print(f"  Method: {result['method']}")
        print(f"  Fitness Score: {result['fitness_score']:.4f}")
        print(f"  Execution Time: {result['execution_time_seconds']:.3f}s")
        print(f"\n  Schedule Allocation:")
        print(f"    In Service: {result['num_service']} trains")
        print(f"    Standby: {result['num_standby']} trains")
        print(f"    Maintenance: {result['num_maintenance']} trains")
        print(f"    Unavailable: {result['num_unavailable']} trains")
        print(f"\n  Detailed Scores:")
        print(f"    Service: {result['service_score']:.4f}")
        print(f"    Standby: {result['standby_score']:.4f}")
        print(f"    Health: {result['health_score']:.4f}")
        print(f"    Certificate: {result['certificate_score']:.4f}")
        print(f"\n  Constraints Satisfied: {result['constraints_satisfied']}")
        
        if result.get('warnings'):
            print(f"  Warnings: {len(result['warnings'])}")
            for warning in result['warnings'][:3]:
                print(f"    - {warning}")
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200


def test_compare(data):
    """Test method comparison endpoint"""
    print("\n" + "="*70)
    print("Testing Method Comparison")
    print("="*70)
    
    # Create comparison request
    request_data = {
        "trainset_status": data['trainset_status'][:15],  # Use smaller dataset for faster comparison
        "fitness_certificates": [fc for fc in data['fitness_certificates'] if fc['trainset_id'] in [ts['trainset_id'] for ts in data['trainset_status'][:15]]],
        "job_cards": [jc for jc in data['job_cards'] if jc['trainset_id'] in [ts['trainset_id'] for ts in data['trainset_status'][:15]]],
        "component_health": [ch for ch in data['component_health'] if ch['trainset_id'] in [ts['trainset_id'] for ts in data['trainset_status'][:15]]],
        "methods": ["ga", "pso"],
        "config": {
            "population_size": 20,
            "generations": 30
        }
    }
    
    print(f"Comparing methods: {request_data['methods']}")
    print(f"Trainsets: {len(request_data['trainset_status'])}")
    
    response = requests.post(f"{BASE_URL}/compare", json=request_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nComparison Results:")
        print(f"  Total Execution Time: {result['summary']['total_execution_time']:.3f}s")
        print(f"  Best Method: {result['summary']['best_method']}")
        print(f"  Best Score: {result['summary']['best_score']:.4f}")
        
        print(f"\n  Individual Results:")
        for method, method_result in result['methods'].items():
            print(f"    {method.upper()}:")
            print(f"      Fitness: {method_result['fitness_score']:.4f}")
            print(f"      Service: {method_result['num_service']} trains")
            print(f"      Time: {method_result.get('execution_time_seconds', 'N/A')}")
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200


def test_custom_data():
    """Test with minimal custom data"""
    print("\n" + "="*70)
    print("Testing with Custom Minimal Data")
    print("="*70)
    
    # Create minimal valid data
    custom_data = {
        "trainset_status": [
            {"trainset_id": f"KMRL-{i:02d}", "operational_status": "Available"}
            for i in range(1, 11)
        ],
        "fitness_certificates": [
            {
                "trainset_id": f"KMRL-{i:02d}",
                "department": "Safety",
                "status": "Valid",
                "expiry_date": (datetime.now() + timedelta(days=365)).isoformat()
            }
            for i in range(1, 11)
        ],
        "job_cards": [],  # No job cards
        "component_health": [
            {
                "trainset_id": f"KMRL-{i:02d}",
                "component": "Brakes",
                "status": "Good",
                "wear_level": 20.0
            }
            for i in range(1, 11)
        ],
        "method": "ga",
        "config": {
            "required_service_trains": 8,
            "min_standby": 1,
            "population_size": 20,
            "generations": 30
        }
    }
    
    print(f"Testing with {len(custom_data['trainset_status'])} trainsets")
    
    response = requests.post(f"{BASE_URL}/optimize", json=custom_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nOptimization successful!")
        print(f"  Fitness: {result['fitness_score']:.4f}")
        print(f"  In Service: {result['num_service']}")
        print(f"  Time: {result['execution_time_seconds']:.3f}s")
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200


def main():
    """Run all tests"""
    print("=" * 70)
    print("GREEDYOPTIM API TEST SUITE")
    print("=" * 70)
    print(f"Testing API at: {BASE_URL}")
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # Run tests
    results['health'] = test_health()
    results['methods'] = test_methods()
    
    # Generate synthetic data for remaining tests
    synthetic_data = test_generate_synthetic()
    
    if synthetic_data:
        results['validate'] = test_validate(synthetic_data)
        results['optimize'] = test_optimize(synthetic_data)
        results['compare'] = test_compare(synthetic_data)
    
    results['custom'] = test_custom_data()
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}")
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status} - {test_name}")
    
    print("\n" + "="*70)
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Could not connect to API")
        print("  Make sure the API is running:")
        print("  python api/run_greedyoptim_api.py")
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
