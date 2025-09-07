#!/usr/bin/env python3
import requests
import time
import sys
import json
import os

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
            print("Warning: config.json not found, using default values")
            return {
                "lm_studio": {"host": "127.0.0.1", "port": 1234, "api_path": "/v1/chat/completions", "health_path": "/health"},
                "server": {"host": "127.0.0.1", "port": 8080}
            }
    except Exception as e:
        print(f"Error loading config: {e}, using defaults")
        return {
            "lm_studio": {"host": "127.0.0.1", "port": 1234, "api_path": "/v1/chat/completions", "health_path": "/health"},
            "server": {"host": "127.0.0.1", "port": 8080}
        }

# Load configuration and set network endpoints
config = load_config()
LM_STUDIO_API_URL = f"http://{config['lm_studio']['host']}:{config['lm_studio']['port']}{config['lm_studio']['api_path']}"
# For testing, use 127.0.0.1 if server host is 0.0.0.0 (since we're testing from the same machine)
server_host = config['server']['host'] if config['server']['host'] != "0.0.0.0" else "127.0.0.1"
CHAT_SERVER_URL = f"http://{server_host}:{config['server']['port']}/api/health"

def test_connection(url, name, timeout=10, is_lm_studio=False):
    """Test connection to a specific endpoint"""
    print(f"Testing {name}...")
    try:
        start_time = time.time()
        
        if is_lm_studio:
            # Test LM Studio with API call instead of /health to avoid error logs
            test_payload = {
                "model": "local-model", 
                "messages": [{"role": "system", "content": "test"}],
                "max_tokens": 1,
                "temperature": 0
            }
            response = requests.post(url, json=test_payload, timeout=timeout)
        else:
            response = requests.get(url, timeout=timeout)
            
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        if is_lm_studio:
            # For LM Studio, accept multiple status codes (200, 400, 422, 500 all mean it's running)
            if response.status_code in [200, 400, 422, 500]:
                print(f"  ✓ {name}: OK (Response time: {response_time:.0f}ms)")
                return True
            else:
                print(f"  ✗ {name}: Failed (Status {response.status_code})")
                return False
        elif response.status_code == 200:
            print(f"  ✓ {name}: OK (Response time: {response_time:.0f}ms)")
            return True
        else:
            print(f"  ✗ {name}: HTTP {response.status_code} (Response time: {response_time:.0f}ms)")
            return False
            
    except requests.exceptions.Timeout:
        print(f"  ✗ {name}: TIMEOUT (>{timeout}s)")
        return False
    except requests.exceptions.ConnectionError:
        print(f"  ✗ {name}: CONNECTION ERROR")
        return False
    except Exception as e:
        print(f"  ✗ {name}: ERROR - {str(e)}")
        return False



def main():
    print("=== Network Connectivity Test ===\n")
    
    # Test basic connectivity
    results = []
    results.append(test_connection(CHAT_SERVER_URL, "Chat Server", timeout=5))
    results.append(test_connection(LM_STUDIO_API_URL, "Nova AI (LM Studio)", timeout=5, is_lm_studio=True))
    
    print(f"\n=== Summary ===")
    if all(results):
        print("✓ All connections working properly")
    else:
        print("✗ Some connections have issues")
        print("\nTroubleshooting suggestions:")
        if not results[0]:
            print("- Chat server is not running or not accessible")
        if not results[2]:
            print("- Nova AI API is slow or not responding")
            print("- Try using a smaller model or increasing timeout values")
            print("- Check LM Studio performance and available memory")

if __name__ == "__main__":
    main()
