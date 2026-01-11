#!/usr/bin/env python3
"""
Startup script for Waterloo CS Study Note Hub
This script will:
1. Stop any running servers
2. Clean up old processes and files
3. Rebuild frontend
4. Restart everything fresh
"""

import subprocess
import os
import sys
import time

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_step(step_num, title):
    print(f"\n{Colors.BOLD}{Colors.BLUE}[Step {step_num}] {title}{Colors.END}")

def run_command(cmd, description, ignore_errors=False):
    """Run a command and display the result"""
    print(f"  → {description}...", end=" ")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 or ignore_errors:
            print(f"{Colors.GREEN}✓{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}✗{Colors.END}")
            if result.stderr:
                print(f"    Error: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"{Colors.RED}✗{Colors.END}")
        print(f"    Error: {e}")
        return False

def main():
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print(f"  {Colors.BOLD}SE-StudyCenter - Startup Script                             ║")
    print(f"║         Starting Backend and Frontend Services                  ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print(Colors.END)
    
    # Change to project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    print_step(1, "Stopping existing servers")
    run_command("pkill -f 'uvicorn.*8000'", "Stopping backend", ignore_errors=True)
    run_command("pkill -f 'vite'", "Stopping frontend", ignore_errors=True)
    time.sleep(2)
    
    print_step(2, "Cleaning up processes")
    run_command("fuser -k 8000/tcp 2>/dev/null", "Killing port 8000", ignore_errors=True)
    run_command("fuser -k 5173/tcp 2>/dev/null", "Killing port 5173", ignore_errors=True)
    
    print_step(3, "Checking virtual environment")
    if not os.path.exists('.venv'):
        run_command("python3 -m venv .venv", "Creating virtual environment")
    else:
        print(f"  {Colors.GREEN}✓ Virtual environment exists{Colors.END}")
    
    print_step(4, "Installing/updating Python dependencies")
    run_command(".venv/bin/pip install -q -r requirements.txt", "Installing packages")
    
    print_step(5, "Checking database")
    if not os.path.exists('wcah.db'):
        print(f"  {Colors.YELLOW}Database not found, creating...{Colors.END}")
        run_command("yes yes | .venv/bin/python scripts/seed_database.py", "Seeding database")
    else:
        print(f"  {Colors.GREEN}✓ Database exists{Colors.END}")
    
    print_step(6, "Cleaning frontend build artifacts")
    run_command("cd src/frontend && rm -rf node_modules/.vite", "Clearing Vite cache", ignore_errors=True)
    run_command("cd src/frontend && rm -rf dist", "Clearing dist", ignore_errors=True)
    
    print_step(7, "Installing/updating frontend dependencies")
    run_command("cd src/frontend && npm install --legacy-peer-deps --silent", "Installing npm packages")
    
    print_step(8, "Starting backend server")
    backend_cmd = ".venv/bin/uvicorn src.backend.main:app --host 0.0.0.0 --port 8000 > /tmp/wcah-backend.log 2>&1 &"
    run_command(backend_cmd, "Starting backend")
    
    print_step(9, "Waiting for backend to be ready")
    print(f"  → Checking backend health...", end=" ")
    for i in range(20):
        try:
            result = subprocess.run(
                ["curl", "-s", "http://localhost:8000/api/health"],
                capture_output=True,
                text=True,
                timeout=1
            )
            if '"status":"healthy"' in result.stdout:
                print(f"{Colors.GREEN}✓{Colors.END}")
                break
        except:
            pass
        time.sleep(0.5)
    else:
        print(f"{Colors.RED}✗ Backend didn't start{Colors.END}")
        print(f"{Colors.YELLOW}Check logs: tail -f /tmp/wcah-backend.log{Colors.END}")
        sys.exit(1)
    
    print_step(10, "Starting frontend server")
    frontend_cmd = "cd src/frontend && npm run dev > /tmp/wcah-frontend.log 2>&1 &"
    run_command(frontend_cmd, "Starting frontend")
    
    print_step(11, "Waiting for frontend to be ready")
    print(f"  → Checking frontend...", end=" ")
    for i in range(20):
        try:
            result = subprocess.run(
                ["curl", "-s", "http://localhost:5173"],
                capture_output=True,
                text=True,
                timeout=1
            )
            if "html" in result.stdout.lower():
                print(f"{Colors.GREEN}✓{Colors.END}")
                break
        except:
            pass
        time.sleep(0.5)
    else:
        print(f"{Colors.RED}✗ Frontend didn't start{Colors.END}")
        print(f"{Colors.YELLOW}Check logs: tail -f /tmp/wcah-frontend.log{Colors.END}")
        sys.exit(1)
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}╔══════════════════════════════════════════════════════════════════╗")
    print(f"║                     ✓ ALL SYSTEMS READY!                        ║")
    print(f"╚══════════════════════════════════════════════════════════════════╝{Colors.END}\n")
    
    print(f"{Colors.BOLD}🌐 Access Your Application:{Colors.END}")
    print(f"  Frontend:  {Colors.GREEN}http://localhost:5173{Colors.END}")
    print(f"  Backend:   {Colors.GREEN}http://localhost:8000{Colors.END}")
    print(f"  API Docs:  {Colors.GREEN}http://localhost:8000/docs{Colors.END}")
    print(f"  Test Page: {Colors.GREEN}file://{project_dir}/test-connection.html{Colors.END}")
    
    print(f"\n{Colors.BOLD}👤 Sample Accounts:{Colors.END}")
    print(f"  Professor: {Colors.YELLOW}prof_smith{Colors.END} / password123")
    print(f"  Student:   {Colors.YELLOW}alice{Colors.END} / password123")
    
    print(f"\n{Colors.BOLD}{Colors.RED}⚠️  IMPORTANT: If you still see 'Cannot connect':{Colors.END}")
    print(f"  1. Open browser in {Colors.BOLD}INCOGNITO/PRIVATE{Colors.END} window")
    print(f"  2. OR open {Colors.BOLD}test-connection.html{Colors.END} and click 'Clear LocalStorage'")
    print(f"  3. Then go to {Colors.GREEN}http://localhost:5173{Colors.END}")
    
    print(f"\n{Colors.BOLD}📝 Logs:{Colors.END}")
    print(f"  Backend:  tail -f /tmp/wcah-backend.log")
    print(f"  Frontend: tail -f /tmp/wcah-frontend.log")
    
    print(f"\n{Colors.BOLD}🛑 To stop servers:{Colors.END}")
    print(f"  pkill -f uvicorn && pkill -f vite")
    
    print(f"\n{Colors.GREEN}✓ Setup complete! Open http://localhost:5173 in your browser{Colors.END}\n")

if __name__ == '__main__':
    main()
