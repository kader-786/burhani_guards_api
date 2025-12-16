#!/usr/bin/env python3
"""
Team API Test Script
Tests the team endpoints
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:8000/BURHANI_GUARDS_API_TEST/api"
TEST_ITS_ID = "10001001"
TEST_PASSWORD = "5678"
TEST_TEAM_ID = 2  # Update with actual team ID

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
                print_info(f"Team ID: {data['data']['team_id']}")
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


def test_view_team(token):
    """Test ViewTeam endpoint"""
    print_header("Step 2: Test View Team")
    
    try:
        print_info(f"Calling ViewTeam for team_id: {TEST_TEAM_ID}")
        
        response = requests.post(
            f"{BASE_URL}/Team/ViewTeam",
            json={"team_id": TEST_TEAM_ID},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n{YELLOW}Response:{RESET}")
            print(json.dumps(data, indent=2))
            
            if data.get("success"):
                print_success("Team members retrieved successfully!")
                
                # Display summary
                members = data.get("data", [])
                if members:
                    print_info(f"\nFound {len(members)} team member(s):")
                    for member in members[:5]:  # Show first 5
                        print(f"  • {member.get('full_name')} ({member.get('its_id')}) - {member.get('position_name')}")
                    if len(members) > 5:
                        print(f"  ... and {len(members) - 5} more")
                else:
                    print_info("No team members found")
                
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


def test_view_my_team(token):
    """Test ViewMyTeam endpoint"""
    print_header("Step 3: Test View My Team (Convenience Endpoint)")
    
    try:
        print_info("Calling ViewMyTeam (uses team ID from token)")
        
        response = requests.get(
            f"{BASE_URL}/Team/ViewMyTeam",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n{YELLOW}Response:{RESET}")
            print(json.dumps(data, indent=2))
            
            if data.get("success"):
                print_success("My team members retrieved successfully!")
                
                # Display summary
                members = data.get("data", [])
                if members:
                    print_info(f"\nYour team has {len(members)} member(s):")
                    for member in members[:5]:  # Show first 5
                        print(f"  • {member.get('full_name')} - {member.get('position_name')}")
                    if len(members) > 5:
                        print(f"  ... and {len(members) - 5} more")
                else:
                    print_info("Your team has no members")
                
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
    """Test team health endpoint"""
    print_header("Step 4: Test Team Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/Team/health")
        
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
    print(f"{'Team API Test Suite':^70}")
    print(f"{'='*70}{RESET}\n")
    
    print_info(f"Base URL: {BASE_URL}")
    print_info(f"Test ITS ID: {TEST_ITS_ID}")
    print_info(f"Test Team ID: {TEST_TEAM_ID}\n")
    
    # Step 1: Login
    token = login_and_get_token()
    if not token:
        print_error("\n❌ Cannot proceed without authentication token")
        return 1
    
    # Step 2: Test view team
    test1 = test_view_team(token)
    
    # Step 3: Test view my team
    test2 = test_view_my_team(token)
    
    # Step 4: Test health
    test3 = test_health()
    
    # Summary
    print_header("TEST SUMMARY")
    
    results = [
        ("Login", token is not None),
        ("View Team", test1),
        ("View My Team", test2),
        ("Health Check", test3)
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

