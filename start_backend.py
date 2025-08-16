#!/usr/bin/env python3
"""
Simple Backend Startup Script
Run: python start_backend.py
"""

import subprocess
import sys
import os

def main():
    print("🚀 Starting DocuGenius Backend...")
    print("=" * 50)
    
    # Change to backend directory
    backend_path = os.path.join(os.getcwd(), "backend")
    if not os.path.exists(backend_path):
        print("❌ Backend directory not found!")
        sys.exit(1)
    
    os.chdir(backend_path)
    
    # Install dependencies if needed
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed!")
    except subprocess.CalledProcessError:
        print("⚠️  Some dependencies may not have installed properly")
    
    # Start the backend
    print("🚀 Starting FastAPI server...")
    print("🌐 Backend will be available at: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    subprocess.run([sys.executable, "main.py"])

if __name__ == "__main__":
    main()
