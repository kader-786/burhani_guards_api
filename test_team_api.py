#!/usr/bin/env python3
"""
Team API Test Script - Updated with all endpoints
Tests all team endpoints
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
                print_success("Login successful!")
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
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_success("Team members retrieved!")
                members = data.get("data", [])
                print_info(f"Found {len(members)} member(s)")
                return True
        
        print_error("ViewTeam failed")
        return False
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_get_all_teams(token):
    """Test GetAllTeams endpoint"""
    print_header("Step 3: Test Get All Teams")
    
    try:
        response = requests.get(
            f"{BASE_URL}/Team/GetAllTeams",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_success("All teams retrieved!")
                teams = data.get("data", [])
                print_info(f"Found {len(teams)} team(s)")
                return True
        
        print_error("GetAllTeams failed")
        return False
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_get_team_by_id(token):
    """Test GetTeamById endpoint"""
    print_header("Step 4: Test Get Team By ID")
    
    try:
        response = requests.post(
            f"{BASE_URL}/Team/GetTeamById",
            json={"team_id": TEST_TEAM_ID},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_success("Team details retrieved!")
                return True
        
        print_error("GetTeamById failed")
        return False
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_get_jamaats_by_team_id(token):
    """Test GetJamaatsByTeamId endpoint"""
    print_header("Step 5: Test Get Jamaats By Team ID")
    
    try:
        response = requests.post(
            f"{BASE_URL}/Team/GetJamaatsByTeamId",
            json={"team_id": TEST_TEAM_ID},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_success("Jamaats retrieved!")
                jamaats = data.get("data", [])
                print_info(f"Found {len(jamaats)} jamaat(s)")
                return True
        
        print_error("GetJamaatsByTeamId failed")
        return False
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_get_all_jamiaats(token):
    """Test GetAllJamiaats endpoint"""
    print_header("Step 6: Test Get All Jamiaats")
    
    try:
        response = requests.get(
            f"{BASE_URL}/Team/GetAllJamiaats",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_success("All jamiaats retrieved!")
                jamiaats = data.get("data", [])
                print_info(f"Found {len(jamiaats)} jamiaat(s)")
                return True
        
        print_error("GetAllJamiaats failed")
        return False
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_view_my_team(token):
    """Test ViewMyTeam endpoint"""
    print_header("Step 7: Test View My Team")
    
    try:
        response = requests.get(
            f"{BASE_URL}/Team/ViewMyTeam",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_success("My team members retrieved!")
                return True
        
        print_error("ViewMyTeam failed")
        return False
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_get_my_team_details(token):
    """Test GetMyTeamDetails endpoint"""
    print_header("Step 8: Test Get My Team Details")
    
    try:
        response = requests.get(
            f"{BASE_URL}/Team/GetMyTeamDetails",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_success("My team details retrieved!")
                return True
        
        print_error("GetMyTeamDetails failed")
        return False
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def main():
    print(f"\n{BLUE}{'='*70}")
    print(f"{'Team API Test Suite':^70}")
    print(f"{'='*70}{RESET}\n")
    
    # Login
    token = login_and_get_token()
    if not token:
        print_error("\n❌ Cannot proceed without authentication token")
        return 1
    
    # Run all tests
    results = [
        ("Login", token is not None),
        ("View Team", test_view_team(token)),
        ("Get All Teams", test_get_all_teams(token)),
        ("Get Team By ID", test_get_team_by_id(token)),
        ("Get Jamaats By Team ID", test_get_jamaats_by_team_id(token)),
        ("Get All Jamiaats", test_get_all_jamiaats(token)),
        ("View My Team", test_view_my_team(token)),
        ("Get My Team Details", test_get_my_team_details(token))
    ]
    
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