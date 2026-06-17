from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "healthy",
        "message": "Secure GitOps Platform running",
        "version": os.getenv("APP_VERSION", "1.0.0")
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/metrics-check')
def metrics():
    return jsonify({
        "status": "ok",
        "uptime": "running"
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)