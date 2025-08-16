#!/usr/bin/env python3
"""
DocuGenius Master Startup Script
Just run: python start_docugenius.py

This will start both the backend API and React frontend!
"""

import subprocess
import sys
import os
import time
import threading
import socket
import requests

def is_port_in_use(port):
    """Check if a port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_backend():
    """Start the backend API server"""
    print("🚀 Starting DocuGenius Backend...")
    backend_path = os.path.join(os.getcwd(), "backend")
    os.chdir(backend_path)
    subprocess.run([sys.executable, "main.py"])

def start_frontend():
    """Start the React frontend"""
    print("🎨 Starting DocuGenius Frontend...")
    frontend_path = os.path.join(os.getcwd(), "ui-react")
    os.chdir(frontend_path)
    subprocess.run(["npm", "run", "dev"])

def main():
    print("🌟 DocuGenius - AI-Powered Technical Documentation Generator")
    print("=" * 60)
    
    # Get the absolute path to the project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    # Check if we're in the right directory
    if not os.path.exists("backend/main.py") or not os.path.exists("ui-react/package.json"):
        print("❌ Error: Required files not found!")
        print(f"   Current directory: {os.getcwd()}")
        print("   Required: backend/main.py and ui-react/package.json")
        print("   Make sure you're in the DocuGenius root directory")
        sys.exit(1)
    
    print("🔑 OpenAI API Key: Already embedded in code!")
    print("📦 Dependencies: Already installed!")
    print(f"📁 Project root: {project_root}")
    print("=" * 60)
    
    # Check if backend is already running
    if is_port_in_use(8000):
        print("✅ Backend is already running on port 8000")
        print("🌐 Backend available at: http://localhost:8000")
    else:
        # Start backend in a separate thread
        print("🚀 Starting new backend instance...")
        backend_thread = threading.Thread(target=start_backend, daemon=True)
        backend_thread.start()
        
        # Wait a bit for backend to start
        print("⏳ Waiting for backend to start...")
        time.sleep(5)
    
    # Check if frontend is already running
    if is_port_in_use(3000):
        print("✅ Frontend is already running on port 3000")
        print("🌐 Frontend available at: http://localhost:3000")
    else:
        # Start frontend in main thread
        print("🎨 Starting React frontend...")
        start_frontend()

if __name__ == "__main__":
    main()
