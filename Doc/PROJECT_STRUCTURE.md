# 📁 DebugBot Project Structure

## Directory Layout

```
debugbot/
├── 📄 README.md                    # Main documentation
├── 📄 LICENSE                      # MIT License
├── 📄 CONTRIBUTING.md              # Contribution guidelines
├── 📄 CHANGELOG.md                 # Version history
├── 📄 requirements.txt             # Python dependencies
├── 📄 .gitignore                   # Git ignore rules
│
├── 🐍 app.py                       # Main Flask backend
│
├── 📁 static/                      # Static files
│   ├── index.html                  # Participant chat interface
│   ├── admin.html                  # Admin dashboard
│   └── credentials.html            # Printable credential sheet
│
├── 📁 docs/                        # Documentation
│   ├── INSTALLATION.md             # Installation guide
│   ├── LAN_SETUP.md                # LAN deployment guide
│   ├── TROUBLESHOOTING.md          # Troubleshooting guide
│   ├── ADMIN.md                    # Admin guide
│   ├── TEAMS.md                    # Team guide
│   └── API.md                      # API reference
│
├── 📁 scripts/                     # Helper scripts
│   ├── start_debugbot.bat          # Windows launcher
│   ├── check_setup.bat             # System diagnostics
│   └── install_dependencies.bat    # Package installer
│
├── 📁 templates/                   # Printable templates
│   ├── access_poster.html          # Access instructions poster
│   ├── qr_code_generator.html      # QR code generator
│   └── credential_cards.html       # Team credential cards
│
└── 📁 tests/                       # Test files (optional)
    ├── test_auth.py                # Authentication tests
    ├── test_chat.py                # Chat functionality tests
    └── test_admin.py               # Admin panel tests
```

## File Descriptions

### Core Files

#### `app.py`
Main Flask application containing:
- Team authentication
- Admin authentication
- Chat endpoint with Ollama integration
- Request filtering logic
- Admin routes
- Session management

**Key components:**
```python
TEAMS = {}                  # Team credentials
ADMIN_USERNAME = "admin"    # Admin username
ADMIN_PASSWORD = ""         # Admin password
MODEL_NAME = ""             # Ollama model name
SYSTEM_PROMPT = ""          # AI system prompt
chat_history = {}           # In-memory chat storage
```

#### `index.html`
Participant chat interface:
- Login form
- Chat messages display
- Message input
- Real-time updates
- Session management

#### `admin.html`
Admin dashboard:
- Admin login
- Team credentials viewer
- Chat logs monitor
- Statistics display
- Search and filter

### Documentation Files

#### `README.md`
Complete project documentation including:
- Overview and features
- Installation instructions
- Configuration guide
- Usage examples
- API documentation
- Troubleshooting

#### `CONTRIBUTING.md`
Guidelines for contributors:
- Code of conduct
- Development setup
- Pull request process
- Style guidelines
- Testing requirements

#### `CHANGELOG.md`
Version history and release notes:
- Features added
- Bugs fixed
- Breaking changes
- Upgrade notes

### Configuration Files

#### `requirements.txt`
Python package dependencies:
```
flask==3.0.0
flask-cors==4.0.0
requests==2.31.0
gunicorn==21.2.0
python-dotenv==1.0.0
```

#### `.gitignore`
Git exclusion rules:
- Python cache files
- Virtual environments
- IDE files
- Log files
- Environment variables

### Helper Scripts

#### `start_debugbot.bat`
Windows batch launcher:
- Checks Python installation
- Verifies Ollama is running
- Displays connection info
- Starts Flask backend

#### `check_setup.bat`
System diagnostics:
- Verifies Python
- Checks pip
- Tests Flask installation
- Validates Ollama
- Confirms model availability

#### `install_dependencies.bat`
Automatic installer:
- Upgrades pip
- Installs Flask
- Installs dependencies
- Verifies installations

### Template Files

#### `access_poster.html`
Printable access instructions:
- Step-by-step guide
- URL and WiFi info
- Editable fields
- Print-friendly layout

