from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
import requests
import json
import secrets
from datetime import datetime
from functools import wraps
import os

app = Flask(__name__, static_folder='.')
app.secret_key = secrets.token_hex(32)
CORS(app, supports_credentials=True, origins=['http://localhost:5000'])

# ========================================
# TEAM CREDENTIALS (30 Teams)
# ========================================
# Format: HACK-A01 to HACK-A30 with unique passwords
TEAMS = {
    "HACK-A01": "xK9mP2nQ7vL4",
    "HACK-A02": "bR5wF8cJ3hN6",
    "HACK-A03": "tY2gV9xM1pD4",
    "HACK-A04": "qL7nK4wP9jR2",
    "HACK-A05": "fH3vB6mC8xT5",
    "HACK-A06": "zN1pW4kL7gQ9",
    "HACK-A07": "dM8cX2vF5nJ3",
    "HACK-A08": "rT6hK9wB4pL1",
    "HACK-A09": "jP3mN7gV2xC8",
    "HACK-A10": "wQ5fL1kR9hM4",
    "HACK-A11": "vB7pT3nJ6cX2",
    "HACK-A12": "nK4wM8gL2fP9",
    "HACK-A13": "cR1vN5hQ7xB3",
    "HACK-A14": "pL9mK2wT6jF4",
    "HACK-A15": "xJ3gP7nC1vR8",
    "HACK-A16": "hF6kL9wM4bT2",
    "HACK-A17": "mN2pV5gX8cQ1",
    "HACK-A18": "bT7wR3nK6fL9",
    "HACK-A19": "gL4pM1vJ8xC5",
    "HACK-A20": "kP9nT2wF6hR3",
    "HACK-A21": "fM5vL8gK1pB7",
    "HACK-A22": "wX3cN6hT9jQ2",
    "HACK-A23": "pR7kM4nL1vF8",
    "HACK-A24": "vJ2gP9wC5xT6",
    "HACK-A25": "nL6fK3hR8mB1",
    "HACK-A26": "tP4wM7gV2cN9",
    "HACK-A27": "hK1nL5vX8pR3",
    "HACK-A28": "mF9gT2wJ6cL4",
    "HACK-A29": "bN3pK7vM1xR8",
    "HACK-A30": "gP6wL9hF4nT2",
    "HACK-A31": "fM5vL8gK1pB5",
    "HACK-A32": "wX3cN6hT9jQ5",
    "HACK-A33": "pR7kM4nL1vF5",
    "HACK-A34": "vJ2gP9wC5xT5",
    "HACK-A35": "nL6fK3hR8mB5",
    "HACK-A36": "tP4wM7gV2cN5",
    "HACK-A37": "hK1nL5vX8pR5",
    "HACK-A38": "mF9gT2wJ6cL5",
    "HACK-A39": "bN3pK7vM1xR5",
    "HACK-A40": "gP6wL9hF4nT5",
    "HACK-A41": "xK9mP2nQ7vL3",
    "HACK-A42": "bR5wF8cJ3hN3",
    "HACK-A43": "tY2gV9xM1pD3",
    "HACK-A44": "qL7nK4wP9jR3",
    "HACK-A45": "fH3vB6mC8xT3",
    "HACK-A46": "zN1pW4kL7gQ3",
    "HACK-A47": "dM8cX2vF5nJ2",
    "HACK-A48": "rT6hK9wB4pL3",
    "HACK-A49": "jP3mN7gV2xC3",
    "HACK-A50": "wQ5fL1kR9hM3"
    
}

# ========================================
# ADMIN CREDENTIALS
# ========================================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Hackathon@2026"  # Change this to your secure password

# ========================================
# OLLAMA CONFIGURATION
# ========================================
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:1.5b"
  # Much faster, still good for debugging

# ========================================
# DEBUG-ONLY SYSTEM PROMPT
# ========================================
SYSTEM_PROMPT = """You are DebugBot. You help ONLY with debugging.

Rules:
- You may explain errors
- You may analyze bugs
- You may troubleshoot issues
- You may give small illustrative examples for understanding
- You may show example error patterns
- You may show example scenarios
- You may explain with mini-snippets (not full programs)

STRICTLY FORBIDDEN:
- Full code generation
- Feature creation
- System design
- Project building
- Architecture design
- Writing full functions
- Writing full applications

Style rules:
- Always explain in simple terms
- Always include at least one example
- Use real-world examples when possible
- Focus on understanding, not implementation

If the user asks for forbidden tasks, politely refuse."""


# ========================================
# CHAT HISTORY STORAGE
# ========================================
chat_history = {}

