#!/usr/bin/env python3
"""
Quick start script for the Regulatory Report Assistant
This script helps you get the application running quickly
"""
import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def run_command(command, description, cwd=None):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True, cwd=cwd)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_python():
    """Check if Python is available"""
    try:
        version = subprocess.run([sys.executable, '--version'], capture_output=True, text=True)
        print(f"✅ Python found: {version.stdout.strip()}")
        return True
    except:
        print("❌ Python not found. Please install Python 3.8+")
        return False

def check_node():
    """Check if Node.js is available"""
    try:
        version = subprocess.run(['node', '--version'], capture_output=True, text=True)
        print(f"✅ Node.js found: {version.stdout.strip()}")
        return True
    except:
        print("❌ Node.js not found. Please install Node.js 16+")
        return False

def setup_backend():
    """Setup the Django backend"""
    print("\n🚀 Setting up Django Backend")
    print("=" * 40)
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    # Install dependencies
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", 
                      "Installing Python dependencies", cwd=backend_dir):
        return False
    
    # Run setup
    if not run_command(f"{sys.executable} setup.py", 
                      "Running Django setup", cwd=backend_dir):
        return False
    
    return True

def setup_frontend():
    """Setup the React frontend"""
    print("\n🚀 Setting up React Frontend")
    print("=" * 40)
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    # Install dependencies
    if not run_command("npm install", "Installing Node.js dependencies", cwd=frontend_dir):
        return False
    
    return True

def start_backend():
    """Start the Django backend server"""
    print("\n🚀 Starting Django Backend Server")
    print("=" * 40)
    
    backend_dir = Path("backend")
    try:
        # Start server in background
        process = subprocess.Popen(
            [sys.executable, "manage.py", "runserver"],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("✅ Django server started on http://localhost:8000")
        print("   Admin interface: http://localhost:8000/admin")
        print("   API endpoints: http://localhost:8000/api/")
        return process
    except Exception as e:
        print(f"❌ Failed to start Django server: {e}")
        return None

def start_frontend():
    """Start the React frontend server"""
    print("\n🚀 Starting React Frontend Server")
    print("=" * 40)
    
    frontend_dir = Path("frontend")
    try:
        # Start server in background
        process = subprocess.Popen(
            ["npm", "start"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("✅ React server started on http://localhost:3000")
        return process
    except Exception as e:
        print(f"❌ Failed to start React server: {e}")
        return None

def main():
    """Main function"""
    print("🎯 Regulatory Report Assistant - Quick Start")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python():
        return False
    
    if not check_node():
        return False
    
    # Setup backend
    if not setup_backend():
        print("\n❌ Backend setup failed")
        return False
    
    # Setup frontend
    if not setup_frontend():
        print("\n❌ Frontend setup failed")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\nTo start the application:")
    print("1. Backend: cd backend && python manage.py runserver")
    print("2. Frontend: cd frontend && npm start")
    print("\nOr run this script with --start flag to start both servers")
    
    # Check if user wants to start servers
    if len(sys.argv) > 1 and sys.argv[1] == "--start":
        print("\n🚀 Starting both servers...")
        
        backend_process = start_backend()
        if not backend_process:
            return False
        
        time.sleep(3)  # Wait for backend to start
        
        frontend_process = start_frontend()
        if not frontend_process:
            backend_process.terminate()
            return False
        
        print("\n🎉 Both servers are running!")
        print("📱 Frontend: http://localhost:3000")
        print("🔧 Backend API: http://localhost:8000/api/")
        print("⚙️  Admin: http://localhost:8000/admin")
        print("\nPress Ctrl+C to stop both servers")
        
        try:
            # Wait for user to stop
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping servers...")
            backend_process.terminate()
            frontend_process.terminate()
            print("✅ Servers stopped")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
