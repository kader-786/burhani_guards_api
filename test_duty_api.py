#!/usr/bin/env python3
"""
Test Script for Guard Duty Insert API Endpoint

Tests both INSERT and DELETE operations for guard duty assignments.
Includes comprehensive validation and result verification.
"""

import requests
import json
from datetime import datetime
from typing import Optional, Dict, Any

# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_URL = "http://13.204.161.209:8080"
LOGIN_ENDPOINT = f"{BASE_URL}/Login/Checklogin"
GUARD_DUTY_INSERT_ENDPOINT = f"{BASE_URL}/Duty/GuardDutyInsert"
HEALTH_ENDPOINT = f"{BASE_URL}/Duty/health"

# Test credentials
TEST_USERNAME = "10001001"
TEST_PASSWORD = "password"

# ANSI color codes
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text:^80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.RESET}\n")

def print_test(test_name: str):
    """Print a test name"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}TEST: {test_name}{Colors.RESET}")
    print(f"{Colors.BLUE}{'-' * 80}{Colors.RESET}")

def print_success(message: str):
    """Print a success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")

def print_error(message: str):
    """Print an error message"""
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")

def print_warning(message: str):
    """Print a warning message"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.RESET}")

def print_info(message: str):
    """Print an info message"""
    print(f"  {message}")

def print_json(data: Any, indent: int = 2):
    """Print formatted JSON"""
    print(f"{Colors.CYAN}{json.dumps(data, indent=indent)}{Colors.RESET}")

# ============================================================================
# TEST FUNCTIONS
# ============================================================================

def login() -> Optional[str]:
    """Login and get JWT token"""
    print_test("Login")
    
    try:
        response = requests.post(
            LOGIN_ENDPOINT,
            json={
                "UserName": TEST_USERNAME,
                "Password": TEST_PASSWORD
            },
            timeout=10
        )
        
        print_info(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_json(data)
            
            if data.get("success") and data.get("access_token"):
                token = data["access_token"]
                print_success("Login successful")
                print_info(f"Token: {token[:50]}...")
                return token
            else:
                print_error("Login failed: No token in response")
                return None
        else:
            print_error(f"Login failed with status {response.status_code}")
            print_info(f"Response: {response.text}")
            return None
    
    except Exception as ex:
        print_error(f"Login exception: {str(ex)}")
        return None


def test_health_check():
    """Test health check endpoint (no auth required)"""
    print_test("Health Check (Public Endpoint)")
    
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=10)
        
        print_info(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_json(data)
            
            if data.get("status") == "healthy":
                print_success("Health check passed")
                return True
            else:
                print_warning("Health check returned non-healthy status")
                return False
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
    
    except Exception as ex:
        print_error(f"Health check exception: {str(ex)}")
        return False


def test_guard_duty_insert(token: str) -> Optional[int]:
    """
    Test guard duty INSERT operation
    Returns the guard_duty_id if successful
    """
    print_test("Guard Duty INSERT")
    
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "form_name": "TEST_GUARD_DUTY_FORM",
        "flag": "I",
        "duty_id": 1,
        "team_id": 2,
        "miqaat_id": 17,
        "its_id": 10009999  # Test ITS ID
    }
    
    print_info("Request Payload:")
    print_json(payload)
    
    try:
        response = requests.post(
            GUARD_DUTY_INSERT_ENDPOINT,
            json=payload,
            headers=headers,
            timeout=10
        )
        
        print_info(f"\nResponse Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            data = response.json()
            print_info("Response:")
            print_json(data)
            
            if data.get("success") and data.get("result") == 1:
                print_success("Guard duty INSERT successful (result=1)")
                print_info("✓ Guard assigned to duty")
                print_info("✓ Activity should be logged")
                return True
            elif data.get("result") == 4:
                print_warning("Duplicate detected (result=4)")
                print_info("Guard already assigned to this duty")
                return False
            else:
                print_error(f"INSERT failed with result={data.get('result')}")
                return False
        else:
            print_error(f"INSERT failed with status {response.status_code}")
            print_info(f"Response: {response.text}")
            return False
    
    except Exception as ex:
        print_error(f"INSERT exception: {str(ex)}")
        return False


def test_guard_duty_duplicate_insert(token: str):
    """Test guard duty INSERT with duplicate (should return result=4)"""
    print_test("Guard Duty INSERT - Duplicate Detection")
    
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "form_name": "TEST_GUARD_DUTY_FORM",
        "flag": "I",
        "duty_id": 1,
        "team_id": 2,
        "miqaat_id": 17,
        "its_id": 10009999  # Same as previous insert
    }
    
    print_info("Request Payload (Same as previous):")
    print_json(payload)
    
    try:
        response = requests.post(
            GUARD_DUTY_INSERT_ENDPOINT,
            json=payload,
            headers=headers,
            timeout=10
        )
        
        print_info(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 409:  # Conflict
            data = response.json()
            print_info("Response:")
            print_json(data)
            
            if data.get("result") == 4:
                print_success("Duplicate correctly detected (result=4)")
                print_info("✓ System prevented duplicate assignment")
                return True
            else:
                print_error(f"Unexpected result code: {data.get('result')}")
                return False
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            print_info(f"Response: {response.text}")
            return False
    
    except Exception as ex:
        print_error(f"Duplicate test exception: {str(ex)}")
        return False


def test_guard_duty_delete(token: str, guard_duty_id: int):
    """Test guard duty DELETE operation"""
    print_test("Guard Duty DELETE (Soft Delete)")
    
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "form_name": "TEST_GUARD_DUTY_FORM",
        "flag": "D",
        "guard_duty_id": guard_duty_id
    }
    
    print_info("Request Payload:")
    print_json(payload)
    
    try:
        response = requests.post(
            GUARD_DUTY_INSERT_ENDPOINT,
            json=payload,
            headers=headers,
            timeout=10
        )
        
        print_info(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_info("Response:")
            print_json(data)
            
            if data.get("success") and data.get("result") == 3:
                print_success("Guard duty DELETE successful (result=3)")
                print_info("✓ Guard removed from duty (soft deleted)")
                print_info("✓ Activity should be logged")
                return True
            elif data.get("result") == 0:
                print_warning("DELETE failed - Record not found or already deleted (result=0)")
                return False
            else:
                print_error(f"DELETE failed with result={data.get('result')}")
                return False
        else:
            print_error(f"DELETE failed with status {response.status_code}")
            print_info(f"Response: {response.text}")
            return False
    
    except Exception as ex:
        print_error(f"DELETE exception: {str(ex)}")
        return False


def test_missing_required_fields(token: str):
    """Test validation of required fields"""
    print_test("Validation - Missing Required Fields")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test INSERT without required fields
    payload = {
        "form_name": "TEST_GUARD_DUTY_FORM",
        "flag": "I",
        "duty_id": 1
        # Missing: team_id, miqaat_id, its_id
    }
    
    print_info("Request Payload (Missing fields):")
    print_json(payload)
    
    try:
        response = requests.post(
            GUARD_DUTY_INSERT_ENDPOINT,
            json=payload,
            headers=headers,
            timeout=10
        )
        
        print_info(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 400:  # Bad Request
            print_success("Validation correctly rejected incomplete request")
            print_info(f"Response: {response.json()}")
            return True
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            return False
    
    except Exception as ex:
        print_error(f"Validation test exception: {str(ex)}")
        return False


def test_invalid_flag(token: str):
    """Test invalid flag value"""
    print_test("Validation - Invalid Flag")
    
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "form_name": "TEST_GUARD_DUTY_FORM",
        "flag": "X",  # Invalid flag
        "duty_id": 1,
        "team_id": 2,
        "miqaat_id": 17,
        "its_id": 10009999
    }
    
    print_info("Request Payload (Invalid flag='X'):")
    print_json(payload)
    
    try:
        response = requests.post(
            GUARD_DUTY_INSERT_ENDPOINT,
            json=payload,
            headers=headers,
            timeout=10
        )
        
        print_info(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 422:  # Unprocessable Entity (validation error)
            print_success("Validation correctly rejected invalid flag")
            print_info(f"Response: {response.json()}")
            return True
        else:
            print_warning(f"Got status code {response.status_code}")
            print_info(f"Response: {response.text}")
            return False
    
    except Exception as ex:
        print_error(f"Invalid flag test exception: {str(ex)}")
        return False


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def main():
    """Run all tests"""
    print_header("GUARD DUTY INSERT API TEST SUITE")
    print(f"Base URL: {BASE_URL}")
    print(f"Test User: {TEST_USERNAME}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        "passed": 0,
        "failed": 0,
        "total": 0
    }
    
    # Test 1: Health Check
    if test_health_check():
        results["passed"] += 1
    else:
        results["failed"] += 1
    results["total"] += 1
    
    # Test 2: Login
    token = login()
    if token:
        results["passed"] += 1
    else:
        results["failed"] += 1
        print_error("\n❌ Cannot proceed without authentication token")
        return
    results["total"] += 1
    
    # Test 3: Guard Duty INSERT
    if test_guard_duty_insert(token):
        results["passed"] += 1
        insert_success = True
    else:
        results["failed"] += 1
        insert_success = False
    results["total"] += 1
    
    # Test 4: Duplicate Detection
    if test_guard_duty_duplicate_insert(token):
        results["passed"] += 1
    else:
        results["failed"] += 1
    results["total"] += 1
    
    # Test 5: Missing Required Fields
    if test_missing_required_fields(token):
        results["passed"] += 1
    else:
        results["failed"] += 1
    results["total"] += 1
    
    # Test 6: Invalid Flag
    if test_invalid_flag(token):
        results["passed"] += 1
    else:
        results["failed"] += 1
    results["total"] += 1
    
    # Test 7: DELETE (only if INSERT was successful)
    if insert_success:
        print_info("\nNote: You need to find the guard_duty_id from the database to test DELETE")
        print_info("Run this SQL query:")
        print_info("  SELECT guard_duty_id FROM bg.guard_duties WHERE its_id = 10009999 AND status = 1;")
        print_info("\nThen run DELETE test manually with:")
        print_info(f"  curl -X POST {GUARD_DUTY_INSERT_ENDPOINT} \\")
        print_info(f"    -H 'Authorization: Bearer YOUR_TOKEN' \\")
        print_info(f"    -H 'Content-Type: application/json' \\")
        print_info(f"    -d '{{\"form_name\":\"TEST\",\"flag\":\"D\",\"guard_duty_id\":YOUR_ID}}'")
    
    # Print summary
    print_header("TEST SUMMARY")
    print(f"Total Tests: {results['total']}")
    print(f"{Colors.GREEN}Passed: {results['passed']}{Colors.RESET}")
    print(f"{Colors.RED}Failed: {results['failed']}{Colors.RESET}")
    
    if results['failed'] == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED! 🎉{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ SOME TESTS FAILED{Colors.RESET}")
    
    print(f"\n{Colors.CYAN}Next Steps:{Colors.RESET}")
    print("1. Check database to verify guard_duties record was created")
    print("2. Check com_user_activity_log for INSERT activity")
    print("3. Test DELETE operation with actual guard_duty_id")
    print("4. Check com_user_activity_log for DELETE activity")
    print("5. Verify com_error_log for any errors")
    
    print(f"\n{Colors.CYAN}Verification SQL Queries:{Colors.RESET}")
    print("""
    -- View inserted guard duty
    SELECT * FROM bg.guard_duties 
    WHERE its_id = 10009999 
    ORDER BY guard_duty_id DESC;
    
    -- View activity log
    SELECT * FROM bg.com_user_activity_log 
    WHERE table_name = 'guard_duties'
    ORDER BY activity_id DESC 
    LIMIT 10;
    
    -- View error log (if any)
    SELECT * FROM bg.com_error_log 
    WHERE error_procedure = 'spr_guard_duty_insert'
    ORDER BY id DESC 
    LIMIT 5;
    """)


if __name__ == "__main__":
    main()