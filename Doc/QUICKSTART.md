# ⚡ DebugBot - Quick Start Guide

Get DebugBot running in **5 minutes**!

## 🎯 Prerequisites

- ✅ Python 3.10+ installed
- ✅ Windows 10/11, macOS, or Linux
- ✅ 8GB+ RAM

## 🚀 Installation (3 Steps)

### Step 1: Install Ollama

**Windows:**
```powershell
# Download from https://ollama.com/download/windows
# Run installer
```

**macOS/Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Step 2: Download AI Model

```bash
ollama pull llama3.2:3b
```

### Step 3: Install Python Packages

```bash
pip install flask flask-cors requests
```

## ▶️ Run DebugBot

```bash
# Clone or download repository
cd debugbot

# Start backend
python app.py
```

You should see:
```
🤖 DebugBot Backend Starting...
✅ Access DebugBot at: http://localhost:5000
```

## 🎮 Test It

1. **Open browser:** `http://localhost:5000`
2. **Login:**
   - Team ID: `HACK-A01`
   - Password: `xK9mP2nQ7vL4`
3. **Ask:** "Why am I getting IndexError?"
4. **DebugBot responds!** ✅

## 👨‍💼 Access Admin Panel

1. **Open:** `http://localhost:5000/admin`
2. **Login:**
   - Username: `admin`
   - Password: `Hackathon@2026`
3. **Monitor all teams!** 📊

## ⚙️ Quick Configuration

### Change Admin Password

Edit `app.py` (line ~45):
```python
ADMIN_PASSWORD = "YourNewPassword123!"
```

### Enable LAN Access

Edit `app.py` (last line):
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

Find your IP:
```bash
ipconfig  # Windows
ifconfig  # Mac/Linux
```

Share: `http://YOUR_IP:5000`

## 🐛 Troubleshooting

### "Cannot connect to Ollama"
```bash
ollama serve
```

### "Port 5000 in use"
Change port in `app.py`:
```python
app.run(debug=True, port=5001)
```

### "Slow responses"
Use faster model:
```bash
ollama pull llama3.2:3b
```

## 📚 Next Steps

- [ ] Read [full README](README.md)
- [ ] Configure [LAN setup](docs/LAN_SETUP.md)
- [ ] Print [credential cards](templates/credential_cards.html)
- [ ] Review [admin guide](docs/ADMIN.md)

## 🎉 You're Ready!

**DebugBot is running!** Start your hackathon with AI-powered debugging assistance.

Need help? Check [troubleshooting guide](docs/TROUBLESHOOTING.md)

---

**Total time: ~5 minutes** ⏱️