# ========================================
# AUTHENTICATION MIDDLEWARE
# ========================================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'team_id' not in session:
            return jsonify({"error": "Unauthorized - Please login"}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'is_admin' not in session or not session['is_admin']:
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated_function

# ========================================
# REQUEST FILTERING
# ========================================
def is_debug_request(user_message):
    """Check if request is debug-related"""
    forbidden_keywords = [
        "create", "build", "generate", "write a function", "make a",
        "develop", "design", "implement", "code for", "write code",
        "build a project", "create a system", "develop a feature"
    ]
    
    debug_keywords = [
        "error", "exception", "bug", "debug", "why is", "not working",
        "fails", "broken", "issue", "problem", "traceback", "stack trace"
    ]
    
    message_lower = user_message.lower()
    
    # Check for forbidden patterns
    for keyword in forbidden_keywords:
        if keyword in message_lower:
            return False
    
    # Check for debug patterns
    for keyword in debug_keywords:
        if keyword in message_lower:
            return True
    
    # If unclear, allow (can be refined later)
    return True

# ========================================
# ROUTES
# ========================================

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    team_id = data.get('team_id')
    password = data.get('password')
    
    if not team_id or not password:
        return jsonify({"error": "Team ID and password required"}), 400
    
    if team_id in TEAMS and TEAMS[team_id] == password:
        session['team_id'] = team_id
        session['is_admin'] = False
        return jsonify({
            "success": True,
            "team_id": team_id,
            "is_admin": False,
            "message": "Login successful"
        })
    
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['team_id'] = 'ADMIN'
        session['is_admin'] = True
        return jsonify({
            "success": True,
            "is_admin": True,
            "message": "Admin login successful"
        })
    
    return jsonify({"error": "Invalid admin credentials"}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('team_id', None)
    return jsonify({"success": True})

@app.route('/api/check-session', methods=['GET'])
def check_session():
    if 'team_id' in session:
        return jsonify({
            "authenticated": True, 
            "team_id": session['team_id'],
            "is_admin": session.get('is_admin', False)
        })
    return jsonify({"authenticated": False})

@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    data = request.json
    user_message = data.get('message', '').strip()
    team_id = session['team_id']
    
    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400
    
    # Filter non-debug requests
    if not is_debug_request(user_message):
        return jsonify({
            "response": "❌ **DebugBot - Request Blocked**\n\nI can only help with debugging existing code. I cannot:\n- Generate new code\n- Build features\n- Create projects\n- Design systems\n\nPlease ask me about errors, exceptions, or debugging existing code!",
            "blocked": True
        })
    
    # Store in chat history
    if team_id not in chat_history:
        chat_history[team_id] = []
    
    chat_history[team_id].append({
        "role": "user",
        "content": user_message,
        "timestamp": datetime.now().isoformat()
    })
    
    # Call Ollama with streaming disabled for faster initial response
    try:
        ollama_response = requests.post(OLLAMA_URL, json={
            "model": MODEL_NAME,
            "prompt": f"{SYSTEM_PROMPT}\n\nUser: {user_message}\nDebugBot:",
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 500  # Limit response length for speed
            }
        }, timeout=30)
        
        if ollama_response.status_code == 200:
            response_text = ollama_response.json().get('response', 'No response')
            
            chat_history[team_id].append({
                "role": "assistant",
                "content": response_text,
                "timestamp": datetime.now().isoformat()
            })
            
            return jsonify({
                "response": response_text,
                "blocked": False
            })
        else:
            return jsonify({"error": "Ollama model not responding"}), 500
            
    except requests.exceptions.Timeout:
        return jsonify({"error": "Response timed out. Model may be too slow."}), 500
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Cannot connect to Ollama. Is it running?"}), 500

@app.route('/api/history', methods=['GET'])
@login_required
def get_history():
    team_id = session['team_id']
    return jsonify({"history": chat_history.get(team_id, [])})

# ========================================
# ADMIN ROUTES
# ========================================

@app.route('/api/admin/teams', methods=['GET'])
@admin_required
def admin_teams():
    """Get all teams (for admin panel)"""
    teams_list = [{"team_id": tid, "password": pwd} for tid, pwd in TEAMS.items()]
    return jsonify({"teams": teams_list})

@app.route('/api/admin/chat-logs', methods=['GET'])
@admin_required
def admin_logs():
    """Get all chat logs"""
    return jsonify({"logs": chat_history})

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/admin')
def admin():
    return app.send_static_file('admin.html')

if __name__ == '__main__':
    print("🤖 DebugBot Backend Starting...")
    print(f"📋 {len(TEAMS)} teams loaded")
    print("🔗 Ollama endpoint:", OLLAMA_URL)
    print("🧠 Model:", MODEL_NAME)
    print("\n✅ Access DebugBot at: http://localhost:5000")
    print("✅ Access Admin Panel at: http://localhost:5000/admin")
    app.run(debug=True, host='0.0.0.0', port=5000)