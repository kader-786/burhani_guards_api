#!/usr/bin/env python3
"""
Guards API Test Script
Tests the guards endpoints
"""

import requests
import json
import sys
from datetime import date

# Configuration
BASE_URL = "http://localhost:8000/BURHANI_GUARDS_API_TEST/api"
TEST_ITS_ID = "10001001"
TEST_PASSWORD = "5678"
TEST_DATE = "2025-01-10"  # Update with actual miqaat date

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
                "username": TEST_ITS_ID,
                "password": TEST_PASSWORD
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                token = data["tokens"]["access_token"]
                print_success(f"Login successful!")
                print_info(f"Token: {token[:50]}...")
                print_info(f"User: {data['data']['full_name']}")
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


def test_accepted_guards_by_date(token):
    """Test GetAcceptedGuardsByMiqaatDate endpoint"""
    print_header("Step 2: Test Accepted Guards by Miqaat Date")
    
    try:
        print_info(f"Calling GetAcceptedGuardsByMiqaatDate for date: {TEST_DATE}")
        
        response = requests.post(
            f"{BASE_URL}/Guards/GetAcceptedGuardsByMiqaatDate",
            json={"miqaat_date": TEST_DATE},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n{YELLOW}Response:{RESET}")
            print(json.dumps(data, indent=2))
            
            if data.get("success"):
                print_success("Accepted guards retrieved successfully!")
                
                # Display summary
                guards = data.get("data", [])
                if guards:
                    print_info(f"\nFound {len(guards)} accepted guard(s) for {TEST_DATE}:")
                    for guard in guards[:5]:  # Show first 5
                        print(f"  • {guard.get('full_name')} ({guard.get('its_id')}) - {guard.get('team_name')}")
                    if len(guards) > 5:
                        print(f"  ... and {len(guards) - 5} more")
                else:
                    print_info(f"No accepted guards found for {TEST_DATE}")
                
                return True
            else:
                print_error(f"Query failed: {data.get('message')}")
                return False
        else:
            print_error(f"Request failed with status {response.status_code}")
            print(response.text)
            return False
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_guard_check(token):
    """Test GuardCheck endpoint"""
    print_header("Step 3: Test Guard Check")
    
    try:
        print_info(f"Calling GuardCheck for its_id: {TEST_ITS_ID}")
        
        response = requests.post(
            f"{BASE_URL}/Guards/GuardCheck",
            json={"its_id": int(TEST_ITS_ID)},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n{YELLOW}Response:{RESET}")
            print(json.dumps(data, indent=2))
            
            if data.get("success"):
                print_success("Guard information retrieved successfully!")
                
                # Display summary
                guards = data.get("data", [])
                if guards:
                    guard = guards[0]
                    print_info(f"\nGuard Information:")
                    print(f"  • Name: {guard.get('full_name')}")
                    print(f"  • ITS ID: {guard.get('its_id')}")
                    print(f"  • Team: {guard.get('team_name')}")
                    print(f"  • Position: {guard.get('position_name')}")
                    print(f"  • Mobile: {guard.get('mobile')}")
                else:
                    print_info("No guard information found")
                
                return True
            else:
                print_error(f"Query failed: {data.get('message')}")
                return False
        else:
            print_error(f"Request failed with status {response.status_code}")
            print(response.text)
            return False
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_check_my_guard_info(token):
    """Test CheckMyGuardInfo endpoint"""
    print_header("Step 4: Test Check My Guard Info (Convenience Endpoint)")
    
    try:
        print_info("Calling CheckMyGuardInfo (uses ITS ID from token)")
        
        response = requests.get(
            f"{BASE_URL}/Guards/CheckMyGuardInfo",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n{YELLOW}Response:{RESET}")
            print(json.dumps(data, indent=2))
            
            if data.get("success"):
                print_success("My guard info retrieved successfully!")
                
                # Display summary
                guards = data.get("data", [])
                if guards:
                    guard = guards[0]
                    print_info(f"\nYour Guard Information:")
                    print(f"  • Name: {guard.get('full_name')}")
                    print(f"  • Team: {guard.get('team_name')}")
                    print(f"  • Position: {guard.get('position_name')}")
                else:
                    print_info("No guard information found")
                
                return True
            else:
                print_error(f"Query failed: {data.get('message')}")
                return False
        else:
            print_error(f"Request failed with status {response.status_code}")
            print(response.text)
            return False
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_health():
    """Test guards health endpoint"""
    print_header("Step 5: Test Guards Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/Guards/health")
        
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
    print(f"{'Guards API Test Suite':^70}")
    print(f"{'='*70}{RESET}\n")
    
    print_info(f"Base URL: {BASE_URL}")
    print_info(f"Test ITS ID: {TEST_ITS_ID}")
    print_info(f"Test Date: {TEST_DATE}\n")
    
    # Step 1: Login
    token = login_and_get_token()
    if not token:
        print_error("\n❌ Cannot proceed without authentication token")
        return 1
    
    # Step 2: Test accepted guards by date
    test1 = test_accepted_guards_by_date(token)
    
    # Step 3: Test guard check
    test2 = test_guard_check(token)
    
    # Step 4: Test my guard info
    test3 = test_check_my_guard_info(token)
    
    # Step 5: Test health
    test4 = test_health()
    
    # Summary
    print_header("TEST SUMMARY")
    
    results = [
        ("Login", token is not None),
        ("Accepted Guards by Date", test1),
        ("Guard Check", test2),
        ("Check My Guard Info", test3),
        ("Health Check", test4)
    ]
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = f"{GREEN}PASSED{RESET}" if result else f"{RED}FAILED{RESET}"
        print(f"  {name:<35} {status}")
    
    print(f"\n{BLUE}Results: {passed}/{total} tests passed{RESET}")
    
    if passed == total:
        print(f"\n{GREEN}✓ All tests passed!{RESET}\n")
        return 0
    else:
        print(f"\n{RED}✗ Some tests failed!{RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())