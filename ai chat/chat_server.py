#!/usr/bin/env python3
import sys
import subprocess
import importlib

def check_and_install_pip():
    """Check if pip is available and install if missing"""
    try:
        import pip
        print("[SERVER SETUP] ✓ pip is available")
        return True
    except ImportError:
        print("[SERVER SETUP] pip not found. Attempting to install...")
        try:
            # Try to install pip using get-pip.py method
            subprocess.check_call([sys.executable, "-m", "ensurepip", "--default-pip"])
            print("[SERVER SETUP] ✓ pip installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("[SERVER SETUP] ✗ Failed to install pip automatically")
            print("Please install pip manually: https://pip.pypa.io/en/stable/installation/")
            return False

def install_package(package_name):
    """Install a package using pip"""
    try:
        print(f"[SERVER SETUP] Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name, "--quiet"])
        print(f"[SERVER SETUP] ✓ {package_name} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[SERVER SETUP] ✗ Failed to install {package_name}: {e}")
        return False

def check_and_install_dependencies():
    """Check and install required dependencies"""
    required_packages = ["flask", "requests"]
    
    print("[SERVER SETUP] Checking dependencies...")
    
    # Check pip first
    if not check_and_install_pip():
        return False
    
    missing_packages = []
    
    # Check each required package
    for package in required_packages:
        try:
            if package == "flask":
                importlib.import_module("flask")
            else:
                importlib.import_module(package)
            print(f"[SERVER SETUP] ✓ {package} is available")
        except ImportError:
            print(f"[SERVER SETUP] {package} not found")
            missing_packages.append(package)
    
    # Install missing packages
    if missing_packages:
        print(f"[SERVER SETUP] Installing missing packages: {', '.join(missing_packages)}")
        for package in missing_packages:
            if not install_package(package):
                print(f"[SERVER SETUP] ✗ Failed to install {package}")
                return False
        print("[SERVER SETUP] ✓ All dependencies installed successfully")
        
        # Reload modules after installation
        for package in missing_packages:
            try:
                if package == "flask":
                    importlib.import_module("flask")
                else:
                    importlib.import_module(package)
            except ImportError:
                print(f"[SERVER SETUP] ✗ Still cannot import {package} after installation")
                return False
    else:
        print("[SERVER SETUP] ✓ All dependencies are already available")
    
    return True

# Install dependencies automatically
print("=== Chat Server Starting ===")
if not check_and_install_dependencies():
    print("[SERVER SETUP] ✗ Dependency installation failed. Exiting...")
    sys.exit(1)

# Now import the required modules
from flask import Flask, request, jsonify
import requests
import sqlite3
import json
import os
import threading
import time
import hashlib
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
            print("[SERVER] Warning: config.json not found, using default values")
            return {
                "lm_studio": {"host": "127.0.0.1", "port": 1234, "api_path": "/v1/chat/completions", "health_path": "/health"},
                "server": {"host": "0.0.0.0", "port": 8080},
                "database": {"file": "chat_database.db"},
                "security": {"password_min_length": 4}
            }
    except Exception as e:
        print(f"[SERVER] Error loading config: {e}, using defaults")
        return {
            "lm_studio": {"host": "127.0.0.1", "port": 1234, "api_path": "/v1/chat/completions", "health_path": "/health"},
            "server": {"host": "0.0.0.0", "port": 8080},
            "database": {"file": "chat_database.db"},
            "security": {"password_min_length": 4}
        }

# Load configuration
config = load_config()

# Database configuration
DB_FILE = config["database"]["file"]

# LM Studio API endpoints (configurable via config.json)
LM_STUDIO_API_URL = f"http://{config['lm_studio']['host']}:{config['lm_studio']['port']}{config['lm_studio']['api_path']}"
LM_STUDIO_HEALTH_URL = f"http://{config['lm_studio']['host']}:{config['lm_studio']['port']}{config['lm_studio']['health_path']}"

app = Flask(__name__)

def init_database():
    """Initialize the SQLite database"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, DB_FILE)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Check if password_hash column exists and add it if missing
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'password_hash' not in columns:
            cursor.execute('ALTER TABLE users ADD COLUMN password_hash TEXT')
            print("[SERVER] Database migrated: Added password_hash column")
        
        # Create conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                messages TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print(f"[SERVER] Database initialized at: {db_path}")
        return True
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

def check_lm_studio():
    """Check if LM Studio is online by testing API endpoint instead of /health"""
    try:
        # Test with a minimal API call instead of /health to avoid error logs
        test_payload = {
            "model": "local-model",
            "messages": [{"role": "system", "content": "test"}],
            "max_tokens": 1,
            "temperature": 0
        }
        response = requests.post(LM_STUDIO_API_URL, json=test_payload, timeout=3)
        # Any response (even error) means LM Studio is running
        return response.status_code in [200, 400, 422, 500]
    except requests.exceptions.RequestException:
        pass
    return False

@app.route('/api/health', methods=['GET'])
def health_check():
    """Check server health (Nova AI status checked only when needed)"""
    # Don't automatically check LM Studio to avoid unnecessary calls/logs
    return jsonify({
        "server": "online",
        "nova_ai": "unknown",  # Status checked during actual chat requests
        "timestamp": datetime.now().isoformat()
    })

def hash_password(password):
    """Hash password with SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/api/user/register', methods=['POST'])
def user_register():
    """Register a new user"""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    if len(password) < 4:
        return jsonify({"error": "Password must be at least 4 characters"}), 400
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, DB_FILE)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            conn.close()
            return jsonify({"error": "Username already exists"}), 400
        
        # Hash password and create user
        password_hash = hash_password(password)
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', 
                      (username, password_hash))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            "success": True,
            "message": "User registered successfully"
        })
        
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@app.route('/api/user/login', methods=['POST'])
def user_login():
    """Login existing user"""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, DB_FILE)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Find user and verify password
        cursor.execute('SELECT id, password_hash, created_at FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return jsonify({"error": "Invalid username or password"}), 401
        
        user_id, stored_password_hash, created_at = user
        
        # Handle legacy users without passwords
        if stored_password_hash is None:
            # Set password for legacy user
            password_hash = hash_password(password)
            cursor.execute('UPDATE users SET password_hash = ? WHERE id = ?', (password_hash, user_id))
            conn.commit()
            print(f"[SERVER] Set password for legacy user: {username}")
        else:
            # Verify password
            provided_password_hash = hash_password(password)
            if provided_password_hash != stored_password_hash:
                conn.close()
                return jsonify({"error": "Invalid username or password"}), 401
        
        # Check if user has conversations
        cursor.execute('SELECT COUNT(*) FROM conversations WHERE user_id = ?', (user_id,))
        conversation_count = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            "success": True,
            "user_id": user_id,
            "username": username,
            "created_at": created_at,
            "has_conversations": conversation_count > 0,
            "is_new_user": conversation_count == 0
        })
            
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@app.route('/api/conversation/load', methods=['POST'])
def load_conversation():
    """Load user's conversation history"""
    data = request.get_json()
    username = data.get('username', '').strip()
    
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, DB_FILE)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get user's most recent conversation
        cursor.execute('''
            SELECT c.messages, c.updated_at 
            FROM conversations c
            JOIN users u ON c.user_id = u.id
            WHERE u.username = ?
            ORDER BY c.updated_at DESC
            LIMIT 1
        ''', (username,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            messages_json, timestamp = row
            messages = json.loads(messages_json)
            
            return jsonify({
                "success": True,
                "messages": messages,
                "updated_at": timestamp
            })
        else:
            return jsonify({
                "success": True,
                "messages": [],
                "updated_at": None
            })
            
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@app.route('/api/conversation/clear', methods=['POST'])
def clear_conversation():
    """Clear user's conversation history"""
    data = request.get_json()
    username = data.get('username', '').strip()
    
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, DB_FILE)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Delete all conversations for this user
        cursor.execute('''
            DELETE FROM conversations 
            WHERE user_id = (SELECT id FROM users WHERE username = ?)
        ''', (username,))
        
        conn.commit()
        conn.close()
        
        return jsonify({"success": True})
        
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@app.route('/api/conversation/list', methods=['POST'])
def list_conversations():
    """List all conversations for a user"""
    data = request.get_json()
    username = data.get('username', '').strip()
    
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, DB_FILE)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all conversations for user
        cursor.execute('''
            SELECT c.id, c.messages, c.updated_at 
            FROM conversations c
            JOIN users u ON c.user_id = u.id
            WHERE u.username = ?
            ORDER BY c.updated_at DESC
        ''', (username,))
        
        conversations = []
        for row in cursor.fetchall():
            conv_id, messages_json, timestamp = row
            messages = json.loads(messages_json)
            
            # Get first user message as title
            title = "Empty conversation"
            for msg in messages:
                if msg["role"] == "user":
                    title = msg["content"][:50] + "..." if len(msg["content"]) > 50 else msg["content"]
                    break
            
            conversations.append({
                "id": conv_id,
                "title": title,
                "message_count": len(messages),
                "updated_at": timestamp
            })
        
        conn.close()
        
        return jsonify({
            "success": True,
            "conversations": conversations
        })
        
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@app.route('/api/conversation/select', methods=['POST'])
def select_conversation():
    """Load a specific conversation by ID"""
    data = request.get_json()
    username = data.get('username', '').strip()
    conversation_id = data.get('conversation_id')
    
    if not username or not conversation_id:
        return jsonify({"error": "Username and conversation_id are required"}), 400
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, DB_FILE)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get specific conversation
        cursor.execute('''
            SELECT c.messages, c.updated_at 
            FROM conversations c
            JOIN users u ON c.user_id = u.id
            WHERE u.username = ? AND c.id = ?
        ''', (username, conversation_id))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            messages_json, timestamp = row
            messages = json.loads(messages_json)
            
            return jsonify({
                "success": True,
                "messages": messages,
                "updated_at": timestamp
            })
        else:
            return jsonify({"error": "Conversation not found"}), 404
        
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@app.route('/api/conversation/delete', methods=['POST'])
def delete_conversation():
    """Delete a specific conversation by ID"""
    data = request.get_json()
    username = data.get('username', '').strip()
    conversation_id = data.get('conversation_id')
    
    if not username or not conversation_id:
        return jsonify({"error": "Username and conversation_id are required"}), 400
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, DB_FILE)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Delete specific conversation (ensure it belongs to the user)
        cursor.execute('''
            DELETE FROM conversations 
            WHERE id = ? AND user_id = (
                SELECT id FROM users WHERE username = ?
            )
        ''', (conversation_id, username))
        
        if cursor.rowcount > 0:
            conn.commit()
            conn.close()
            return jsonify({
                "success": True,
                "message": "Conversation deleted successfully"
            })
        else:
            conn.close()
            return jsonify({"error": "Conversation not found or not owned by user"}), 404
        
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    data = request.get_json()
    username = data.get('username', '').strip()
    message = data.get('message', '').strip()
    conversation_history = data.get('conversation_history', [])
    
    if not username or not message:
        return jsonify({"error": "Username and message are required"}), 400
    
    # Check if LM Studio is online
    if not check_lm_studio():
        return jsonify({"error": "LM Studio is offline"}), 503
    
    # Prepare conversation history for LM Studio
    messages = conversation_history.copy()
    messages.append({"role": "user", "content": message})
    
    try:
        # Send to LM Studio
        payload = {
            "model": "local-model",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        response = requests.post(LM_STUDIO_API_URL, json=payload, timeout=180)
        
        if response.status_code != 200:
            return jsonify({"error": f"LM Studio error: {response.status_code}"}), 500
        
        result = response.json()
        ai_response = result["choices"][0]["message"]["content"]
        
        # Add AI response to history
        conversation_history.append({"role": "user", "content": message})
        conversation_history.append({"role": "assistant", "content": ai_response})
        
        # Prepare response immediately
        response_data = {
            "success": True,
            "response": ai_response,
            "conversation_history": conversation_history,
            "saved": True  # Assume success for immediate response
        }
        
        # Save to database asynchronously (don't wait for it)
        try:
            import threading
            save_thread = threading.Thread(
                target=save_conversation_to_db, 
                args=(username, conversation_history.copy())
            )
            save_thread.daemon = True
            save_thread.start()
        except Exception as e:
            print(f"Warning: Could not start database save thread: {e}")
        
        return jsonify(response_data)
        
    except requests.exceptions.Timeout:
        return jsonify({"error": "LM Studio request timeout"}), 504
    except Exception as e:
        return jsonify({"error": f"Chat error: {str(e)}"}), 500

def save_conversation_to_db(username, conversation_history):
    """Save conversation to database"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, DB_FILE)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get user ID
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_row = cursor.fetchone()
        if not user_row:
            conn.close()
            return False
        
        user_id = user_row[0]
        messages_json = json.dumps(conversation_history)
        
        # Update or insert conversation (replace current conversation)
        cursor.execute('DELETE FROM conversations WHERE user_id = ?', (user_id,))
        cursor.execute('''
            INSERT INTO conversations (user_id, messages, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (user_id, messages_json))
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error saving conversation: {e}")
        return False

@app.route('/api/conversation/summary', methods=['POST'])
def conversation_summary():
    """Get conversation summary"""
    data = request.get_json()
    username = data.get('username', '').strip()
    
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, DB_FILE)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get user's most recent conversation
        cursor.execute('''
            SELECT c.messages, c.updated_at 
            FROM conversations c
            JOIN users u ON c.user_id = u.id
            WHERE u.username = ?
            ORDER BY c.updated_at DESC
            LIMIT 1
        ''', (username,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            messages_json, timestamp = row
            messages = json.loads(messages_json)
            
            # Get last few messages for preview
            preview_messages = []
            for msg in messages[-6:]:  # Last 6 messages (3 exchanges)
                role = "You" if msg["role"] == "user" else "AI"
                content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
                preview_messages.append({"role": role, "content": content})
            
            return jsonify({
                "success": True,
                "timestamp": timestamp,
                "total_messages": len(messages),
                "preview_messages": preview_messages
            })
        else:
            return jsonify({
                "success": True,
                "timestamp": None,
                "total_messages": 0,
                "preview_messages": []
            })
            
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

if __name__ == "__main__":
    print("Starting Chat Server...")
    
    # Initialize database
    init_database()
    
    # Check Nova AI connection (using API test instead of /health to avoid error logs)
    if check_lm_studio():
        print("[SERVER] ✓ Connected to Nova AI")
    else:
        print("[SERVER] ⚠ Warning: Nova AI is offline")
    
    server_host = config["server"]["host"]
    server_port = config["server"]["port"]
    print(f"[SERVER] Starting HTTP server on http://{server_host}:{server_port}")
    print(f"[SERVER] Nova AI endpoint: {LM_STUDIO_API_URL}")
    app.run(host=server_host, port=server_port)
