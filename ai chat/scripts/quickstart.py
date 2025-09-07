#!/usr/bin/env python3
"""
Nova AI Chat - Quick Start Script
One-command setup and launch for Nova AI Chat
"""
import sys
import subprocess
import os
import time

def main():
    """Quick start - install and run"""
    print("🚀 Nova AI Chat - Quick Start")
    print("=" * 40)
    print()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Step 1: Run full installation
    print("📦 Running complete installation...")
    try:
        # Get the script directory and go to parent directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        install_path = os.path.join(script_dir, "install.py")
        
        result = subprocess.run([sys.executable, install_path], cwd=parent_dir, check=True)
        print("✅ Installation completed!")
    except subprocess.CalledProcessError:
        print("❌ Installation failed. Please run 'python scripts/install.py' manually.")
        return False
    except FileNotFoundError:
        print("❌ install.py not found. Please make sure all files are present.")
        return False
    
    print()
    
    # Step 2: Ask if user wants to configure now
    config_now = input("🔧 Configure Nova AI connection now? (Y/n): ").strip().lower()
    if config_now != 'n':
        try:
            setup_path = os.path.join(script_dir, "setup.py")
            subprocess.run([sys.executable, setup_path], cwd=parent_dir, check=True)
        except subprocess.CalledProcessError:
            print("⚠️  Configuration skipped - you can run 'python scripts/setup.py' later")
        except KeyboardInterrupt:
            print("\n⚠️  Configuration cancelled - you can run 'python scripts/setup.py' later")
    
    print()
    
    # Step 3: Ask if user wants to start server now
    start_now = input("🚀 Start Nova AI Chat Server now? (Y/n): ").strip().lower()
    if start_now != 'n':
        print()
        print("🔥 Starting Nova AI Chat Server...")
        print("💡 Tip: Open another terminal and run 'python launch_client.py' to connect")
        print()
        time.sleep(2)
        
        try:
            # Start the server from parent directory
            launch_server_path = os.path.join(parent_dir, "launch_server.py")
            subprocess.run([sys.executable, launch_server_path], cwd=parent_dir)
        except KeyboardInterrupt:
            print("\n🛑 Server stopped.")
        except Exception as e:
            print(f"❌ Server error: {e}")
    else:
        print()
        print("🎯 Ready to go! To start:")
        print("   Server: python launch_server.py")
        print("   Client: python launch_client.py")
        print()
        print("📖 For help: see README.md")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Quick start cancelled.")
        sys.exit(0)
