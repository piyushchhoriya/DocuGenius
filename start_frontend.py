#!/usr/bin/env python3
"""
DocuGenius Frontend Startup Script
Just run: python start_frontend.py
"""

import subprocess
import sys
import os
import webbrowser
import time

def main():
    print("🎨 DocuGenius Frontend Startup")
    print("=" * 50)
    
    # Get the absolute path to the project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    # Check if we're in the right directory
    if not os.path.exists("ui-react/package.json"):
        print("❌ Error: ui-react/package.json not found!")
        print(f"   Current directory: {os.getcwd()}")
        print("   Make sure you're in the DocuGenius root directory")
        sys.exit(1)
    
    # Change to ui-react directory
    frontend_path = os.path.join(project_root, "ui-react")
    os.chdir(frontend_path)
    
    print("📦 Starting React development server...")
    print("🌐 Frontend will be at http://localhost:3000")
    print("=" * 50)
    
    try:
        # Start the React dev server
        subprocess.run(["npm", "run", "dev"])
    except KeyboardInterrupt:
        print("\n🛑 Frontend stopped by user")
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")

if __name__ == "__main__":
    main()
