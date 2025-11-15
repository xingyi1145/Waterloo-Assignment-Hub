#!/usr/bin/env python3
"""
WCAH Application Launcher
Automatically starts backend and frontend servers
"""

import os
import sys
import subprocess
import time
import signal
import requests
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓{Colors.END} {text}")

def print_error(text):
    print(f"{Colors.RED}✗{Colors.END} {text}")

def print_info(text):
    print(f"{Colors.YELLOW}ℹ{Colors.END} {text}")

# Global process trackers
backend_process = None
frontend_process = None

def cleanup(signum=None, frame=None):
    """Cleanup function to kill processes on exit"""
    print_info("\nShutting down servers...")
    
    if backend_process:
        backend_process.terminate()
        try:
            backend_process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            backend_process.kill()
    
    if frontend_process:
        frontend_process.terminate()
        try:
            frontend_process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            frontend_process.kill()
    
    print_success("Servers stopped")
    sys.exit(0)

# Register cleanup handlers
signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def check_prerequisites():
    """Check if required tools are installed"""
    print_header("Checking Prerequisites")
    
    checks_passed = True
    
    # Check Python version
    python_version = sys.version_info
    if python_version >= (3, 8):
        print_success(f"Python {python_version.major}.{python_version.minor}")
    else:
        print_error(f"Python 3.8+ required (found {python_version.major}.{python_version.minor})")
        checks_passed = False
    
    # Check Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        version = result.stdout.strip()
        print_success(f"Node.js {version}")
    except FileNotFoundError:
        print_error("Node.js not found")
        checks_passed = False
    
    # Check npm
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        version = result.stdout.strip()
        print_success(f"npm {version}")
    except FileNotFoundError:
        print_error("npm not found")
        checks_passed = False
    
    return checks_passed

def check_database():
    """Check if database exists and has data"""
    print_header("Checking Database")
    
    if not os.path.exists('wcah.db'):
        print_error("Database not found")
        print_info("Creating and seeding database...")
        
        # Seed database
        try:
            result = subprocess.run(
                ['python3', 'scripts/seed_database.py'],
                input='yes\n',
                text=True,
                capture_output=True
            )
            if result.returncode == 0:
                print_success("Database created and seeded")
                return True
            else:
                print_error("Failed to seed database")
                print(result.stderr)
                return False
        except Exception as e:
            print_error(f"Error seeding database: {e}")
            return False
    else:
        # Check if database has data
        try:
            result = subprocess.run(
                ['sqlite3', 'wcah.db', 'SELECT COUNT(*) FROM users'],
                capture_output=True,
                text=True
            )
            count = int(result.stdout.strip())
            if count > 0:
                print_success(f"Database exists with {count} users")
                return True
            else:
                print_info("Database exists but is empty, seeding...")
                subprocess.run(
                    ['python3', 'scripts/seed_database.py'],
                    input='yes\n',
                    text=True
                )
                return True
        except:
            print_success("Database exists")
            return True

