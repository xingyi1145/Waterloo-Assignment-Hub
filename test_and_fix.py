#!/usr/bin/env python3
"""
Comprehensive test script to diagnose and fix frontend-backend connection issues
"""

import requests
import subprocess
import time
import sys

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_section(title):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")

def test_backend():
    """Test backend connectivity"""
    print_section("Testing Backend")
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Health endpoint
    tests_total += 1
    print("1. Testing health endpoint...")
    try:
        response = requests.get('http://localhost:8000/api/health', timeout=2)
        if response.status_code == 200:
            print(f"   {Colors.GREEN}✓ Health check passed{Colors.END}")
            print(f"   Response: {response.json()}")
            tests_passed += 1
        else:
            print(f"   {Colors.RED}✗ Health check failed: {response.status_code}{Colors.END}")
    except Exception as e:
        print(f"   {Colors.RED}✗ Cannot connect to backend: {e}{Colors.END}")
        print(f"   {Colors.YELLOW}→ Make sure backend is running on port 8000{Colors.END}")
    
    # Test 2: CORS headers
    tests_total += 1
    print("\n2. Testing CORS configuration...")
    try:
        response = requests.options(
            'http://localhost:8000/api/auth/login',
            headers={
                'Origin': 'http://localhost:5173',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'content-type,authorization'
            },
            timeout=2
        )
        cors_origin = response.headers.get('access-control-allow-origin')
        if cors_origin == 'http://localhost:5173':
            print(f"   {Colors.GREEN}✓ CORS configured correctly{Colors.END}")
            print(f"   Allow-Origin: {cors_origin}")
            tests_passed += 1
        else:
            print(f"   {Colors.RED}✗ CORS not configured for frontend{Colors.END}")
            print(f"   Expected: http://localhost:5173, Got: {cors_origin}")
    except Exception as e:
        print(f"   {Colors.RED}✗ CORS test failed: {e}{Colors.END}")
    
    # Test 3: Login endpoint
    tests_total += 1
    print("\n3. Testing login endpoint...")
    try:
        response = requests.post(
            'http://localhost:8000/api/auth/login',
            headers={'Content-Type': 'application/json'},
            json={'username': 'alice', 'password': 'password123'},
            timeout=2
        )
        if response.status_code == 200:
            data = response.json()
            if 'access_token' in data and 'user' in data:
                print(f"   {Colors.GREEN}✓ Login working correctly{Colors.END}")
                print(f"   User: {data['user']['username']}")
                tests_passed += 1
                return data['access_token']  # Return token for further tests
            else:
                print(f"   {Colors.RED}✗ Login response missing required fields{Colors.END}")
        else:
            print(f"   {Colors.RED}✗ Login failed: {response.status_code}{Colors.END}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   {Colors.RED}✗ Login test failed: {e}{Colors.END}")
    
    # Test 4: Authenticated endpoint
    tests_total += 1
    print("\n4. Testing authenticated endpoint...")
    if tests_passed >= 3:
        token = test_backend.last_token if hasattr(test_backend, 'last_token') else None
        if token:
            try:
                response = requests.get(
                    'http://localhost:8000/api/courses/',
                    headers={'Authorization': f'Bearer {token}'},
                    timeout=2
                )
                if response.status_code == 200:
                    courses = response.json()
                    print(f"   {Colors.GREEN}✓ Authenticated requests working{Colors.END}")
                    print(f"   Found {len(courses)} courses")
                    tests_passed += 1
                else:
                    print(f"   {Colors.RED}✗ Authenticated request failed: {response.status_code}{Colors.END}")
            except Exception as e:
                print(f"   {Colors.RED}✗ Authenticated test failed: {e}{Colors.END}")
    else:
        print(f"   {Colors.YELLOW}⊘ Skipped (previous tests failed){Colors.END}")
    
    print(f"\n{Colors.BOLD}Backend Tests: {tests_passed}/{tests_total} passed{Colors.END}")
    return tests_passed == tests_total

def test_frontend():
    """Test frontend connectivity"""
    print_section("Testing Frontend")
    
    tests_passed = 0
    tests_total = 2
    
    # Test 1: Frontend server
    print("1. Testing frontend server...")
    try:
        response = requests.get('http://localhost:5173/', timeout=2)
        if response.status_code == 200 and 'html' in response.text.lower():
            print(f"   {Colors.GREEN}✓ Frontend is serving{Colors.END}")
            tests_passed += 1
        else:
            print(f"   {Colors.RED}✗ Frontend returned unexpected response{Colors.END}")
    except Exception as e:
        print(f"   {Colors.RED}✗ Cannot connect to frontend: {e}{Colors.END}")
        print(f"   {Colors.YELLOW}→ Make sure frontend is running on port 5173{Colors.END}")
    
    # Test 2: Static assets
    print("\n2. Testing frontend assets...")
    try:
        response = requests.get('http://localhost:5173/@vite/client', timeout=2)
        if response.status_code == 200:
            print(f"   {Colors.GREEN}✓ Vite dev server working{Colors.END}")
            tests_passed += 1
        else:
            print(f"   {Colors.YELLOW}⚠ Vite client endpoint returned {response.status_code}{Colors.END}")
    except Exception as e:
        print(f"   {Colors.RED}✗ Asset test failed: {e}{Colors.END}")
    
    print(f"\n{Colors.BOLD}Frontend Tests: {tests_passed}/{tests_total} passed{Colors.END}")
    return tests_passed == tests_total

