#!/usr/bin/env python3
import sys
import subprocess
import importlib

def check_and_install_pip():
    """Check if pip is available and install if missing"""
    try:
        import pip
        print("[SETUP] ✓ pip is available")
        return True
    except ImportError:
        print("[SETUP] pip not found. Attempting to install...")
        try:
            # Try to install pip using get-pip.py method
            subprocess.check_call([sys.executable, "-m", "ensurepip", "--default-pip"])
            print("[SETUP] ✓ pip installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("[SETUP] ✗ Failed to install pip automatically")
            print("Please install pip manually: https://pip.pypa.io/en/stable/installation/")
            return False

def install_package(package_name):
    """Install a package using pip"""
    try:
        print(f"[SETUP] Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name, "--quiet"])
        print(f"[SETUP] ✓ {package_name} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[SETUP] ✗ Failed to install {package_name}: {e}")
        return False

def check_and_install_dependencies():
    """Check and install required dependencies"""
    required_packages = ["requests"]
    
    print("[SETUP] Checking dependencies...")
    
    # Check pip first
    if not check_and_install_pip():
        return False
    
    missing_packages = []
    
    # Check each required package
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"[SETUP] ✓ {package} is available")
        except ImportError:
            print(f"[SETUP] {package} not found")
            missing_packages.append(package)
    
    # Install missing packages
    if missing_packages:
        print(f"[SETUP] Installing missing packages: {', '.join(missing_packages)}")
        for package in missing_packages:
            if not install_package(package):
                print(f"[SETUP] ✗ Failed to install {package}")
                return False
        print("[SETUP] ✓ All dependencies installed successfully")
        
        # Reload modules after installation
        for package in missing_packages:
            try:
                importlib.import_module(package)
            except ImportError:
                print(f"[SETUP] ✗ Still cannot import {package} after installation")
                return False
    else:
        print("[SETUP] ✓ All dependencies are already available")
    
    return True

# Install dependencies automatically
if not check_and_install_dependencies():
    print("[SETUP] ✗ Dependency installation failed. Exiting...")
    sys.exit(1)

# Now import the required modules
import requests
import threading
import time
import json
import os
from datetime import datetime

# Load configuration
def load_config():
    """Load configuration from config.json"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, 'config.json')
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            print("[CLIENT] Warning: config.json not found, using default values")
            return {
                "server": {"host": "127.0.0.1", "port": 8080}
            }
    except Exception as e:
        print(f"[CLIENT] Error loading config: {e}, using defaults")
        return {
            "server": {"host": "127.0.0.1", "port": 8080}
        }

# Load configuration and set server URL
config = load_config()
# Client connects to the chat server (use 127.0.0.1 if server host is 0.0.0.0)
server_host = config['server']['host'] if config['server']['host'] != "0.0.0.0" else "127.0.0.1"
SERVER_URL = f"http://{server_host}:{config['server']['port']}"

# Colors
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

# Global variables
stop_animation = False
conversation_history = []
current_user = None

def loading():
    """Loop animation until stopped"""
    while not stop_animation:
        for c in "|/-\\":
            if stop_animation:
                break
            print(f"\rGenerating {c}", end="", flush=True)
            time.sleep(0.2)

def check_server_status():
    """Check if chat server is online"""
    print("Checking chat server connection...", end="", flush=True)
    
    while True:
        try:
            response = requests.get(f"{SERVER_URL}/api/health", timeout=5)
            if response.status_code == 200:
                result = response.json()
                # Check Nova AI status with fallback for compatibility
                nova_ai_status = result.get("nova_ai", result.get("lm_studio", "unknown"))
                if nova_ai_status == "online":
                    print(" ✓ Connected! (Nova AI online)")
                elif nova_ai_status == "offline":
                    print(" ✓ Connected! (Warning: Nova AI offline)")
                else:
                    print(" ✓ Connected! (Nova AI will be checked when needed)")
                return True
        except requests.exceptions.RequestException:
            pass
        except (KeyError, ValueError) as e:
            print(f" ✗ Server response error: {e}")
            pass
        
        print(" ✗ Server offline. Retrying in 3 seconds...", end="", flush=True)
        time.sleep(3)
        print("\rChecking chat server connection...", end="", flush=True)

def user_register():
    """Register a new user"""
    print(f"\n{YELLOW}=== Register New User ==={RESET}")
    username = input("Enter username: ").strip()
    
    if not username:
        print("Username cannot be empty!")
        return user_register()
    
    import getpass
    password = getpass.getpass("Enter password (min 4 chars): ").strip()
    
    if len(password) < 4:
        print("Password must be at least 4 characters!")
        return user_register()
    
    try:
        data = {"username": username, "password": password}
        response = requests.post(f"{SERVER_URL}/api/user/register", json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"{GREEN}✓ Registration successful!{RESET}")
            return True
        else:
            error_msg = response.json().get("error", "Registration failed")
            print(f"{RED}✗ {error_msg}{RESET}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"{RED}✗ Network error: {e}{RESET}")
        return False

def user_login():
    """Login existing user"""
    global current_user
    
    print(f"\n{YELLOW}=== Nova AI Chat ==={RESET}")
    
    # Ask if new user or existing
    while True:
        choice = input("Are you a (N)ew user or (E)xisting user? [N/E]: ").strip().upper()
        if choice in ['N', 'E']:
            break
        print("Please enter 'N' for new user or 'E' for existing user")
    
    if choice == 'N':
        if not user_register():
            return user_login()
    
    # Login process
    username = input("Enter your username: ").strip()
    
    if not username:
        print("Username cannot be empty!")
        return user_login()
    
    import getpass
    password = getpass.getpass("Enter password: ").strip()
    
    try:
        data = {"username": username, "password": password}
        response = requests.post(f"{SERVER_URL}/api/user/login", json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                current_user = username
                if result.get("is_new_user"):
                    print(f"{GREEN}Welcome, {username}! You have no previous conversations.{RESET}")
                else:
                    print(f"{GREEN}Welcome back, {username}!{RESET}")
                return result.get("has_conversations", False)
            else:
                print(f"{RED}Error: {result.get('error', 'Unknown error')}{RESET}")
                return user_login()
        elif response.status_code == 401:
            error_msg = response.json().get("error", "Invalid credentials")
            print(f"{RED}✗ {error_msg}{RESET}")
            return user_login()
        else:
            print(f"{RED}Server error: {response.status_code}{RESET}")
            return user_login()
            
    except requests.exceptions.RequestException as e:
        print(f"{RED}Connection error: {str(e)}{RESET}")
        return user_login()

def load_conversation():
    """Load conversation history from server"""
    global conversation_history
    
    if not current_user:
        return False
    
    try:
        data = {"username": current_user}
        response = requests.post(f"{SERVER_URL}/api/conversation/load", json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                conversation_history = result.get("messages", [])
                timestamp = result.get("updated_at")
                if timestamp and conversation_history:
                    print(f"{GREEN}Loaded conversation from: {timestamp}{RESET}")
                    return True
        return False
        
    except requests.exceptions.RequestException:
        return False

def clear_conversation():
    """Clear conversation on server"""
    if not current_user:
        return False
    
    try:
        data = {"username": current_user}
        response = requests.post(f"{SERVER_URL}/api/conversation/clear", json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("success", False)
        return False
        
    except requests.exceptions.RequestException:
        return False

def show_conversation_summary():
    """Show conversation summary"""
    if not current_user:
        return
    
    try:
        data = {"username": current_user}
        response = requests.post(f"{SERVER_URL}/api/conversation/summary", json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                timestamp = result.get("timestamp")
                total_messages = result.get("total_messages", 0)
                preview_messages = result.get("preview_messages", [])
                
                if total_messages > 0:
                    print(f"\n{GREEN}=== Previous Conversation Summary ==={RESET}")
                    print(f"Date: {timestamp}")
                    print(f"Total messages: {total_messages}")
                    
                    if preview_messages:
                        print("\nLast few exchanges:")
                        for msg in preview_messages:
                            print(f"{msg['role']}: {msg['content']}")
                    print(f"{GREEN}========================{RESET}\n")
                else:
                    print("No previous conversation found.")
        
    except requests.exceptions.RequestException:
        print("Error fetching conversation summary.")

def list_conversations():
    """List all conversations for the current user"""
    if not current_user:
        return []
    
    try:
        data = {"username": current_user}
        response = requests.post(f"{SERVER_URL}/api/conversation/list", json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                return result.get("conversations", [])
        return []
        
    except requests.exceptions.RequestException:
        return []

def select_conversation(conversation_id):
    """Load a specific conversation by ID"""
    global conversation_history
    
    if not current_user:
        return False
    
    try:
        data = {"username": current_user, "conversation_id": conversation_id}
        response = requests.post(f"{SERVER_URL}/api/conversation/select", json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                conversation_history = result.get("messages", [])
                timestamp = result.get("updated_at")
                print(f"{GREEN}Loaded conversation from: {timestamp}{RESET}")
                return True
        return False
        
    except requests.exceptions.RequestException:
        return False

def delete_conversation(conversation_id):
    """Delete a specific conversation by ID"""
    if not current_user:
        return False
    
    try:
        data = {"username": current_user, "conversation_id": conversation_id}
        response = requests.post(f"{SERVER_URL}/api/conversation/delete", json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("success", False)
        return False
        
    except requests.exceptions.RequestException:
        return False

def show_conversation_menu():
    """Show menu for conversation management"""
    has_conversation = user_login()
    
    if has_conversation:
        while True:
            print(f"\n{YELLOW}=== Conversation Menu ==={RESET}")
            print("1. Continue most recent chat")
            print("2. List all conversations")
            print("3. Start new conversation")
            print("4. Exit")
            
            choice = input("\nChoose option (1-4): ").strip()
            
            if choice == "1":
                # Show conversation summary first
                show_conversation_summary()
                if load_conversation():
                    print(f"Continuing with {len(conversation_history)} previous messages.")
                    return True
                else:
                    print("Failed to load conversation. Starting new one.")
                    return False
                    
            elif choice == "2":
                # List all conversations
                conversations = list_conversations()
                if not conversations:
                    print("No conversations found.")
                    continue
                
                print(f"\n{GREEN}=== Your Conversations ==={RESET}")
                for i, conv in enumerate(conversations, 1):
                    print(f"{i}. {conv['title']} ({conv['message_count']} messages) - {conv['updated_at']}")
                
                print(f"\n{len(conversations) + 1}. Go back to main menu")
                
                while True:
                    try:
                        conv_choice = input(f"\nSelect conversation (1-{len(conversations) + 1}) or 'delete <number>' to delete: ").strip()
                        
                        if conv_choice.startswith('delete '):
                            # Delete conversation
                            try:
                                del_num = int(conv_choice.split()[1])
                                if 1 <= del_num <= len(conversations):
                                    conv_to_delete = conversations[del_num - 1]
                                    confirm = input(f"Delete '{conv_to_delete['title']}'? (y/N): ").strip().lower()
                                    if confirm == 'y':
                                        if delete_conversation(conv_to_delete['id']):
                                            print(f"{GREEN}Conversation deleted successfully.{RESET}")
                                            break  # Go back to conversation list
                                        else:
                                            print(f"{RED}Failed to delete conversation.{RESET}")
                                    else:
                                        print("Deletion cancelled.")
                                else:
                                    print("Invalid conversation number.")
                            except (ValueError, IndexError):
                                print("Invalid delete command. Use 'delete <number>'")
                            continue
                        
                        conv_num = int(conv_choice)
                        if conv_num == len(conversations) + 1:
                            break  # Go back to main menu
                        elif 1 <= conv_num <= len(conversations):
                            selected_conv = conversations[conv_num - 1]
                            if select_conversation(selected_conv['id']):
                                print(f"Loaded conversation: {selected_conv['title']}")
                                print(f"Messages: {len(conversation_history)}")
                                return True
                            else:
                                print("Failed to load conversation.")
                                break
                        else:
                            print(f"Invalid choice. Please enter 1-{len(conversations) + 1}")
                    except ValueError:
                        print("Please enter a valid number or 'delete <number>'")
                
            elif choice == "3":
                # Clear conversation on server
                if clear_conversation():
                    print("Starting new conversation.")
                else:
                    print("Warning: Failed to clear old conversation.")
                return False
                
            elif choice == "4":
                print("Goodbye!")
                sys.exit(0)
                
            else:
                print("Invalid choice. Please enter 1-4.")
    else:
        print("No previous conversation found. Starting new conversation.")
        return False

def chat(prompt):
    """Send message to chat server"""
    global stop_animation, conversation_history
    
    if not current_user:
        return "Error: No user logged in"
    
    # Start animation in background
    stop_animation = False
    thread = threading.Thread(target=loading)
    thread.start()

    try:
        # Send to chat server
        data = {
            "username": current_user,
            "message": prompt,
            "conversation_history": conversation_history
        }
        
        response = requests.post(f"{SERVER_URL}/api/chat", json=data, timeout=240)
        
        # Stop animation
        stop_animation = True
        thread.join()
        print("\r", end="")  # clear line
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                ai_response = result["response"]
                conversation_history = result["conversation_history"]
                return ai_response
            else:
                return f"{RED}Error: {result.get('error', 'Unknown error')}{RESET}"
        elif response.status_code == 503:
            return f"{RED}Error: Nova AI is offline{RESET}"
        elif response.status_code == 504:
            return f"{RED}Error: Request timeout{RESET}"
        else:
            return f"{RED}Error: Server returned {response.status_code}{RESET}"
            
    except requests.exceptions.ConnectionError:
        stop_animation = True
        thread.join()
        print("\r", end="")
        return f"{RED}Error: Cannot connect to chat server{RESET}"
    except requests.exceptions.Timeout:
        stop_animation = True
        thread.join()
        print("\r", end="")
        return f"{RED}Error: Request timeout{RESET}"
    except Exception as e:
        stop_animation = True
        thread.join()
        print("\r", end="")
        return f"{RED}Error: {str(e)}{RESET}"

if __name__ == "__main__":
    # Check server status before starting
    check_server_status()
    
    # Show conversation menu and login
    show_conversation_menu()
    
    print(f"\n{GREEN}Connected to Chat Server. Type 'exit' to quit.{RESET}")
    print(f"Commands: 'clear' (new conversation), 'list' (manage conversations), 'help' (show commands)\n")
    
    while True:
        user_input = input(f"{current_user}: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        elif user_input.lower() == "clear":
            if clear_conversation():
                conversation_history.clear()
                print(f"{YELLOW}Conversation cleared. Starting fresh.{RESET}\n")
            else:
                print(f"{RED}Failed to clear conversation on server.{RESET}\n")
            continue
        elif user_input.lower() == "list":
            # Show conversation management
            conversations = list_conversations()
            if not conversations:
                print("No conversations found.")
                continue
            
            print(f"\n{GREEN}=== Your Conversations ==={RESET}")
            for i, conv in enumerate(conversations, 1):
                print(f"{i}. {conv['title']} ({conv['message_count']} messages) - {conv['updated_at']}")
            
            while True:
                try:
                    action = input(f"\nEnter 'load <number>', 'delete <number>', or 'back': ").strip()
                    
                    if action.lower() == 'back':
                        break
                    elif action.startswith('load '):
                        conv_num = int(action.split()[1])
                        if 1 <= conv_num <= len(conversations):
                            selected_conv = conversations[conv_num - 1]
                            if select_conversation(selected_conv['id']):
                                print(f"{GREEN}Loaded: {selected_conv['title']}{RESET}")
                                print(f"Messages loaded: {len(conversation_history)}\n")
                                break
                            else:
                                print(f"{RED}Failed to load conversation.{RESET}")
                        else:
                            print("Invalid conversation number.")
                    elif action.startswith('delete '):
                        conv_num = int(action.split()[1])
                        if 1 <= conv_num <= len(conversations):
                            conv_to_delete = conversations[conv_num - 1]
                            confirm = input(f"Delete '{conv_to_delete['title']}'? (y/N): ").strip().lower()
                            if confirm == 'y':
                                if delete_conversation(conv_to_delete['id']):
                                    print(f"{GREEN}Conversation deleted.{RESET}")
                                    # Refresh the list
                                    conversations = list_conversations()
                                    if not conversations:
                                        print("No more conversations.")
                                        break
                                    print(f"\n{GREEN}=== Your Conversations ==={RESET}")
                                    for i, conv in enumerate(conversations, 1):
                                        print(f"{i}. {conv['title']} ({conv['message_count']} messages) - {conv['updated_at']}")
                                else:
                                    print(f"{RED}Failed to delete conversation.{RESET}")
                            else:
                                print("Deletion cancelled.")
                        else:
                            print("Invalid conversation number.")
                    else:
                        print("Use 'load <number>', 'delete <number>', or 'back'")
                except (ValueError, IndexError):
                    print("Invalid command format.")
            continue
        elif user_input.lower() == "help":
            print(f"\n{YELLOW}=== Available Commands ==={RESET}")
            print("exit/quit - Exit the chat")
            print("clear - Start a new conversation (clears current)")
            print("list - Manage your conversations (load/delete)")
            print("help - Show this help message")
            print("")
            continue
            
        reply = chat(user_input)
        print(f"AI: {BLUE}{reply}{RESET}\n")
