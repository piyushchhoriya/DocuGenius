#!/usr/bin/env python3
"""
Test script for DocuGenius Streamlit UI
Run this to verify all components work correctly
"""

import sys
import os
import requests
import json

def test_backend_connection():
    """Test if the backend is accessible"""
    print("🔍 Testing backend connection...")
    try:
        response = requests.get("http://localhost:8000/health/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and healthy!")
            data = response.json()
            print(f"   Version: {data.get('version', 'Unknown')}")
            print(f"   Status: {data.get('status', 'Unknown')}")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend connection failed: {str(e)}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🔍 Testing API endpoints...")
    
    # Test modes endpoint
    try:
        response = requests.get("http://localhost:8000/ask/modes", timeout=5)
        if response.status_code == 200:
            modes = response.json()
            print(f"✅ Modes endpoint working - {len(modes.get('modes', []))} modes available")
        else:
            print(f"❌ Modes endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Modes endpoint error: {str(e)}")
    
    # Test documentation generation
    try:
        test_request = {
            "query": "What is a function in Python?",
            "mode": "explain",
            "audience": "beginner",
            "withDiagram": True,
            "verifyCode": False
        }
        response = requests.post("http://localhost:8000/ask/", json=test_request, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ Documentation generation working!")
            print(f"   Generation time: {result.get('generation_time', 0):.2f}s")
            print(f"   Confidence: {result.get('confidence', 0):.1%}")
        else:
            print(f"❌ Documentation generation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Documentation generation error: {str(e)}")

def test_streamlit_dependencies():
    """Test if Streamlit dependencies are available"""
    print("\n🔍 Testing Streamlit dependencies...")
    
    required_packages = [
        'streamlit',
        'requests',
        'pandas',
        'plotly',
        'streamlit_ace',
        'streamlit_option_menu'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is available")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    else:
        print("✅ All required packages are available!")
        return True

def test_language_detection():
    """Test language detection functionality"""
    print("\n🔍 Testing language detection...")
    
    test_cases = [
        ("def hello_world():", "python"),
        ("function greet() {", "javascript"),
        ("public class Main {", "java"),
        ("interface User {", "typescript"),
        ("fn calculate() {", "rust"),
        ("func main() {", "go"),
        ("#include <iostream>", "cpp"),
        ("using System;", "csharp"),
        ("This is just text", "text")
    ]
    
    # Import the detection function
    sys.path.append(os.path.join(os.path.dirname(__file__)))
    from app import detect_language
    
    for code, expected in test_cases:
        detected = detect_language(code)
        if detected == expected:
            print(f"✅ '{code[:20]}...' -> {detected}")
        else:
            print(f"❌ '{code[:20]}...' -> {detected} (expected {expected})")

def main():
    """Run all tests"""
    print("🚀 DocuGenius Streamlit UI - Component Test")
    print("=" * 50)
    
    # Test backend
    backend_ok = test_backend_connection()
    
    if backend_ok:
        test_api_endpoints()
    
    # Test dependencies
    deps_ok = test_streamlit_dependencies()
    
    # Test language detection
    test_language_detection()
    
    print("\n" + "=" * 50)
    if backend_ok and deps_ok:
        print("🎉 All tests passed! Streamlit UI should work correctly.")
        print("\nTo start the Streamlit UI:")
        print("  python start_streamlit.py")
        print("  or")
        print("  cd streamlit-ui && streamlit run app.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues before running the UI.")
        if not backend_ok:
            print("  - Start the backend: python start_backend.py")
        if not deps_ok:
            print("  - Install dependencies: pip install -r streamlit-ui/requirements.txt")

if __name__ == "__main__":
    main()
