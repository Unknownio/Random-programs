#!/usr/bin/env python3
"""
Chat Server Launcher
Automatically installs dependencies and runs the chat server
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
        print("[SERVER LAUNCHER] ✓ pip is available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[SERVER LAUNCHER] pip not found. Attempting to install...")
        try:
            subprocess.run([sys.executable, "-m", "ensurepip", "--default-pip"], 
                          check=True, capture_output=True)
            print("[SERVER LAUNCHER] ✓ pip installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("[SERVER LAUNCHER] ✗ Failed to install pip automatically")
            print("Please install pip manually and try again")
            return False

def install_package(package_name):
    """Install a package using pip"""
    try:
        print(f"[SERVER LAUNCHER] Installing {package_name}...")
        subprocess.run([sys.executable, "-m", "pip", "install", package_name], 
                      check=True, capture_output=True)
        print(f"[SERVER LAUNCHER] ✓ {package_name} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[SERVER LAUNCHER] ✗ Failed to install {package_name}")
        return False

def setup_dependencies():
    """Setup all required dependencies"""
    print("[SERVER LAUNCHER] Setting up Nova AI Chat Server...")
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check pip
    if not check_and_install_pip():
        return False
    
    # Required packages for server
    required_packages = ["flask", "requests"]
    
    print("[SERVER LAUNCHER] Checking dependencies...")
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == "flask":
                importlib.import_module("flask")
            else:
                importlib.import_module(package)
            print(f"[SERVER LAUNCHER] ✓ {package} is available")
        except ImportError:
            missing_packages.append(package)
    
    # Install missing packages
    if missing_packages:
        print(f"[SERVER LAUNCHER] Installing: {', '.join(missing_packages)}")
        for package in missing_packages:
            if not install_package(package):
                return False
    
    print("[SERVER LAUNCHER] ✓ All dependencies ready!")
    return True

def run_server():
    """Run the chat server"""
    try:
        print("[SERVER LAUNCHER] Starting chat server...\n")
        
        # Change to the script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Check if chat_server.py exists
        server_path = os.path.join(script_dir, 'chat_server.py')
        if not os.path.exists(server_path):
            print("[SERVER LAUNCHER] ✗ chat_server.py not found in the same directory")
            print("Please make sure chat_server.py is in the same folder as this launcher")
            return False
        
        # Run the server using subprocess for better isolation
        print("[SERVER LAUNCHER] Launching Nova AI Chat Server...")
        subprocess.run([sys.executable, 'chat_server.py'], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"[SERVER LAUNCHER] ✗ Server exited with error code: {e.returncode}")
    except KeyboardInterrupt:
        print(f"\n[SERVER LAUNCHER] Server stopped by user")
    except Exception as e:
        print(f"[SERVER LAUNCHER] ✗ Error running server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("    Nova AI Chat Server Launcher")
    print("=" * 50)
    
    if setup_dependencies():
        run_server()
    else:
        print("\n[SERVER LAUNCHER] ✗ Setup failed. Please fix the issues above and try again.")
        input("Press Enter to exit...")
        sys.exit(1)
