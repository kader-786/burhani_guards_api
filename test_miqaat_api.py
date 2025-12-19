#!/usr/bin/env python3
"""
Miqaat Master CRUD Test Script
Tests all Miqaat endpoints
"""

import requests
import json
import sys
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000/BURHANI_GUARDS_API_TEST/api"
TEST_ITS_ID = "10001001"
TEST_PASSWORD = "5678"

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
                print_success("Login successful!")
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


def test_get_all_miqaat(token):
    """Test GetAllMiqaat endpoint"""
    print_header("Step 2: Test Get All Miqaat")
    
    try:
        response = requests.get(
            f"{BASE_URL}/Miqaat/GetAllMiqaat",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n{YELLOW}Response:{RESET}")
            print(json.dumps(data, indent=2, default=str))
            
            if data.get("success"):
                print_success("All miqaats retrieved successfully!")
                miqaats = data.get("data", [])
                if miqaats:
                    print_info(f"Found {len(miqaats)} miqaat(s)")
                return True
            else:
                print_error(f"Query failed: {data.get('message')}")
                return False
        else:
            print_error(f"Request failed with status {response.status_code}")
            return False
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_get_all_miqaat_types(token):
    """Test GetAllMiqaatTypes endpoint"""
    print_header("Step 3: Test Get All Miqaat Types")
    
    try:
        response = requests.get(
            f"{BASE_URL}/Miqaat/GetAllMiqaatTypes",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n{YELLOW}Response:{RESET}")
            print(json.dumps(data, indent=2))
            
            if data.get("success"):
                print_success("Miqaat types retrieved successfully!")
                return True, data.get("data", [])
            else:
                print_error(f"Query failed: {data.get('message')}")
                return False, []
        else:
            print_error(f"Request failed with status {response.status_code}")
            return False, []
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False, []


def test_insert_miqaat(token):
    """Test InsertMiqaat endpoint"""
    print_header("Step 4: Test Insert Miqaat")
    
    try:
        # Prepare dates (tomorrow, 6 PM to 10 PM)
        tomorrow = datetime.now() + timedelta(days=1)
        start_date = tomorrow.replace(hour=18, minute=0, second=0, microsecond=0)
        end_date = tomorrow.replace(hour=22, minute=0, second=0, microsecond=0)
        
        payload = {
            "miqaat_name": "Test Miqaat API",
            "miqaat_type_id": 1,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "venue": "Test Venue",
            "jamaat_id": 1,
            "jamiaat_id": 3,
            "quantity": 50,
            "is_active": True
        }
        
        print_info(f"Inserting miqaat: {payload['miqaat_name']}")
        
        response = requests.post(
            f"{BASE_URL}/Miqaat/InsertMiqaat",
            json=payload,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code in [200, 201]:
            data = response.json()
            print(f"\n{YELLOW}Response:{RESET}")
            print(json.dumps(data, indent=2))
            
            if data.get("success"):
                print_success("Miqaat inserted successfully!")
                return True
            else:
                print_error(f"Insert failed: {data.get('message')}")
                return False
        else:
            print_error(f"Request failed with status {response.status_code}")
            return False
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def main():
    print(f"\n{BLUE}{'='*70}")
    print(f"{'Miqaat Master Test Suite':^70}")
    print(f"{'='*70}{RESET}\n")
    
    # Login
    token = login_and_get_token()
    if not token:
        print_error("\n❌ Cannot proceed without authentication token")
        return 1
    
    # Test endpoints
    results = []
    
    # 1. Get All Miqaat
    results.append(("Get All Miqaat", test_get_all_miqaat(token)))
    
    # 2. Get All Miqaat Types
    miqaat_types_success, _ = test_get_all_miqaat_types(token)
    results.append(("Get All Miqaat Types", miqaat_types_success))
    
    # 3. Insert Miqaat
    results.append(("Insert Miqaat", test_insert_miqaat(token)))
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = f"{GREEN}PASSED{RESET}" if result else f"{RED}FAILED{RESET}"
        print(f"  {name:<30} {status}")
    
    print(f"\n{BLUE}Results: {passed}/{total} tests passed{RESET}")
    
    if passed == total:
        print(f"\n{GREEN}✓ All tests passed!{RESET}\n")
        return 0
    else:
        print(f"\n{RED}✗ Some tests failed!{RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())