#### `qr_code_generator.html`
QR code creator:
- Input IP address
- Generate QR code
- Download as image
- Display for scanning

#### `credential_cards.html`
Team credentials:
- All 30 teams
- Printable cards
- Cut guidelines
- Instructions

## Data Flow

```
1. Team Login
   index.html → /api/login → app.py → Session created

2. Chat Message
   index.html → /api/chat → is_debug_request() → Ollama API → Response

3. Admin Access
   admin.html → /api/admin/login → app.py → Admin session

4. View Logs
   admin.html → /api/admin/chat-logs → app.py → Returns chat_history
```

## Important Directories

### `/static/`
Served by Flask. Contains all frontend HTML files accessible via browser.

### `/docs/`
Detailed documentation for different use cases and scenarios.

### `/scripts/`
Windows batch files for easy setup and operation.

### `/templates/`
Printable resources for hackathon organization.

### `/tests/` (optional)
Unit and integration tests for quality assurance.

## Configuration Points

### 1. Team Credentials
**Location:** `app.py` → `TEAMS` dictionary  
**Format:** `{"TEAM-ID": "password"}`

### 2. Admin Password
**Location:** `app.py` → `ADMIN_PASSWORD`  
**Default:** `Hackathon@2026` (⚠️ CHANGE THIS!)

### 3. AI Model
**Location:** `app.py` → `MODEL_NAME`  
**Options:** `codellama`, `codellama:7b`, `llama3.2:3b`

### 4. Request Filtering
**Location:** `app.py` → `is_debug_request()` function  
**Customize:** Add/remove keywords

### 5. Network Settings
**Location:** `app.py` → `app.run()`  
**LAN mode:** `host='0.0.0.0'`

## Customization Guide

### Adding More Teams

Edit `app.py`:
```python
TEAMS = {
    # ... existing teams ...
    "HACK-A31": "newPassword123",
    "HACK-A32": "anotherPass456",
}
```

### Changing UI Theme

Edit `index.html` or `admin.html`:
```css
/* Find gradient in <style> section */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Change to your colors */
background: linear-gradient(135deg, #yourColor1, #yourColor2);
```

### Adding New Admin Features

1. Add route in `app.py`:
```python
@app.route('/api/admin/new-feature', methods=['GET'])
@admin_required
def new_feature():
    return jsonify({"data": "your data"})
```

2. Add frontend in `admin.html`:
```javascript
async function loadNewFeature() {
    const res = await fetch(`${API_URL}/api/admin/new-feature`);
    const data = await res.json();
    // Process data
}
```

## Deployment Considerations

### Local Development
- Use default `host='127.0.0.1'`
- Debug mode ON
- Single user testing

### Hackathon (LAN)
- Use `host='0.0.0.0'`
- Debug mode ON (for troubleshooting)
- Multiple concurrent users
- Monitor admin panel

### Production (Cloud)
- Use production WSGI server (Gunicorn)
- Debug mode OFF
- Environment variables for secrets
- Reverse proxy (Nginx)
- HTTPS enabled

## Security Notes

### Sensitive Files
- `app.py` - Contains passwords (change defaults!)
- `.env` - Environment variables (don't commit!)

### Public Files
- `index.html` - Participant interface
- `admin.html` - Admin interface (password protected)
- Documentation files

### Best Practices
1. Change admin password before deployment
2. Use strong, unique passwords
3. Don't commit credentials to Git
4. Use environment variables for production
5. Enable HTTPS for production deployments

## Maintenance

### Regular Updates
- [ ] Update Python dependencies
- [ ] Update Ollama models
- [ ] Review team credentials
- [ ] Check for security updates

### Before Each Hackathon
- [ ] Test all functionality
- [ ] Update team credentials
- [ ] Change admin password
- [ ] Test on LAN
- [ ] Print materials

### After Each Hackathon
- [ ] Review chat logs for improvements
- [ ] Gather feedback
- [ ] Document issues
- [ ] Plan enhancements

---

**This structure is optimized for ease of use, maintenance, and deployment at hackathon events.**