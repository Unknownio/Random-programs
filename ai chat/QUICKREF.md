# Quick Reference - Nova AI Chat

## 🚀 Get Started in 30 Seconds

```bash
python quickstart.py
```
That's it! This command will:
- Install all dependencies automatically
- Set up configuration
- Start the chat server
- Guide you to connect the client

## 📁 What Each File Does

| File | Purpose |
|------|---------|
| `quickstart.py` | **START HERE** - One command setup |
| `install.py` | Complete automatic installer |
| `run.py` | Universal launcher (all platforms) |
| `scripts/quickstart.py` | One-command setup |
| `scripts/setup.py` | Interactive configuration |
| `launch_server.py` | Start the chat server |
| `launch_client.py` | Start the chat client |
| `scripts/network_test.py` | Test connectivity |
| `start_server.bat/.sh` | Platform startup scripts |

## 🔧 Common Commands

```bash
# First time setup
python scripts/quickstart.py

# Universal launcher (easiest)
python run.py

# Configure Nova AI connection  
python scripts/setup.py

# Test connectivity
python scripts/network_test.py

# Start manually
python launch_server.py    # Terminal 1
python launch_client.py    # Terminal 2

# Platform-specific shortcuts
./start_server.sh          # Mac/Linux
start_server.bat           # Windows
```

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Nova AI is offline" | Start LM Studio and load a model |
| "Connection refused" | Check IP address in config.json |
| "Module not found" | Run `python install.py` |
| Server won't start | Check if port 8080 is free |

## 💡 Pro Tips

- Keep LM Studio running while using the chat
- Use `python scripts/network_test.py` to diagnose issues
- Edit `config.json` to change IP addresses/ports
- See `README.md` for complete documentation

---
🤖 **Nova AI Chat** - Tested with LM Studio
