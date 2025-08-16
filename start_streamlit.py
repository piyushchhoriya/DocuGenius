#!/usr/bin/env python3
"""
Simple Streamlit UI Startup Script
Run: python start_streamlit.py
"""

import subprocess
import sys
import os

def main():
    print("🎨 Starting DocuGenius Streamlit UI...")
    print("=" * 50)
    
    # Change to streamlit-ui directory
    streamlit_path = os.path.join(os.getcwd(), "streamlit-ui")
    if not os.path.exists(streamlit_path):
        print("❌ Streamlit UI directory not found!")
        sys.exit(1)
    
    os.chdir(streamlit_path)
    
    # Install dependencies if needed
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed!")
    except subprocess.CalledProcessError:
        print("⚠️  Some dependencies may not have installed properly")
    
    # Start Streamlit
    print("🚀 Starting Streamlit UI...")
    print("🌐 Streamlit UI will be available at: http://localhost:8501")
    print("📖 Backend API: http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"])

if __name__ == "__main__":
    main()
