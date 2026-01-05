from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import json
import os
import secrets
from datetime import datetime

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Caminho para o banco de dados simples (JSON)
DB_PATH = 'data/consoles.json'

def load_db():
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, 'w') as f:
            json.dump({"consoles": {}, "settings": {"version": "1.0.0", "status": "online"}}, f)
    with open(DB_PATH, 'r') as f:
        return json.load(f)

def save_db(data):
    with open(DB_PATH, 'w') as f:
        json.dump(data, f, indent=4)

# --- API PARA O CONSOLE (XBOX 360) ---

@app.route('/api/v1/auth', methods=['POST'])
def authenticate():
    data = request.json
    cpukey = data.get('cpukey')
    
    if not cpukey:
        return jsonify({"status": "error", "message": "CPUKey missing"}), 400
    
    db = load_db()
    if cpukey in db['consoles']:
        console = db['consoles'][cpukey]
        console['last_seen'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_db(db)
        
        return jsonify({
            "status": "success",
            "authorized": True,
            "message": "Welcome to Dark Stealth",
            "server_version": db['settings']['version']
        })
    else:
        # Auto-registro para teste (pode ser desativado depois)
        db['consoles'][cpukey] = {
            "name": f"Console_{cpukey[:4]}",
            "added_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "active"
        }
        save_db(db)
        return jsonify({"status": "success", "authorized": True, "message": "Console registered"})

@app.route('/api/v1/challenges', methods=['GET'])
def get_challenges():
    # Aqui você enviaria os bytes dos desafios (hashes, etc)
    # Simulação de resposta de desafio
    return jsonify({
        "challenge_id": secrets.token_hex(8),
        "data": "SIMULATED_CHALLENGE_DATA_FOR_XBOX_LIVE",
        "timestamp": datetime.now().timestamp()
    })

# --- PAINEL DE CONTROLE (WEB) ---

@app.route('/')
def index():
    db = load_db()
    return render_template('dashboard.html', consoles=db['consoles'], settings=db['settings'])

@app.route('/admin/settings', methods=['POST'])
def update_settings():
    db = load_db()
    db['settings']['status'] = request.form.get('status')
    db['settings']['version'] = request.form.get('version')
    save_db(db)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
