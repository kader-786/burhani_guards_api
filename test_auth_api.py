#!/usr/bin/env python3
"""
JWT Authentication API Test Script
Tests the authentication endpoints and token functionality
"""

import requests
import json
from typing import Dict, Any
import sys
from datetime import datetime

# Configuration
# BASE_URL = "http://13.204.161.209/BURHANI_GUARDS_API_TEST/api"
# For local testing: 
BASE_URL = "http://localhost:8000/BURHANI_GUARDS_API_TEST/api"

# Test credentials - UPDATE WITH ACTUAL CREDENTIALS
TEST_ITS_ID = "10001001"
TEST_PASSWORD = "5678"

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(test_name):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*70}")
    print(f"{test_name:^70}")
    print(f"{'='*70}{Colors.RESET}\n")

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")

def print_info(message):
    print(f"{Colors.YELLOW}ℹ {message}{Colors.RESET}")

def print_json(data, title="Response"):
    print(f"\n{Colors.YELLOW}{title}:{Colors.RESET}")
    print(json.dumps(data, indent=2))

# Global variable to store tokens
tokens = {}

def test_login():
    """Test login endpoint and get JWT tokens"""
    print_header("Test 1: Login and Get JWT Tokens")
    
    payload = {
        "username": TEST_ITS_ID,
        "password": TEST_PASSWORD
    }
    
    try:
        print_info(f"POST {BASE_URL}/Login/CheckLogin")
        print_info(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            f"{BASE_URL}/Login/CheckLogin",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_json(data)
            
            if data.get("success"):
                print_success("Login successful!")
                
                # Validate token structure
                if "tokens" in data and data["tokens"]:
                    tokens_data = data["tokens"]
                    
                    # Store tokens globally
                    tokens["access_token"] = tokens_data.get("access_token")
                    tokens["refresh_token"] = tokens_data.get("refresh_token")
                    
                    print_success(f"Access Token: {tokens['access_token'][:50]}...")
                    print_success(f"Refresh Token: {tokens['refresh_token'][:50]}...")
                    print_success(f"Token Type: {tokens_data.get('token_type')}")
                    print_success(f"Expires In: {tokens_data.get('expires_in')} seconds")
                    
                    # Validate user data
                    if "data" in data and data["data"]:
                        user_data = data["data"]
                        print_info("\nUser Information:")
                        print_success(f"  ITS ID: {user_data.get('its_id')}")
                        print_success(f"  Name: {user_data.get('full_name')}")
                        print_success(f"  Team: {user_data.get('team_name')}")
                        print_success(f"  Role: {user_data.get('role_name')}")
                        print_success(f"  Is Admin: {user_data.get('is_admin')}")
                        print_success(f"  Access Rights: {user_data.get('access_rights')}")
                    
                    return True
                else:
                    print_error("Tokens missing from response")
                    return False
            else:
                print_error(f"Login failed: {data.get('message')}")
                return False
        else:
            print_error(f"HTTP Error: {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Exception: {str(e)}")
        return False


def test_get_current_user():
    """Test getting current user with access token"""
    print_header("Test 2: Get Current User (Protected Endpoint)")
    
    if not tokens.get("access_token"):
        print_error("No access token available. Run login test first.")
        return False
    
    try:
        headers = {
            "Authorization": f"Bearer {tokens['access_token']}",
            "Content-Type": "application/json"
        }
        
        print_info(f"GET {BASE_URL}/Login/Me")
        print_info(f"Authorization: Bearer {tokens['access_token'][:50]}...")
        
        response = requests.get(
            f"{BASE_URL}/Login/Me",
            headers=headers,
            timeout=10
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_json(data)
            
            if data.get("success"):
                print_success("Successfully retrieved user information!")
                
                # Validate user data from token
                if "data" in data:
                    print_info("\nUser Data from Token:")
                    user_data = data["data"]
                    print_success(f"  ITS ID: {user_data.get('its_id')}")
                    print_success(f"  Name: {user_data.get('full_name')}")
                    print_success(f"  Team ID: {user_data.get('team_id')}")
                    print_success(f"  Role ID: {user_data.get('role_id')}")
                
                return True
            else:
                print_error(f"Failed: {data.get('message')}")
                return False
        elif response.status_code == 401:
            print_error("Unauthorized - Token is invalid or expired")
            return False
        else:
            print_error(f"HTTP Error: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Exception: {str(e)}")
        return False


def test_refresh_token():
    """Test refreshing access token"""
    print_header("Test 3: Refresh Access Token")
    
    if not tokens.get("refresh_token"):
        print_error("No refresh token available. Run login test first.")
        return False
    
    try:
        payload = {
            "refresh_token": tokens["refresh_token"]
        }
        
        print_info(f"POST {BASE_URL}/Login/RefreshToken")
        print_info(f"Refresh Token: {tokens['refresh_token'][:50]}...")
        
        response = requests.post(
            f"{BASE_URL}/Login/RefreshToken",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_json(data)
            
            if data.get("success"):
                print_success("Token refreshed successfully!")
                
                if "tokens" in data and data["tokens"]:
                    new_tokens = data["tokens"]
                    
                    # Update global tokens
                    tokens["access_token"] = new_tokens.get("access_token")
                    tokens["refresh_token"] = new_tokens.get("refresh_token")
                    
                    print_success(f"New Access Token: {tokens['access_token'][:50]}...")
                    print_success(f"New Refresh Token: {tokens['refresh_token'][:50]}...")
                    print_success(f"Expires In: {new_tokens.get('expires_in')} seconds")
                    
                    return True
                else:
                    print_error("New tokens missing from response")
                    return False
            else:
                print_error(f"Refresh failed: {data.get('message')}")
                return False
        else:
            print_error(f"HTTP Error: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Exception: {str(e)}")
        return False


def test_invalid_token():
    """Test with invalid token"""
    print_header("Test 4: Invalid Token (Should Fail)")
    
    try:
        headers = {
            "Authorization": "Bearer invalid.token.here",
            "Content-Type": "application/json"
        }
        
        print_info(f"GET {BASE_URL}/Login/Me")
        print_info("Using invalid token...")
        
        response = requests.get(
            f"{BASE_URL}/Login/Me",
            headers=headers,
            timeout=10
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 401:
            print_success("Correctly rejected invalid token! (401 Unauthorized)")
            return True
        else:
            print_error(f"Expected 401, got {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Exception: {str(e)}")
        return False


def test_no_token():
    """Test protected endpoint without token"""
    print_header("Test 5: No Token (Should Fail)")
    
    try:
        print_info(f"GET {BASE_URL}/Login/Me")
        print_info("Without Authorization header...")
        
        response = requests.get(
            f"{BASE_URL}/Login/Me",
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 403:
            print_success("Correctly rejected request without token! (403 Forbidden)")
            return True
        else:
            print_error(f"Expected 403, got {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Exception: {str(e)}")
        return False


def test_failed_login():
    """Test login with wrong password"""
    print_header("Test 6: Failed Login (Wrong Password)")
    
    payload = {
        "username": TEST_ITS_ID,
        "password": "wrong_password_123"
    }
    
    try:
        print_info(f"POST {BASE_URL}/Login/CheckLogin")
        print_info("Using wrong password...")
        
        response = requests.post(
            f"{BASE_URL}/Login/CheckLogin",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if not data.get("success"):
                print_success(f"Correctly rejected wrong password!")
                print_info(f"Message: {data.get('message')}")
                return True
            else:
                print_error("Should have rejected wrong password!")
                return False
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Exception: {str(e)}")
        return False


def run_all_tests():
    """Run all authentication tests"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔" + "═" * 68 + "╗")
    print("║" + " JWT Authentication Test Suite ".center(68) + "║")
    print("║" + f" {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    print(f"{Colors.RESET}")
    
    print_info(f"Base URL: {BASE_URL}")
    print_info(f"Test ITS ID: {TEST_ITS_ID}")
    print()
    
    tests = [
        ("Login and Get JWT Tokens", test_login),
        ("Get Current User (Protected)", test_get_current_user),
        ("Refresh Access Token", test_refresh_token),
        ("Invalid Token (Should Fail)", test_invalid_token),
        ("No Token (Should Fail)", test_no_token),
        ("Failed Login (Wrong Password)", test_failed_login),
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
    print_header("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{Colors.GREEN}PASSED{Colors.RESET}" if result else f"{Colors.RED}FAILED{Colors.RESET}"
        print(f"  {test_name:<50} {status}")
    
    print(f"\n{Colors.BOLD}Results: {passed}/{total} tests passed{Colors.RESET}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ All tests passed!{Colors.RESET}\n")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ {total - passed} test(s) failed!{Colors.RESET}\n")
        return 1


if __name__ == "__main__":
    print(f"\n{Colors.YELLOW}NOTE: Update TEST_ITS_ID and TEST_PASSWORD with actual credentials{Colors.RESET}\n")
    exit_code = run_all_tests()
    sys.exit(exit_code)