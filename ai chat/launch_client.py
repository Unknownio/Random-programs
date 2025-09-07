#!/usr/bin/env python3
"""
Simple Chat Client Launcher
Automatically installs dependencies and runs the chat client
"""
import sys
import subprocess
import importlib
import os

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 6):
        print("Error: Python 3.6 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    return True

def check_and_install_pip():
    """Check if pip is available and install if missing"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print("[LAUNCHER] ✓ pip is available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[LAUNCHER] pip not found. Attempting to install...")
        try:
            subprocess.run([sys.executable, "-m", "ensurepip", "--default-pip"], 
                          check=True, capture_output=True)
            print("[LAUNCHER] ✓ pip installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("[LAUNCHER] ✗ Failed to install pip automatically")
            print("Please install pip manually and try again")
            return False

def install_package(package_name):
    """Install a package using pip"""
    try:
        print(f"[LAUNCHER] Installing {package_name}...")
        subprocess.run([sys.executable, "-m", "pip", "install", package_name], 
                      check=True, capture_output=True)
        print(f"[LAUNCHER] ✓ {package_name} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[LAUNCHER] ✗ Failed to install {package_name}")
        return False

def setup_dependencies():
    """Setup all required dependencies"""
    print("[LAUNCHER] Setting up Nova AI Chat Client...")
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check pip
    if not check_and_install_pip():
        return False
    
    # Required packages
    required_packages = ["requests"]
    
    print("[LAUNCHER] Checking dependencies...")
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"[LAUNCHER] ✓ {package} is available")
        except ImportError:
            missing_packages.append(package)
    
    # Install missing packages
    if missing_packages:
        print(f"[LAUNCHER] Installing: {', '.join(missing_packages)}")
        for package in missing_packages:
            if not install_package(package):
                return False
    
    print("[LAUNCHER] ✓ All dependencies ready!")
    return True

def run_client():
    """Run the chat client"""
    try:
        print("[LAUNCHER] Starting chat client...\n")
        
        # Change to the script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Check if chat_client.py exists
        client_path = os.path.join(script_dir, 'chat_client.py')
        if not os.path.exists(client_path):
            print("[LAUNCHER] ✗ chat_client.py not found in the same directory")
            print("Please make sure chat_client.py is in the same folder as this launcher")
            return False
        
        # Run the client using subprocess for better isolation
        print("[LAUNCHER] Launching Nova AI Chat Client...")
        subprocess.run([sys.executable, 'chat_client.py'], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"[LAUNCHER] ✗ Client exited with error code: {e.returncode}")
    except KeyboardInterrupt:
        print(f"\n[LAUNCHER] Client stopped by user")
    except Exception as e:
        print(f"[LAUNCHER] ✗ Error running client: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("    Nova AI Chat Client Launcher")
    print("=" * 50)
    
    if setup_dependencies():
        run_client()
    else:
        print("\n[LAUNCHER] ✗ Setup failed. Please fix the issues above and try again.")
        input("Press Enter to exit...")
        sys.exit(1)
