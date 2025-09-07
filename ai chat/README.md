# AI Chat Application with Nova AI Integration

A complete chat application that integrates with Nova AI for local AI conversations. Features include user authentication, conversation history, and a simple terminal-based interface.

> **Note**: This application was developed and tested using LM Studio as the Nova AI backend.

## 🚀 Features

- **Local AI Integration**: Connect to your Nova AI instance for private AI conversations
- **User Authentication**: Secure login and registration system
- **Conversation History**: Persistent chat history stored in SQLite database
- **Multi-user Support**: Multiple users can have separate conversation histories
- **Auto-dependency Installation**: Automatically installs required Python packages
- **Cross-platform**: Works on Windows, macOS, and Linux

## 📋 Prerequisites

- **Python 3.6+** installed on your system
- **Nova AI** (LM Studio) installed and running with a loaded model
- **Network access** between the chat server and Nova AI

## 🛠 Installation & Setup

### One-Command Install (Easiest)

For the fastest setup, run:
```bash
python scripts/quickstart.py
```
This automatically installs everything, configures the app, and starts the server!

### Automatic Installation

For complete automatic setup:
```bash
python scripts/install.py
```
This downloads and installs all dependencies, creates configuration files, and sets up startup scripts.

### Check System Requirements (Optional)

To verify your system is ready:
```bash
python scripts/check_requirements.py
```

### Manual Configuration

Run the interactive setup script:
```bash
python scripts/setup.py
```
This will guide you through the configuration process step by step.

### Manual Setup

#### Step 1: Configure Nova AI Connection

1. Open `config.json` and update the Nova AI settings:
   ```json
   {
     "lm_studio": {
2. Replace `YOUR_NOVA_AI_IP_HERE` with your Nova AI computer's IP address:
   - **Same computer**: Use `127.0.0.1` or `localhost`
   - **Different computer**: Use the IP address (e.g., `192.168.1.100`)

#### Step 2: Start Nova AI
       "port": 8080
     }
   }
   ```
4. Verify the server is running by visiting `http://YOUR_IP:1234` in a browser

#### Step 3: Run the Application7.0.0.1` or `localhost`
   - **Different computer**: Use the IP address (e.g., `192.168.1.100`)

### Step 2: Start Nova AI

1. Launch Nova AI (LM Studio) on your target machine
2. Load your preferred AI model
3. Start the server (usually runs on port 1234)
4. Verify the server is running by visiting `http://YOUR_IP:1234` in a browser

### Step 3: Run the Application

#### Option A: Universal Launcher (Easiest)
```bash
# Cross-platform launcher with menu
python run.py
```
Choose to start server, client, or both from an interactive menu.

#### Option B: Platform-Specific Scripts

**Windows:**
```batch
# Double-click these files or run in terminal:
start_server.bat
start_client.bat
```

**macOS/Linux:**
```bash
# Make executable and run:
./start_server.sh
./start_client.sh
```

#### Option C: Manual Launch
```bash
# Start the server
python launch_server.py        # Windows
python3 launch_server.py       # macOS/Linux

# In another terminal, start the client
python launch_client.py        # Windows  
python3 launch_client.py       # macOS/Linux
```

## 🔧 Configuration

### config.json Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `lm_studio.host` | IP address of Nova AI server | `127.0.0.1` |
| `lm_studio.port` | Port number for Nova AI | `1234` |
| `server.host` | Chat server bind address | `0.0.0.0` |
| `server.port` | Chat server port | `8080` |

### Network Configuration

- **Local Setup**: Set Nova AI host to `127.0.0.1`
- **Network Setup**: Set Nova AI host to the IP address of the computer running Nova AI
- **Firewall**: Ensure ports 1234 (Nova AI) and 8080 (Chat Server) are open

## 🎮 Usage

### First Time Setup
1. Run the client: `python launch_client.py`
2. Create a new account when prompted
```
nova-ai-chat/
├── README.md                 # This file
├── LICENSE                   # MIT License
├── quickstart.py            # One-command install & run
├── install.py               # Complete automatic installer
├── README.md                 # This file
├── LICENSE                   # MIT License
├── config.json              # Configuration file
├── requirements.txt          # Python dependencies
├── chat_server.py           # Main server application
├── chat_client.py           # Terminal chat client
├── launch_server.py         # Server launcher with auto-setup
├── launch_client.py         # Client launcher with auto-setup
├── scripts/                 # Utility scripts folder
│   ├── install.py           # Complete installation script
│   ├── quickstart.py        # One-command setup and launch
│   ├── setup.py             # Interactive configuration script
│   ├── network_test.py      # Network connectivity tester
│   └── check_requirements.py # System requirements checker
├── start_server.bat/.sh     # OS-specific startup scripts (auto-created)
├── start_client.bat/.sh     # OS-specific startup scripts (auto-created)
├── chat_database.db         # SQLite database (created automatically)
└── conversation_history.json # Backup conversation file
```

## 🔍 Troubleshooting

### Connection Issues

1. **Test Network Connectivity**:
   ```bash
   python scripts/network_test.py
   ```

2. **Common Issues**:
   - **Nova AI not running**: Start Nova AI (LM Studio) and load a model
   - **Wrong IP address**: Update `config.json` with correct IP
   - **Firewall blocking**: Open ports 1234 and 8080
   - **Model not loaded**: Load a model in Nova AI before connecting

### Error Messages

| Error | Solution |
|-------|----------|
| "Nova AI is offline" | Check Nova AI (LM Studio) is running and accessible |
| "Connection refused" | Verify IP address and port in config.json |
| "Username already exists" | Try a different username or login |
| "Database error" | Delete `chat_database.db` to reset |

## 🌐 Deployment Options

### Local Network Deployment
1. Run the server on one computer
2. Update client configurations to point to server IP
3. Ensure all computers are on the same network

### Cloud Deployment
1. Deploy server to cloud instance (AWS, DigitalOcean, etc.)
2. Update security groups/firewall rules
3. Use public IP or domain name in client configuration
4. Consider using HTTPS in production

## 🔒 Security Notes

- **Passwords**: Stored as SHA-256 hashes (consider upgrading to bcrypt for production)
- **Network**: No encryption between client and server (consider adding SSL/TLS)
- **Database**: SQLite file should be protected with appropriate file permissions
- **API Keys**: Nova AI connection is local by default (no API keys required)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 💡 Tips

- Keep Nova AI (LM Studio) running while using the chat application
- Use descriptive usernames to manage multiple users
- Clear conversation history if you want to start fresh
- Test network connectivity before reporting issues
- Consider the AI model's context window for long conversations

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Run `python scripts/network_test.py` to diagnose connectivity
3. Check Nova AI (LM Studio) logs for errors
4. Create an issue with error details and system information

---

**Note**: This application is designed for local/private use with Nova AI. Tested and developed using LM Studio as the backend. For production deployments, consider additional security measures like authentication tokens, HTTPS, and proper database security.
