#!/usr/bin/env python3
"""
Burhani Guards API Test Script
Tests the Login endpoints and validates responses
"""

import requests
import json
from typing import Dict, Any
import sys

# Configuration
BASE_URL = "http://13.204.161.209/BURHANI_GUARDS_API_TEST/api"
# For local testing, use: BASE_URL = "http://localhost:8000/BURHANI_GUARDS_API_TEST/api"

# Test credentials - UPDATE THESE WITH ACTUAL TEST CREDENTIALS
TEST_ITS_ID = "12345678"  # Replace with actual test ITS ID
TEST_PASSWORD = "password123"  # Replace with actual test password

# ANSI color codes for output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_test_header(test_name: str):
    """Print formatted test header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{test_name:^70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")


def print_success(message: str):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")


def print_error(message: str):
    """Print error message"""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")


def print_info(message: str):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")


def print_response(response: Dict[Any, Any]):
    """Print formatted JSON response"""
    print(f"{Colors.OKBLUE}Response:{Colors.ENDC}")
    print(json.dumps(response, indent=2, ensure_ascii=False))


def test_health_check():
    """Test the main health check endpoint"""
    print_test_header("Test 1: Main Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        
        print_info(f"URL: {BASE_URL}/health")
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_response(data)
            
            if data.get("status") == "healthy":
                print_success("Main health check passed!")
                return True
            else:
                print_error("Health check returned unhealthy status")
                return False
        else:
            print_error(f"Health check failed with status code: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print_error(f"Request failed: {str(e)}")
        return False


def test_login_health_check():
    """Test the login health check endpoint"""
    print_test_header("Test 2: Login Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/Login/health", timeout=10)
        
        print_info(f"URL: {BASE_URL}/Login/health")
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_response(data)
            
            if data.get("status") == "healthy" and data.get("database") == "PostgreSQL":
                print_success("Login health check passed!")
                return True
            else:
                print_error("Login health check returned unexpected status")
                return False
        else:
            print_error(f"Login health check failed with status code: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print_error(f"Request failed: {str(e)}")
        return False


def test_successful_login():
    """Test successful login with valid credentials"""
    print_test_header("Test 3: Successful Login")
    
    payload = {
        "username": TEST_ITS_ID,
        "password": TEST_PASSWORD
    }
    
    try:
        print_info(f"URL: {BASE_URL}/Login/CheckLogin")
        print_info(f"Request Payload:")
        print(json.dumps(payload, indent=2))
        
        response = requests.post(
            f"{BASE_URL}/Login/CheckLogin",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_response(data)
            
            if data.get("success") == True:
                print_success("Login successful!")
                
                # Validate response structure
                if "data" in data and data["data"]:
                    user_data = data["data"]
                    print_info("\nUser Data Validation:")
                    
                    required_fields = [
                        "its_id", "full_name", "email", "mobile",
                        "team_name", "position_name", "jamaat_name",
                        "jamiaat_name", "role_name", "access_rights"
                    ]
                    
                    all_fields_present = True
                    for field in required_fields:
                        if field in user_data:
                            print_success(f"  {field}: {user_data[field]}")
                        else:
                            print_error(f"  {field}: MISSING")
                            all_fields_present = False
                    
                    if all_fields_present:
                        print_success("\nAll required fields present!")
                        return True
                    else:
                        print_error("\nSome required fields are missing!")
                        return False
                else:
                    print_error("Response missing 'data' field")
                    return False
            else:
                print_error(f"Login failed: {data.get('message', 'Unknown error')}")
                return False
        else:
            print_error(f"Login request failed with status code: {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.RequestException as e:
        print_error(f"Request failed: {str(e)}")
        return False


def test_failed_login_wrong_password():
    """Test login with wrong password"""
    print_test_header("Test 4: Failed Login - Wrong Password")
    
    payload = {
        "username": TEST_ITS_ID,
        "password": "wrong_password_12345"
    }
    
    try:
        print_info(f"URL: {BASE_URL}/Login/CheckLogin")
        print_info(f"Testing with wrong password...")
        
        response = requests.post(
            f"{BASE_URL}/Login/CheckLogin",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_response(data)
            
            if data.get("success") == False:
                print_success("Correctly rejected wrong password!")
                return True
            else:
                print_error("Should have rejected wrong password!")
                return False
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print_error(f"Request failed: {str(e)}")
        return False


def test_failed_login_invalid_its_id():
    """Test login with invalid ITS ID"""
    print_test_header("Test 5: Failed Login - Invalid ITS ID")
    
    payload = {
        "username": "99999999",  # Non-existent ITS ID
        "password": "any_password"
    }
    
    try:
        print_info(f"URL: {BASE_URL}/Login/CheckLogin")
        print_info(f"Testing with invalid ITS ID...")
        
        response = requests.post(
            f"{BASE_URL}/Login/CheckLogin",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_response(data)
            
            if data.get("success") == False:
                print_success("Correctly rejected invalid ITS ID!")
                return True
            else:
                print_error("Should have rejected invalid ITS ID!")
                return False
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print_error(f"Request failed: {str(e)}")
        return False


def test_api_docs_available():
    """Test if API documentation is available"""
    print_test_header("Test 6: API Documentation")
    
    try:
        # Test Swagger UI
        response = requests.get(f"{BASE_URL}/docs", timeout=10)
        print_info(f"Swagger UI URL: {BASE_URL}/docs")
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print_success("Swagger UI is accessible!")
        else:
            print_error(f"Swagger UI not accessible: {response.status_code}")
        
        # Test ReDoc
        response = requests.get(f"{BASE_URL}/redoc", timeout=10)
        print_info(f"ReDoc URL: {BASE_URL}/redoc")
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print_success("ReDoc is accessible!")
            return True
        else:
            print_error(f"ReDoc not accessible: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print_error(f"Request failed: {str(e)}")
        return False


def run_all_tests():
    """Run all tests and print summary"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("╔" + "═" * 68 + "╗")
    print("║" + "  BURHANI GUARDS API TEST SUITE".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    print(f"{Colors.ENDC}")
    
    print_info(f"Base URL: {BASE_URL}")
    print_info(f"Test ITS ID: {TEST_ITS_ID}")
    print()
    
    tests = [
        ("Health Check", test_health_check),
        ("Login Health Check", test_login_health_check),
        ("Successful Login", test_successful_login),
        ("Failed Login - Wrong Password", test_failed_login_wrong_password),
        ("Failed Login - Invalid ITS ID", test_failed_login_invalid_its_id),
        ("API Documentation", test_api_docs_available),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Test crashed: {str(e)}")
            results.append((test_name, False))
    
    # Print summary
    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("╔" + "═" * 68 + "╗")
    print("║" + "  TEST SUMMARY".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    print(f"{Colors.ENDC}\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{Colors.OKGREEN}PASSED{Colors.ENDC}" if result else f"{Colors.FAIL}FAILED{Colors.ENDC}"
        print(f"  {test_name:<50} {status}")
    
    print(f"\n{Colors.BOLD}Results: {passed}/{total} tests passed{Colors.ENDC}")
    
    if passed == total:
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}✓ All tests passed!{Colors.ENDC}\n")
        return 0
    else:
        print(f"\n{Colors.FAIL}{Colors.BOLD}✗ {total - passed} test(s) failed!{Colors.ENDC}\n")
        return 1


if __name__ == "__main__":
    print(f"\n{Colors.WARNING}NOTE: Update TEST_ITS_ID and TEST_PASSWORD with actual test credentials{Colors.ENDC}\n")
    exit_code = run_all_tests()
    sys.exit(exit_code)
