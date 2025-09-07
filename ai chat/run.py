#!/usr/bin/env python3
"""
Nova AI Chat - Universal Launcher
Cross-platform launcher for Nova AI Chat (Server & Client)
Works on Windows, macOS, and Linux
"""
import sys
import subprocess
import os
import platform
import time
import threading

def print_banner():
    """Print welcome banner"""
    print("🚀 Nova AI Chat - Universal Launcher")
    print("=" * 45)
    print()

def start_server():
    """Start the chat server"""
    print("🔥 Starting Nova AI Chat Server...")
    try:
        # Use python3 on Unix-like systems, python on Windows
        python_cmd = "python" if platform.system().lower() == "windows" else "python3"
        subprocess.run([python_cmd, "launch_server.py"])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped.")
    except Exception as e:
        print(f"❌ Server error: {e}")

def start_client():
    """Start the chat client"""
    print("💬 Starting Nova AI Chat Client...")
    time.sleep(2)  # Give server time to start
    try:
        # Use python3 on Unix-like systems, python on Windows
        python_cmd = "python" if platform.system().lower() == "windows" else "python3"
        subprocess.run([python_cmd, "launch_client.py"])
    except KeyboardInterrupt:
        print("\n🛑 Client stopped.")
    except Exception as e:
        print(f"❌ Client error: {e}")

def main():
    """Main launcher function"""
    print_banner()
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("Choose what to launch:")
    print("1. 🖥️  Server only")
    print("2. 💬 Client only") 
    print("3. 🚀 Both (Server + Client)")
    print("4. ❌ Exit")
    print()
    
    while True:
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            start_server()
            break
        elif choice == "2":
            start_client()
            break
        elif choice == "3":
            print("🚀 Starting both Server and Client...")
            print("💡 Server will start first, then client will connect")
            print()
            
            # Start server in background thread
            server_thread = threading.Thread(target=start_server)
            server_thread.daemon = True
            server_thread.start()
            
            # Start client in main thread
            start_client()
            break
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Launcher cancelled.")
        sys.exit(0)
