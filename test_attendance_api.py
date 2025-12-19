#!/usr/bin/env python3
"""
Attendance API Test Script
Tests the attendance endpoints
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:8000/BURHANI_GUARDS_API_TEST/api"
TEST_ITS_ID = "10001001"
TEST_PASSWORD = "5678"

# Test data - UPDATE THESE WITH ACTUAL VALUES
TEST_ATTENDANCE_DATA = {
    "form_name": "ATTENDANCE_FORM",
    "user_id": 3,
    "its_id": 10001002,
    "miqaat_id": 17,
    "team_id": 2
}

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


def test_attendance_insert(token):
    """Test AttendanceInsert endpoint"""
    print_header("Step 2: Test Attendance Insert")
    
    try:
        print_info("Calling AttendanceInsert")
        print_info(f"Payload: {json.dumps(TEST_ATTENDANCE_DATA, indent=2)}")
        
        response = requests.post(
            f"{BASE_URL}/Attendance/AttendanceInsert",
            json=TEST_ATTENDANCE_DATA,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n{YELLOW}Response:{RESET}")
            print(json.dumps(data, indent=2))
            
            result = data.get("result")
            
            if result == 1:
                print_success("Attendance record inserted successfully!")
                return True
            elif result == 4:
                print_success("Duplicate detected (expected if running test multiple times)")
                print_info(f"Message: {data.get('message')}")
                return True
            else:
                print_error(f"Insert failed with result: {result}")
                print_error(f"Message: {data.get('message')}")
                return False
        else:
            print_error(f"Request failed with status {response.status_code}")
            print(response.text)
            return False
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_insert_my_attendance(token):
    """Test InsertMyAttendance endpoint"""
    print_header("Step 3: Test Insert My Attendance (Convenience Endpoint)")
    
    try:
        print_info("Calling InsertMyAttendance (uses ITS ID and Team ID from token)")
        
        payload = {
            "form_name": "ATTENDANCE_FORM",
            "miqaat_id": 17
        }
        
        print_info(f"Payload: {json.dumps(payload, indent=2)}")
        
        # Note: This endpoint uses query parameters
        response = requests.post(
            f"{BASE_URL}/Attendance/InsertMyAttendance",
            params=payload,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n{YELLOW}Response:{RESET}")
            print(json.dumps(data, indent=2))
            
            result = data.get("result")
            
            if result == 1:
                print_success("My attendance inserted successfully!")
                return True
            elif result == 4:
                print_success("Duplicate detected (expected if already marked)")
                print_info(f"Message: {data.get('message')}")
                return True
            else:
                print_error(f"Insert failed with result: {result}")
                print_error(f"Message: {data.get('message')}")
                return False
        else:
            print_error(f"Request failed with status {response.status_code}")
            print(response.text)
            return False
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_duplicate_detection(token):
    """Test duplicate detection by inserting same record twice"""
    print_header("Step 4: Test Duplicate Detection")
    
    try:
        print_info("Attempting to insert the same attendance record again")
        print_info("This should return result=4 (duplicate)")
        
        response = requests.post(
            f"{BASE_URL}/Attendance/AttendanceInsert",
            json=TEST_ATTENDANCE_DATA,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n{YELLOW}Response:{RESET}")
            print(json.dumps(data, indent=2))
            
            result = data.get("result")
            
            if result == 4:
                print_success("Duplicate detection working correctly!")
                print_info(f"Message: {data.get('message')}")
                return True
            elif result == 1:
                print_error("Expected duplicate (result=4) but got success (result=1)")
                print_error("This might indicate an issue with duplicate detection")
                return False
            else:
                print_error(f"Unexpected result: {result}")
                return False
        else:
            print_error(f"Request failed with status {response.status_code}")
            return False
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_health():
    """Test attendance health endpoint"""
    print_header("Step 5: Test Attendance Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/Attendance/health")
        
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
    print(f"{'Attendance API Test Suite':^70}")
    print(f"{'='*70}{RESET}\n")
    
    print_info(f"Base URL: {BASE_URL}")
    print_info(f"Test ITS ID: {TEST_ITS_ID}")
    print_info(f"Test Attendance Data:")
    print(f"  {json.dumps(TEST_ATTENDANCE_DATA, indent=2)}\n")
    
    # Step 1: Login
    token = login_and_get_token()
    if not token:
        print_error("\n❌ Cannot proceed without authentication token")
        return 1
    
    # Step 2: Test attendance insert
    test1 = test_attendance_insert(token)
    
    # Step 3: Test insert my attendance
    test2 = test_insert_my_attendance(token)
    
    # Step 4: Test duplicate detection
    test3 = test_duplicate_detection(token)
    
    # Step 5: Test health
    test4 = test_health()
    
    # Summary
    print_header("TEST SUMMARY")
    
    results = [
        ("Login", token is not None),
        ("Attendance Insert", test1),
        ("Insert My Attendance", test2),
        ("Duplicate Detection", test3),
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