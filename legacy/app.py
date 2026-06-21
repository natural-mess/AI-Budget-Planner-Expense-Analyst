import os
from flask import Flask, request, jsonify, render_template
from main_agent import MainAgent
import logging

app = Flask(__name__, static_folder='static', template_folder='templates')
logging.basicConfig(level=logging.INFO)

# In-memory store for demo
sessions = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("prompt")
    api_key = data.get("api_key")
    session_id = data.get("session_id", "default")
    
    if session_id not in sessions:
        sessions[session_id] = MainAgent()
        
    agent = sessions[session_id]
    
    result = agent.handle_message(user_input, api_key)
    return jsonify(result)

@app.route('/approve', methods=['POST'])
def approve():
    data = request.json
    budget = data.get("budget")
    session_id = data.get("session_id", "default")
    
    agent = sessions.get(session_id)
    if not agent:
        return jsonify({"error": "Session not found"}), 400
        
    result = agent.approve_budget(budget)
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
