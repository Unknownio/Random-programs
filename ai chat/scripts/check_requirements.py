#!/usr/bin/env python3
"""
Nova AI Chat - System Requirements Checker
Checks if your system meets all requirements before installation
"""
import sys
import platform
import subprocess
import urllib.request
import urllib.error

def check_python():
    """Check Python version"""
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 6:
        print("✅ Python version is compatible")
        return True
    else:
        print("❌ Python 3.6+ required")
        print("   Download from: https://python.org")
        return False

def check_pip():
    """Check pip availability"""
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"✅ pip is available: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ pip not found")
        print("   Will be installed during setup")
        return False

def check_internet():
    """Check internet connectivity"""
    test_urls = ["https://pypi.org", "https://github.com"]
    
    for url in test_urls:
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                if response.status == 200:
                    print(f"✅ Internet connectivity: OK")
                    return True
        except:
            continue
    
    print("⚠️  Limited internet connectivity")
    print("   May affect package downloads")
    return False

def check_system():
    """Check system information"""
    system = platform.system()
    print(f"Operating System: {system} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    
    if system in ["Windows", "Darwin", "Linux"]:
        print("✅ Operating system is supported")
        return True
    else:
        print("⚠️  Untested operating system")
        return True

def check_disk_space():
    """Check available disk space"""
    import shutil
    
    try:
        total, used, free = shutil.disk_usage(".")
        free_mb = free // (1024 * 1024)
        
        print(f"Available Disk Space: {free_mb} MB")
        
        if free_mb > 100:  # Need at least 100MB
            print("✅ Sufficient disk space")
            return True
        else:
            print("⚠️  Low disk space (may cause issues)")
            return False
    except:
        print("⚠️  Could not check disk space")
        return True

def main():
    """Main requirements check"""
    print("🔍 Nova AI Chat - System Requirements Check")
    print("=" * 50)
    print()
    
    checks = []
    
    print("📋 System Information:")
    checks.append(check_system())
    checks.append(check_disk_space())
    print()
    
    print("🐍 Python Environment:")
    checks.append(check_python())
    checks.append(check_pip())
    print()
    
    print("🌐 Network Connectivity:")
    checks.append(check_internet())
    print()
    
    # Summary
    passed = sum(checks)
    total = len(checks)
    
    print("📊 Summary:")
    print(f"   Checks passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All requirements met! Ready for installation.")
        print()
        print("Next steps:")
        print("   Quick setup: python quickstart.py")
        print("   Manual setup: python install.py")
        return True
    elif passed >= total - 1:
        print("⚠️  Most requirements met. Installation should work.")
        print()
        print("You can proceed with:")
        print("   python install.py")
        return True
    else:
        print("❌ Several requirements not met.")
        print("   Please address the issues above before installation.")
        return False

if __name__ == "__main__":
    main()
