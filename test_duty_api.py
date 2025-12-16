#!/usr/bin/env python3
"""
Duty API Test Script
Tests the duty endpoints
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


def test_active_assigned_miqaat_duties(token):
    """Test GetActiveAssignedMiqaatDuties endpoint"""
    print_header("Step 2: Test Active Assigned Miqaat Duties")
    
    try:
        print_info(f"Calling GetActiveAssignedMiqaatDuties for team_id: {TEST_TEAM_ID}")
        
        response = requests.post(
            f"{BASE_URL}/Duty/GetActiveAssignedMiqaatDuties",
            json={"team_id": TEST_TEAM_ID},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n{YELLOW}Response:{RESET}")
            print(json.dumps(data, indent=2))
            
            if data.get("success"):
                print_success("Active assigned miqaat duties retrieved successfully!")
                
                # Display summary
                duties = data.get("data", [])
                if duties:
                    print_info(f"\nFound {len(duties)} active duty assignment(s):")
                    for duty in duties[:3]:  # Show first 3
                        print(f"  • {duty.get('miqaat_name')} - {duty.get('location')}")
                else:
                    print_info("No active duties found for this team")
                
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


def test_guard_duties_assigned(token):
    """Test GetGuardDutiesAssigned endpoint"""
    print_header("Step 3: Test Guard Duties Assigned")
    
    try:
        print_info(f"Calling GetGuardDutiesAssigned for its_id: {TEST_ITS_ID}")
        
        response = requests.post(
            f"{BASE_URL}/Duty/GetGuardDutiesAssigned",
            json={"its_id": int(TEST_ITS_ID)},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n{YELLOW}Response:{RESET}")
            print(json.dumps(data, indent=2))
            
            if data.get("success"):
                print_success("Guard duties retrieved successfully!")
                
                # Display summary
                duties = data.get("data", [])
                if duties:
                    print_info(f"\nFound {len(duties)} assigned duty/duties:")
                    for duty in duties[:3]:  # Show first 3
                        print(f"  • {duty.get('miqaat_name')} - {duty.get('location')}")
                else:
                    print_info("No guard duties found for this member")
                
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


def test_my_duties(token):
    """Test GetMyDuties endpoint"""
    print_header("Step 4: Test My Duties (Convenience Endpoint)")
    
    try:
        print_info("Calling GetMyDuties (uses ITS ID from token)")
        
        response = requests.get(
            f"{BASE_URL}/Duty/GetMyDuties",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n{YELLOW}Response:{RESET}")
            print(json.dumps(data, indent=2))
            
            if data.get("success"):
                print_success("My duties retrieved successfully!")
                
                # Display summary
                duties = data.get("data", [])
                if duties:
                    print_info(f"\nYou have {len(duties)} assigned duty/duties")
                else:
                    print_info("You have no duties assigned")
                
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


def test_my_team_duties(token):
    """Test GetMyTeamDuties endpoint"""
    print_header("Step 5: Test My Team Duties (Convenience Endpoint)")
    
    try:
        print_info("Calling GetMyTeamDuties (uses team ID from token)")
        
        response = requests.get(
            f"{BASE_URL}/Duty/GetMyTeamDuties",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n{YELLOW}Response:{RESET}")
            print(json.dumps(data, indent=2))
            
            if data.get("success"):
                print_success("My team duties retrieved successfully!")
                
                # Display summary
                duties = data.get("data", [])
                if duties:
                    print_info(f"\nYour team has {len(duties)} active duty assignment(s)")
                else:
                    print_info("Your team has no active duties")
                
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
    """Test duty health endpoint"""
    print_header("Step 6: Test Duty Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/Duty/health")
        
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
    print(f"{'Duty API Test Suite':^70}")
    print(f"{'='*70}{RESET}\n")
    
    print_info(f"Base URL: {BASE_URL}")
    print_info(f"Test ITS ID: {TEST_ITS_ID}")
    print_info(f"Test Team ID: {TEST_TEAM_ID}\n")
    
    # Step 1: Login
    token = login_and_get_token()
    if not token:
        print_error("\n❌ Cannot proceed without authentication token")
        return 1
    
    # Step 2: Test active assigned miqaat duties
    test1 = test_active_assigned_miqaat_duties(token)
    
    # Step 3: Test guard duties assigned
    test2 = test_guard_duties_assigned(token)
    
    # Step 4: Test my duties
    test3 = test_my_duties(token)
    
    # Step 5: Test my team duties
    test4 = test_my_team_duties(token)
    
    # Step 6: Test health
    test5 = test_health()
    
    # Summary
    print_header("TEST SUMMARY")
    
    results = [
        ("Login", token is not None),
        ("Active Assigned Miqaat Duties", test1),
        ("Guard Duties Assigned", test2),
        ("My Duties", test3),
        ("My Team Duties", test4),
        ("Health Check", test5)
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