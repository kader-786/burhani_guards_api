#!/usr/bin/env python3
"""
Pre-flight Check Script
Verifies all requirements are met before starting the API
"""

import os
import sys
import subprocess
from pathlib import Path

# ANSI colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    print(f"\n{BOLD}{BLUE}{'=' * 60}{RESET}")
    print(f"{BOLD}{BLUE}{text:^60}{RESET}")
    print(f"{BOLD}{BLUE}{'=' * 60}{RESET}\n")

def print_check(message, success):
    symbol = f"{GREEN}✓{RESET}" if success else f"{RED}✗{RESET}"
    status = f"{GREEN}OK{RESET}" if success else f"{RED}FAILED{RESET}"
    print(f"{symbol} {message:<50} [{status}]")
    return success

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    version = sys.version_info
    is_ok = version.major == 3 and version.minor >= 8
    print_check(f"Python version ({version.major}.{version.minor}.{version.micro})", is_ok)
    if not is_ok:
        print(f"   {YELLOW}Required: Python 3.8 or higher{RESET}")
    return is_ok

def check_env_file():
    """Check if .env file exists"""
    env_path = Path(".env")
    exists = env_path.exists()
    print_check(".env file exists", exists)
    if not exists:
        print(f"   {YELLOW}Copy .env.example to .env and configure it{RESET}")
    return exists

def check_env_password():
    """Check if password is configured in .env"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        password = os.getenv("PG_PASSWORD", "")
        is_configured = password and password != "your_password_here" and password != "your_actual_password_here"
        print_check("Database password configured", is_configured)
        if not is_configured:
            print(f"   {YELLOW}Update PG_PASSWORD in .env file{RESET}")
        return is_configured
    except ImportError:
        print_check("python-dotenv installed", False)
        print(f"   {YELLOW}Run: pip install python-dotenv{RESET}")
        return False

def check_requirements():
    """Check if required packages are installed"""
    required = ["fastapi", "uvicorn", "psycopg2", "pydantic"]
    all_ok = True
    
    for package in required:
        try:
            __import__(package)
            print_check(f"Package: {package}", True)
        except ImportError:
            print_check(f"Package: {package}", False)
            all_ok = False
    
    if not all_ok:
        print(f"   {YELLOW}Run: pip install -r requirements.txt{RESET}")
    
    return all_ok

def check_database_connection():
    """Check if PostgreSQL database is accessible"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        import psycopg2
        
        conn_string = f"host={os.getenv('PG_HOST')} port={os.getenv('PG_PORT')} " \
                     f"dbname={os.getenv('PG_DATABASE')} user={os.getenv('PG_USER')} " \
                     f"password={os.getenv('PG_PASSWORD')}"
        
        conn = psycopg2.connect(conn_string)
        conn.close()
        
        print_check("Database connection", True)
        return True
    except Exception as e:
        print_check("Database connection", False)
        print(f"   {YELLOW}Error: {str(e)}{RESET}")
        return False

def check_login_function():
    """Check if com_spr_login_json function exists"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        import psycopg2
        
        conn_string = f"host={os.getenv('PG_HOST')} port={os.getenv('PG_PORT')} " \
                     f"dbname={os.getenv('PG_DATABASE')} user={os.getenv('PG_USER')} " \
                     f"password={os.getenv('PG_PASSWORD')}"
        
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT routine_name 
            FROM information_schema.routines 
            WHERE routine_schema = 'bg' 
            AND routine_name = 'com_spr_login_json'
        """)
        
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        exists = result is not None
        print_check("Login function (com_spr_login_json)", exists)
        
        if not exists:
            print(f"   {YELLOW}Deploy the login function first!{RESET}")
        
        return exists
    except Exception as e:
        print_check("Login function check", False)
        print(f"   {YELLOW}Could not verify: {str(e)}{RESET}")
        return False

def check_app_structure():
    """Check if app directory structure is correct"""
    required_files = [
        "app/__init__.py",
        "app/main.py",
        "app/config.py",
        "app/db.py",
        "app/models/login.py",
        "app/routers/Login_controller.py"
    ]
    
    all_ok = True
    for file_path in required_files:
        exists = Path(file_path).exists()
        if not exists:
            all_ok = False
        print_check(f"File: {file_path}", exists)
    
    return all_ok

def main():
    print_header("BURHANI GUARDS API - PRE-FLIGHT CHECK")
    
    checks = []
    
    # Basic checks
    print(f"\n{BOLD}Basic Requirements:{RESET}")
    checks.append(check_python_version())
    checks.append(check_env_file())
    checks.append(check_env_password())
    
    # Package checks
    print(f"\n{BOLD}Python Packages:{RESET}")
    checks.append(check_requirements())
    
    # File structure checks
    print(f"\n{BOLD}Application Structure:{RESET}")
    checks.append(check_app_structure())
    
    # Database checks
    print(f"\n{BOLD}Database Checks:{RESET}")
    checks.append(check_database_connection())
    checks.append(check_login_function())
    
    # Summary
    print_header("SUMMARY")
    
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print(f"{GREEN}{BOLD}✓ All checks passed! ({passed}/{total}){RESET}")
        print(f"\n{GREEN}You're ready to start the API!{RESET}")
        print(f"\nRun: {BOLD}./run.sh{RESET} to start the server\n")
        return 0
    else:
        failed = total - passed
        print(f"{RED}{BOLD}✗ {failed} check(s) failed ({passed}/{total} passed){RESET}")
        print(f"\n{YELLOW}Please fix the issues above before starting the API.{RESET}\n")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