def check_common_issues():
    """Check for common configuration issues"""
    print_section("Checking Common Issues")
    
    issues_found = []
    
    # Check 1: API base URL in frontend
    print("1. Checking API configuration...")
    try:
        with open('src/frontend/src/api.ts', 'r') as f:
            content = f.read()
            if 'localhost:8000' in content:
                print(f"   {Colors.GREEN}✓ API base URL correct{Colors.END}")
            else:
                print(f"   {Colors.RED}✗ API base URL not set to localhost:8000{Colors.END}")
                issues_found.append("API base URL misconfigured")
    except Exception as e:
        print(f"   {Colors.RED}✗ Cannot read api.ts: {e}{Colors.END}")
        issues_found.append("Cannot read API configuration")
    
    # Check 2: CORS in backend
    print("\n2. Checking CORS configuration...")
    try:
        with open('src/backend/main.py', 'r') as f:
            content = f.read()
            if 'localhost:5173' in content:
                print(f"   {Colors.GREEN}✓ CORS allows frontend origin{Colors.END}")
            else:
                print(f"   {Colors.RED}✗ CORS not configured for localhost:5173{Colors.END}")
                issues_found.append("CORS misconfigured")
    except Exception as e:
        print(f"   {Colors.RED}✗ Cannot read main.py: {e}{Colors.END}")
        issues_found.append("Cannot read backend configuration")
    
    # Check 3: Database
    print("\n3. Checking database...")
    try:
        result = subprocess.run(
            ['sqlite3', 'wcah.db', 'SELECT COUNT(*) FROM users'],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            count = int(result.stdout.strip())
            print(f"   {Colors.GREEN}✓ Database has {count} users{Colors.END}")
        else:
            print(f"   {Colors.RED}✗ Database query failed{Colors.END}")
            issues_found.append("Database issue")
    except Exception as e:
        print(f"   {Colors.RED}✗ Cannot check database: {e}{Colors.END}")
        issues_found.append("Cannot access database")
    
    if issues_found:
        print(f"\n{Colors.RED}Found {len(issues_found)} issue(s):{Colors.END}")
        for issue in issues_found:
            print(f"  • {issue}")
    else:
        print(f"\n{Colors.GREEN}No configuration issues found!{Colors.END}")
    
    return len(issues_found) == 0

def provide_diagnosis():
    """Provide diagnosis and recommendations"""
    print_section("Diagnosis & Recommendations")
    
    print(f"{Colors.BOLD}If you're seeing 'Cannot connect to server':{Colors.END}\n")
    
    print("1. {Colors.YELLOW}Timing Issue:{Colors.END}")
    print("   • The frontend loads before backend is ready")
    print("   • Wait a few seconds after starting, then refresh the page")
    print("   • The start.py script should wait for backend health check")
    
    print("\n2. {Colors.YELLOW}Old Token Issue:{Colors.END}")
    print("   • An expired token is in localStorage")
    print("   • Open browser console (F12) and run:")
    print("     localStorage.clear()")
    print("   • Then refresh the page")
    
    print("\n3. {Colors.YELLOW}Port Conflicts:{Colors.END}")
    print("   • Backend port 8000 or frontend port 5173 already in use")
    print("   • Kill existing processes:")
    print("     pkill -f uvicorn")
    print("     pkill -f vite")
    
    print("\n4. {Colors.YELLOW}Browser Cache:{Colors.END}")
    print("   • Hard refresh: Ctrl+Shift+R (Linux) or Cmd+Shift+R (Mac)")
    print("   • Or open in incognito/private window")
    
    print(f"\n{Colors.BOLD}Quick Fix Steps:{Colors.END}")
    print("1. Kill old processes: pkill -f uvicorn && pkill -f vite")
    print("2. Clear localStorage: Open browser console, run: localStorage.clear()")
    print("3. Start fresh: python3 start.py")
    print("4. Wait for 'Application Ready!' message")
    print("5. Open http://localhost:5173 in a new incognito tab")

def main():
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║          WCAH Diagnostic & Test Tool                              ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print(Colors.END)
    
    backend_ok = test_backend()
    frontend_ok = test_frontend()
    config_ok = check_common_issues()
    
    print_section("Summary")
    
    if backend_ok and frontend_ok and config_ok:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ All tests passed!{Colors.END}")
        print(f"\nYour application is configured correctly.")
        print(f"If you're still seeing connection errors in the browser:")
        print(f"  1. Clear browser cache and localStorage")
        print(f"  2. Open in incognito window")
        print(f"  3. Check browser console (F12) for detailed error messages")
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ Some tests failed{Colors.END}")
        print(f"\nTest Results:")
        print(f"  Backend:      {'✓ OK' if backend_ok else '✗ FAILED'}")
        print(f"  Frontend:     {'✓ OK' if frontend_ok else '✗ FAILED'}")
        print(f"  Configuration: {'✓ OK' if config_ok else '✗ ISSUES FOUND'}")
        
        if not backend_ok:
            print(f"\n{Colors.YELLOW}→ Backend not responding. Start it with:{Colors.END}")
            print(f"  source .venv/bin/activate")
            print(f"  uvicorn src.backend.main:app --reload")
        
        if not frontend_ok:
            print(f"\n{Colors.YELLOW}→ Frontend not responding. Start it with:{Colors.END}")
            print(f"  cd src/frontend")
            print(f"  npm run dev")
    
    provide_diagnosis()

if __name__ == '__main__':
    main()