def check_venv():
    """Check if virtual environment exists and has dependencies"""
    print_header("Checking Python Environment")
    
    if not os.path.exists('.venv'):
        print_error("Virtual environment not found")
        print_info("Creating virtual environment...")
        subprocess.run(['python3', '-m', 'venv', '.venv'])
    
    print_success("Virtual environment exists")
    
    # Check if dependencies are installed
    pip_path = '.venv/bin/pip'
    try:
        result = subprocess.run(
            [pip_path, 'show', 'fastapi'],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print_info("Installing Python dependencies...")
            subprocess.run([pip_path, 'install', '-q', '-r', 'requirements.txt'])
            print_success("Dependencies installed")
        else:
            print_success("Dependencies installed")
    except:
        print_info("Installing Python dependencies...")
        subprocess.run([pip_path, 'install', '-q', '-r', 'requirements.txt'])

def check_frontend_deps():
    """Check if frontend dependencies are installed"""
    print_header("Checking Frontend Dependencies")
    
    frontend_path = Path('src/frontend')
    node_modules = frontend_path / 'node_modules'
    
    if not node_modules.exists():
        print_info("Installing frontend dependencies...")
        subprocess.run(
            ['npm', 'install', '--silent'],
            cwd=frontend_path,
            capture_output=True
        )
        print_success("Frontend dependencies installed")
    else:
        print_success("Frontend dependencies installed")

def wait_for_server(url, name, max_attempts=30):
    """Wait for a server to be ready"""
    print_info(f"Waiting for {name} to start...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(url, timeout=1)
            if response.status_code < 500:
                print_success(f"{name} is ready")
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.5)
    
    print_error(f"{name} failed to start")
    return False

def start_backend():
    """Start the backend server"""
    global backend_process
    
    print_header("Starting Backend Server")
    
    # Check if already running
    try:
        response = requests.get('http://localhost:8000/api/health', timeout=1)
        if response.status_code == 200:
            print_info("Backend already running")
            return True
    except:
        pass
    
    # Start backend
    uvicorn_path = '.venv/bin/uvicorn'
    backend_process = subprocess.Popen(
        [uvicorn_path, 'src.backend.main:app', '--host', '0.0.0.0', '--port', '8000'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for backend to be ready
    if wait_for_server('http://localhost:8000/api/health', 'Backend'):
        print_success("Backend started on http://localhost:8000")
        return True
    else:
        return False

def start_frontend():
    """Start the frontend server"""
    global frontend_process
    
    print_header("Starting Frontend Server")
    
    # Check if already running
    try:
        response = requests.get('http://localhost:5173/', timeout=1)
        if response.status_code == 200:
            print_info("Frontend already running")
            return True
    except:
        pass
    
    # Start frontend
    frontend_path = Path('src/frontend')
    frontend_process = subprocess.Popen(
        ['npm', 'run', 'dev'],
        cwd=frontend_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for frontend to be ready
    if wait_for_server('http://localhost:5173/', 'Frontend'):
        print_success("Frontend started on http://localhost:5173")
        return True
    else:
        return False

def print_access_info():
    """Print access information"""
    print_header("Application Ready!")
    
    print(f"{Colors.BOLD}Access URLs:{Colors.END}")
    print(f"  🌐 Frontend:  {Colors.GREEN}http://localhost:5173{Colors.END}")
    print(f"  🔧 Backend:   {Colors.GREEN}http://localhost:8000{Colors.END}")
    print(f"  📚 API Docs:  {Colors.GREEN}http://localhost:8000/docs{Colors.END}")
    print()
    print(f"{Colors.BOLD}Sample Accounts (password: password123):{Colors.END}")
    print(f"  👨‍🏫 Professor: {Colors.YELLOW}prof_smith{Colors.END}")
    print(f"  👨‍🎓 Student:   {Colors.YELLOW}alice{Colors.END}")
    print()
    print(f"{Colors.BOLD}Press Ctrl+C to stop all servers{Colors.END}\n")

def main():
    """Main function"""
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    print_header("WCAH Application Launcher")
    
    # Run checks
    if not check_prerequisites():
        print_error("\nPrerequisites check failed")
        sys.exit(1)
    
    check_venv()
    check_database()
    check_frontend_deps()
    
    # Start servers
    if not start_backend():
        print_error("Failed to start backend")
        cleanup()
        sys.exit(1)
    
    if not start_frontend():
        print_error("Failed to start frontend")
        cleanup()
        sys.exit(1)
    
    # Print access info
    print_access_info()
    
    # Keep the script running and monitor servers
    try:
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process and backend_process.poll() is not None:
                print_error("Backend process died")
                break
            
            if frontend_process and frontend_process.poll() is not None:
                print_error("Frontend process died")
                break
    
    except KeyboardInterrupt:
        pass
    
    cleanup()

if __name__ == '__main__':
    main()
