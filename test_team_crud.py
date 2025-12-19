#!/usr/bin/env python3
"""
Team CRUD Operations Test Script
Tests INSERT, UPDATE, DELETE endpoints
"""

import requests
import json
import sys

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


def test_insert_team(token):
    """Test InsertTeam endpoint"""
    print_header("Step 2: Test Insert Team")
    
    try:
        payload = {
            "team_name": "Test Team Alpha",
            "jamiaat_id": 3,
            "jamaat_ids": [1, 3]
        }
        
        print_info(f"Inserting team: {payload['team_name']}")
        
        response = requests.post(
            f"{BASE_URL}/Team/InsertTeam",
            json=payload,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code in [200, 201]:
            data = response.json()
            print(f"\n{YELLOW}Response:{RESET}")
            print(json.dumps(data, indent=2))
            
            if data.get("success"):
                print_success("Team inserted successfully!")
                return True, data.get("data", {}).get("team_id")
            else:
                print_error(f"Insert failed: {data.get('message')}")
                return False, None
        else:
            print_error(f"Request failed with status {response.status_code}")
            return False, None
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False, None


def test_update_team(token, team_id):
    """Test UpdateTeam endpoint"""
    print_header("Step 3: Test Update Team")
    
    try:
        payload = {
            "team_id": team_id,
            "team_name": "Test Team Alpha Updated",
            "jamiaat_id": 3,
            "jamaat_ids": [1, 3, 5]
        }
        
        print_info(f"Updating team_id: {team_id}")
        
        response = requests.put(
            f"{BASE_URL}/Team/UpdateTeam",
            json=payload,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n{YELLOW}Response:{RESET}")
            print(json.dumps(data, indent=2))
            
            if data.get("success"):
                print_success("Team updated successfully!")
                return True
            else:
                print_error(f"Update failed: {data.get('message')}")
                return False
        else:
            print_error(f"Request failed with status {response.status_code}")
            return False
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_delete_team(token, team_id):
    """Test DeleteTeam endpoint"""
    print_header("Step 4: Test Delete Team")
    
    try:
        payload = {
            "team_id": team_id
        }
        
        print_info(f"Deleting team_id: {team_id}")
        
        response = requests.delete(
            f"{BASE_URL}/Team/DeleteTeam",
            json=payload,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n{YELLOW}Response:{RESET}")
            print(json.dumps(data, indent=2))
            
            if data.get("success"):
                print_success("Team deleted successfully!")
                return True
            else:
                print_error(f"Delete failed: {data.get('message')}")
                return False
        else:
            print_error(f"Request failed with status {response.status_code}")
            return False
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def main():
    print(f"\n{BLUE}{'='*70}")
    print(f"{'Team CRUD Operations Test Suite':^70}")
    print(f"{'='*70}{RESET}\n")
    
    # Login
    token = login_and_get_token()
    if not token:
        print_error("\n❌ Cannot proceed without authentication token")
        return 1
    
    # Test Insert
    insert_success, team_id = test_insert_team(token)
    
    # Test Update (only if insert succeeded)
    update_success = False
    if insert_success and team_id:
        update_success = test_update_team(token, team_id)
    
    # Test Delete (only if insert succeeded)
    delete_success = False
    if insert_success and team_id:
        delete_success = test_delete_team(token, team_id)
    
    # Summary
    print_header("TEST SUMMARY")
    
    results = [
        ("Login", token is not None),
        ("Insert Team", insert_success),
        ("Update Team", update_success),
        ("Delete Team", delete_success)
    ]
    
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