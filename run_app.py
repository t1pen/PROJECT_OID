#!/usr/bin/env python3
"""
EDA Interactive Dashboard - Quick Setup & Launch Script
This script installs dependencies and launches the Streamlit app
"""

import subprocess
import sys
import os
from pathlib import Path

def print_header():
    print("\n" + "="*50)
    print("  EDA Interactive Dashboard Launcher")
    print("="*50 + "\n")

def check_python():
    """Check if Python is available"""
    try:
        version = sys.version_info
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} found")
        return True
    except Exception as e:
        print(f"✗ Error checking Python: {e}")
        return False

def install_requirements():
    """Install required packages from requirements.txt"""
    print("\nInstalling required packages...")
    print("(This may take a few minutes on first run)\n")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("\n✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Failed to install dependencies: {e}")
        return False

def launch_app():
    """Launch the Streamlit application"""
    print("\nLaunching EDA Interactive Dashboard...\n")
    print("The app will open in your browser at: http://localhost:8501")
    print("Press Ctrl+C to stop the application\n")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n\nApplication closed by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error launching app: {e}")
        sys.exit(1)

def main():
    print_header()
    
    # Check Python
    if not check_python():
        print("\nFailed to verify Python installation")
        sys.exit(1)
    
    # Verify we're in the right directory
    if not Path("app.py").exists():
        print("\n✗ Error: app.py not found in current directory")
        print(f"Current directory: {os.getcwd()}")
        print("Please run this script from the PROJECT_OID directory")
        sys.exit(1)
    
    print("✓ Found app.py")
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Launch app
    launch_app()

if __name__ == "__main__":
    main()
