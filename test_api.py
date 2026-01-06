#!/usr/bin/env python3
"""
Test script for Math Operations API
Run after starting the server to verify functionality
"""

import requests
import sys

BASE_URL = "http://localhost:8000"

def test_root():
    """Test root endpoint"""
    print("Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 200

def test_health():
    """Test health check endpoint"""
    print("Testing health check endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 200

def test_calculate():
    """Test calculate endpoint"""
    print("Testing calculate endpoint...")
    
    test_cases = [
        {"x": 10, "y": 5, "expected_sum": 15, "expected_mult": 50},
        {"x": 7.5, "y": 2.5, "expected_sum": 10, "expected_mult": 18.75},
        {"x": -3, "y": 4, "expected_sum": 1, "expected_mult": -12},
        {"x": 0, "y": 100, "expected_sum": 100, "expected_mult": 0},
    ]
    
    all_passed = True
    
    for i, test in enumerate(test_cases, 1):
        print(f"Test case {i}: x={test['x']}, y={test['y']}")
        response = requests.post(
            f"{BASE_URL}/calculate",
            json={"x": test["x"], "y": test["y"]}
        )
        
        if response.status_code != 200:
            print(f"❌ Failed with status code: {response.status_code}")
            all_passed = False
            continue
        
        result = response.json()
        print(f"Response: {result}")
        
        if result["sum"] == test["expected_sum"] and result["mult"] == test["expected_mult"]:
            print("✅ Passed\n")
        else:
            print(f"❌ Failed - Expected sum={test['expected_sum']}, mult={test['expected_mult']}\n")
            all_passed = False
    
    return all_passed

def main():
    print("=" * 50)
    print("Math Operations API Test Suite")
    print("=" * 50 + "\n")
    
    try:
        results = []
        results.append(("Root endpoint", test_root()))
        results.append(("Health check", test_health()))
        results.append(("Calculate endpoint", test_calculate()))
        
        print("=" * 50)
        print("Test Results Summary")
        print("=" * 50)
        
        for name, passed in results:
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"{name}: {status}")
        
        if all(passed for _, passed in results):
            print("\n🎉 All tests passed!")
            sys.exit(0)
        else:
            print("\n❌ Some tests failed")
            sys.exit(1)
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API.")
        print(f"Make sure the server is running at {BASE_URL}")
        sys.exit(1)

if __name__ == "__main__":
    main()