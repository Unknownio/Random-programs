#!/usr/bin/env python3
"""
Nova AI Chat - Complete Setup Script
Downloads and installs everything needed to run the Nova AI Chat application.
This script handles Python dependencies, configuration setup, and initial testing.
"""
import sys
import subprocess
import importlib
import os
import json
import urllib.request
import urllib.error
import platform

# Colors for output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    """Print welcome header"""
    print(f"{Colors.BLUE}{Colors.BOLD}")
    print("=" * 60)
    print("     Nova AI Chat - Complete Setup & Installation")
    print("=" * 60)
    print(f"{Colors.RESET}")
    print("This script will set up everything you need to run Nova AI Chat.")
    print("Tested with LM Studio as the Nova AI backend.\n")

def check_python_version():
    """Check if Python version is compatible"""
    print(f"{Colors.YELLOW}[SETUP]{Colors.RESET} Checking Python version...")
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print(f"{Colors.RED}✗ Python 3.6+ required. Current: {version.major}.{version.minor}{Colors.RESET}")
        print("Please install Python 3.6 or higher from https://python.org")
        return False
    
    print(f"{Colors.GREEN}✓ Python {version.major}.{version.minor}.{version.micro} - Compatible{Colors.RESET}")
    return True

def check_and_install_pip():
    """Check if pip is available and install if missing"""
    print(f"{Colors.YELLOW}[SETUP]{Colors.RESET} Checking pip installation...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True, text=True)
        print(f"{Colors.GREEN}✓ pip is available{Colors.RESET}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{Colors.YELLOW}Installing pip...{Colors.RESET}")
        try:
            subprocess.run([sys.executable, "-m", "ensurepip", "--default-pip"], 
                          check=True, capture_output=True, text=True)
            print(f"{Colors.GREEN}✓ pip installed successfully{Colors.RESET}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}✗ Failed to install pip: {e}{Colors.RESET}")
            print("Please install pip manually from https://pip.pypa.io/en/stable/installation/")
            return False

def upgrade_pip():
    """Upgrade pip to latest version"""
    print(f"{Colors.YELLOW}[SETUP]{Colors.RESET} Upgrading pip to latest version...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True, text=True)
        print(f"{Colors.GREEN}✓ pip upgraded successfully{Colors.RESET}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Colors.YELLOW}⚠ Failed to upgrade pip (continuing anyway): {e}{Colors.RESET}")
        return True  # Non-critical failure

def install_requirements():
    """Install all required packages"""
    print(f"{Colors.YELLOW}[SETUP]{Colors.RESET} Installing required Python packages...")
    
    required_packages = [
        "flask>=2.0.0",
        "requests>=2.25.0"
    ]
    
    # Create requirements.txt if it doesn't exist (in parent directory)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    requirements_path = os.path.join(parent_dir, 'requirements.txt')
    
    if not os.path.exists(requirements_path):
        print(f"{Colors.YELLOW}Creating requirements.txt...{Colors.RESET}")
        with open(requirements_path, 'w') as f:
            f.write("flask>=2.0.0\n")
            f.write("requests>=2.25.0\n")
        print(f"{Colors.GREEN}✓ requirements.txt created{Colors.RESET}")
    
    # Install packages
    for package in required_packages:
        print(f"Installing {package}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                          check=True, capture_output=True, text=True)
            print(f"{Colors.GREEN}✓ {package} installed{Colors.RESET}")
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}✗ Failed to install {package}: {e}{Colors.RESET}")
            return False
    
    print(f"{Colors.GREEN}✓ All Python packages installed successfully{Colors.RESET}")
    return True

def verify_imports():
    """Verify that all required modules can be imported"""
    print(f"{Colors.YELLOW}[SETUP]{Colors.RESET} Verifying package installations...")
    
    required_modules = ["flask", "requests", "sqlite3", "json", "threading", "datetime"]
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"{Colors.GREEN}✓ {module} - OK{Colors.RESET}")
        except ImportError as e:
            print(f"{Colors.RED}✗ {module} - Failed: {e}{Colors.RESET}")
            return False
    
    print(f"{Colors.GREEN}✓ All required modules are available{Colors.RESET}")
    return True

def create_default_config():
    """Create default configuration file if it doesn't exist"""
    print(f"{Colors.YELLOW}[SETUP]{Colors.RESET} Setting up configuration...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    config_path = os.path.join(parent_dir, 'config.json')
    
    default_config = {
        "lm_studio": {
            "host": "127.0.0.1",
            "port": 1234,
            "api_path": "/v1/chat/completions",
            "health_path": "/health"
        },
        "server": {
            "host": "0.0.0.0",
            "port": 8080
        },
        "database": {
            "file": "chat_database.db"
        },
        "security": {
            "password_min_length": 4
        }
    }
    
    if os.path.exists(config_path):
        print(f"{Colors.GREEN}✓ config.json already exists{Colors.RESET}")
        return True
    
    try:
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
        print(f"{Colors.GREEN}✓ config.json created with default settings{Colors.RESET}")
        return True
    except Exception as e:
        print(f"{Colors.RED}✗ Failed to create config.json: {e}{Colors.RESET}")
        return False

def test_network_connectivity():
    """Test basic network connectivity"""
    print(f"{Colors.YELLOW}[SETUP]{Colors.RESET} Testing network connectivity...")
    
    test_urls = [
        "http://httpbin.org/get",
        "https://api.github.com"
        # Note: LM Studio /health endpoint generates error logs, so we skip it
    ]
    
    working_connections = 0
    
    for url in test_urls:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Nova-AI-Chat-Setup'})
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    print(f"{Colors.GREEN}✓ {url} - OK{Colors.RESET}")
                    working_connections += 1
                else:
                    print(f"{Colors.YELLOW}⚠ {url} - Status {response.status}{Colors.RESET}")
        except urllib.error.URLError:
            print(f"{Colors.RED}✗ {url} - Connection failed{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}✗ {url} - Error: {e}{Colors.RESET}")
    
    if working_connections >= 2:
        print(f"{Colors.GREEN}✓ Network connectivity looks good{Colors.RESET}")
        return True
    else:
        print(f"{Colors.YELLOW}⚠ Limited network connectivity (may affect some features){Colors.RESET}")
        return True  # Non-critical

def create_startup_scripts():
    """Create convenient startup scripts"""
    print(f"{Colors.YELLOW}[SETUP]{Colors.RESET} Creating startup scripts...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    system = platform.system().lower()
    
    # Create batch file for Windows
    if system == "windows":
        start_server_bat = os.path.join(parent_dir, 'start_server.bat')
        start_client_bat = os.path.join(parent_dir, 'start_client.bat')
        
        with open(start_server_bat, 'w') as f:
            f.write('@echo off\n')
            f.write('echo Starting Nova AI Chat Server...\n')
            f.write('python launch_server.py\n')
            f.write('pause\n')
        
        with open(start_client_bat, 'w') as f:
            f.write('@echo off\n')
            f.write('echo Starting Nova AI Chat Client...\n')
            f.write('python launch_client.py\n')
            f.write('pause\n')
        
        print(f"{Colors.GREEN}✓ Windows batch files created (start_server.bat, start_client.bat){Colors.RESET}")
    
    # Create shell scripts for Unix-like systems
    else:
        start_server_sh = os.path.join(parent_dir, 'start_server.sh')
        start_client_sh = os.path.join(parent_dir, 'start_client.sh')
        
        with open(start_server_sh, 'w') as f:
            f.write('#!/bin/bash\n')
            f.write('# Nova AI Chat Server Launcher for Mac/Linux\n')
            f.write('echo "🚀 Starting Nova AI Chat Server..."\n')
            f.write('cd "$(dirname "$0")"\n')
            f.write('python3 launch_server.py\n')
            f.write('echo "Press any key to exit..."\n')
            f.write('read -n 1\n')
        
        with open(start_client_sh, 'w') as f:
            f.write('#!/bin/bash\n')
            f.write('# Nova AI Chat Client Launcher for Mac/Linux\n')
            f.write('echo "💬 Starting Nova AI Chat Client..."\n')
            f.write('cd "$(dirname "$0")"\n')
            f.write('python3 launch_client.py\n')
            f.write('echo "Press any key to exit..."\n')
            f.write('read -n 1\n')
        
        # Make scripts executable
        os.chmod(start_server_sh, 0o755)
        os.chmod(start_client_sh, 0o755)
        
        print(f"{Colors.GREEN}✓ Shell scripts created (start_server.sh, start_client.sh){Colors.RESET}")
    
    return True

def show_final_instructions():
    """Show final setup instructions"""
    print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 Setup Complete!{Colors.RESET}")
    print(f"\n{Colors.BLUE}Next Steps:{Colors.RESET}")
    print("1. Install and start Nova AI (LM Studio):")
    print("   - Download from: https://lmstudio.ai/")
    print("   - Load an AI model")
    print("   - Start the server (usually runs on port 1234)")
    print()
    print("2. Configure Nova AI connection (if needed):")
    print("   - Run: python setup.py")
    print("   - Or edit config.json manually")
    print()
    print("3. Start the chat application:")
    
    system = platform.system().lower()
    if system == "windows":
        print("   🪟 Windows:")
        print("     - Double-click start_server.bat")
        print("     - Double-click start_client.bat (in another window)")
    elif system == "darwin":  # macOS
        print("   🍎 macOS:")
        print("     - Double-click start_server.sh (or run: ./start_server.sh)")
        print("     - Double-click start_client.sh (or run: ./start_client.sh)")
        print("     - You may need to allow execution in System Preferences > Security")
    else:  # Linux
        print("   🐧 Linux:")
        print("     - Run: ./start_server.sh")
        print("     - Run: ./start_client.sh (in another terminal)")
    
    print()
    print("   ⚙️  Manual start (all platforms):")
    print("     - Terminal 1: python launch_server.py (or python3)")
    print("     - Terminal 2: python launch_client.py (or python3)")
    print()
    print("4. Test connectivity:")
    print("   - Run: python scripts/network_test.py")
    print()
    print(f"{Colors.YELLOW}📋 Available Files:{Colors.RESET}")
    print("- README.md - Complete documentation")
    print("- setup.py - Interactive configuration")
    print("- scripts/network_test.py - Connection testing")
    print("- config.json - Configuration file")
    print()
    print(f"{Colors.GREEN}Happy chatting with Nova AI! 🤖{Colors.RESET}")

def main():
    """Main setup function"""
    print_header()
    
    # Step 1: Check Python version
    if not check_python_version():
        return False
    
    # Step 2: Check and install pip
    if not check_and_install_pip():
        return False
    
    # Step 3: Upgrade pip
    upgrade_pip()
    
    # Step 4: Install requirements
    if not install_requirements():
        return False
    
    # Step 5: Verify imports
    if not verify_imports():
        return False
    
    # Step 6: Create default config
    if not create_default_config():
        return False
    
    # Step 7: Test network connectivity
    test_network_connectivity()
    
    # Step 8: Create startup scripts
    create_startup_scripts()
    
    # Step 9: Show final instructions
    show_final_instructions()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print(f"\n{Colors.RED}❌ Setup failed. Please check the errors above.{Colors.RESET}")
            sys.exit(1)
        else:
            print(f"\n{Colors.GREEN}✅ Setup completed successfully!{Colors.RESET}")
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Setup cancelled by user.{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Unexpected error: {e}{Colors.RESET}")
        sys.exit(1)
