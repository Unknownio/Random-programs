#!/usr/bin/env python3
"""
Nova AI Chat Setup Script
Helps users configure their Nova AI chat application for first-time use
"""
import json
import os
import sys

def get_user_input(prompt, default=None):
    """Get user input with optional default value"""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        return input(f"{prompt}: ").strip()

def setup_config():
    """Interactive setup for config.json"""
    print("=== Nova AI Chat Configuration Setup ===\n")
    print("This script will help you configure your Nova AI chat application.")
    print("Note: This application was tested with LM Studio as the Nova AI backend.\n")
    
    # Load existing config if it exists (look in parent directory)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    config_path = os.path.join(parent_dir, 'config.json')
    default_config = {
        "lm_studio": {"host": "127.0.0.1", "port": 1234, "api_path": "/v1/chat/completions", "health_path": "/health"},
        "server": {"host": "0.0.0.0", "port": 8080},
        "database": {"file": "chat_database.db"},
        "security": {"password_min_length": 4}
    }
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                default_config = json.load(f)
            print("Found existing configuration. You can update the settings below.\n")
        except:
            print("Found corrupted config file. Creating new configuration.\n")
    
    # Get Nova AI (LM Studio) settings
    print("--- Nova AI (LM Studio) Configuration ---")
    print("Enter the IP address where Nova AI (LM Studio) is running:")
    print("- Use '127.0.0.1' if running on the same computer")
    print("- Use the IP address if running on a different computer (e.g., 192.168.1.100)")
    
    nova_ai_host = get_user_input("Nova AI Host", default_config["lm_studio"]["host"])
    nova_ai_port = get_user_input("Nova AI Port", str(default_config["lm_studio"]["port"]))
    
    try:
        nova_ai_port = int(nova_ai_port)
    except ValueError:
        print("Invalid port number, using default 1234")
        nova_ai_port = 1234
    
    # Get server settings
    print("\n--- Chat Server Configuration ---")
    print("These settings control how the chat server runs:")
    
    server_host = get_user_input("Server Host (0.0.0.0 for all interfaces)", default_config["server"]["host"])
    server_port = get_user_input("Server Port", str(default_config["server"]["port"]))
    
    try:
        server_port = int(server_port)
    except ValueError:
        print("Invalid port number, using default 8080")
        server_port = 8080
    
    # Create final configuration
    final_config = {
        "lm_studio": {
            "host": nova_ai_host,
            "port": nova_ai_port,
            "api_path": "/v1/chat/completions",
            "health_path": "/health"
        },
        "server": {
            "host": server_host,
            "port": server_port
        },
        "database": {
            "file": "chat_database.db"
        },
        "security": {
            "password_min_length": 4
        }
    }
    
    # Save configuration
    try:
        with open(config_path, 'w') as f:
            json.dump(final_config, f, indent=2)
        
        print(f"\n✓ Configuration saved to {config_path}")
        print("\n--- Configuration Summary ---")
        print(f"Nova AI (LM Studio): http://{nova_ai_host}:{nova_ai_port}")
        print(f"Chat Server: http://{server_host}:{server_port}")
        print("\n--- Next Steps ---")
        print("1. Make sure Nova AI (LM Studio) is running with a loaded model")
        print("2. Run: python launch_server.py")
        print("3. In another terminal, run: python launch_client.py")
        print("4. If you have connection issues, run: python scripts/network_test.py")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error saving configuration: {e}")
        return False

def main():
    """Main setup function"""
    try:
        if setup_config():
            print("\n🎉 Setup complete! You're ready to start chatting with Nova AI.")
        else:
            print("\n❌ Setup failed. Please check the error messages above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
