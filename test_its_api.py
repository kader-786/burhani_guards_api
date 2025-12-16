#!/usr/bin/env python3
"""
ITS External API Test Script
Tests the HandlerB2 and HandlerE1 endpoints
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:8000/BURHANI_GUARDS_API_TEST/api"
TEST_ITS_ID_LOGIN = "10001001"  # For login
TEST_PASSWORD = "5678"
TEST_ITS_ID_QUERY = "10001001"  # ITS ID to query in external API

# Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*70}")
    print(f"{text:^70}")
    print(f"{'='*70}{RESET}\n")

def print_success(msg):
    print(f"{GREEN}✓ {msg}{RESET}")

def print_error(msg):
    print(f"{RED}✗ {msg}{RESET}")

def print_info(msg):
    print(f"{YELLOW}ℹ {msg}{RESET}")


def login_and_get_token():
    """Login and get access token"""
    print_header("Step 1: Login to Get Access Token")
    
    try:
        response = requests.post(
            f"{BASE_URL}/Login/CheckLogin",
            json={
                "username": TEST_ITS_ID_LOGIN,
                "password": TEST_PASSWORD
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                token = data["tokens"]["access_token"]
                print_success(f"Login successful! Token: {token[:50]}...")
                return token
            else:
                print_error(f"Login failed: {data.get('message')}")
                return None
        else:
            print_error(f"Login failed with status {response.status_code}")
            return None
    
    except Exception as e:
        print_error(f"Login error: {str(e)}")
        return None


def test_handlerb2(token):
    """Test HandlerB2 endpoint"""
    print_header("Step 2: Test HandlerB2 API")
    
    try:
        print_info(f"Calling HandlerB2 for ITS ID: 30320819")
        
        response = requests.post(
            f"{BASE_URL}/ITS-API/HandlerB2",
            json={"its_id": 30320819},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n{YELLOW}Response:{RESET}")
            print(json.dumps(data, indent=2))
            
            if data.get("success"):
                print_success("HandlerB2 call successful!")
                return True
            else:
                print_error(f"HandlerB2 failed: {data.get('message')}")
                return False
        else:
            print_error(f"HandlerB2 failed with status {response.status_code}")
            print(response.text)
            return False
    
    except Exception as e:
        print_error(f"HandlerB2 error: {str(e)}")
        return False


def test_handlere1(token):
    """Test HandlerE1 endpoint"""
    print_header("Step 3: Test HandlerE1 API")
    
    try:
        print_info(f"Calling HandlerE1 for ITS ID: 30320819")
        
        response = requests.post(
            f"{BASE_URL}/ITS-API/HandlerE1",
            json={"its_id": 30320819},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n{YELLOW}Response:{RESET}")
            print(json.dumps(data, indent=2))
            
            if data.get("success"):
                print_success("HandlerE1 call successful!")
                return True
            else:
                print_error(f"HandlerE1 failed: {data.get('message')}")
                return False
        else:
            print_error(f"HandlerE1 failed with status {response.status_code}")
            print(response.text)
            return False
    
    except Exception as e:
        print_error(f"HandlerE1 error: {str(e)}")
        return False


def test_health():
    """Test ITS API health endpoint"""
    print_header("Step 4: Test ITS API Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/ITS-API/health")
        
        if response.status_code == 200:
            data = response.json()
            print(json.dumps(data, indent=2))
            print_success("Health check passed!")
            return True
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
    
    except Exception as e:
        print_error(f"Health check error: {str(e)}")
        return False


def main():
    print(f"\n{BLUE}{'='*70}")
    print(f"{'ITS External API Test Suite':^70}")
    print(f"{'='*70}{RESET}\n")
    
    print_info(f"Base URL: {BASE_URL}")
    print_info(f"Test ITS ID: {TEST_ITS_ID_QUERY}\n")
    
    # Step 1: Login
    token = login_and_get_token()
    if not token:
        print_error("\n❌ Cannot proceed without authentication token")
        return 1
    
    # Step 2: Test HandlerB2
    b2_result = test_handlerb2(token)
    
    # Step 3: Test HandlerE1
    e1_result = test_handlere1(token)
    
    # Step 4: Test health
    health_result = test_health()
    
    # Summary
    print_header("TEST SUMMARY")
    
    results = [
        ("Login", token is not None),
        ("HandlerB2", b2_result),
        ("HandlerE1", e1_result),
        ("Health Check", health_result)
    ]
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = f"{GREEN}PASSED{RESET}" if result else f"{RED}FAILED{RESET}"
        print(f"  {name:<20} {status}")
    
    print(f"\n{BLUE}Results: {passed}/{total} tests passed{RESET}")
    
    if passed == total:
        print(f"\n{GREEN}✓ All tests passed!{RESET}\n")
        return 0
    else:
        print(f"\n{RED}✗ Some tests failed!{RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())