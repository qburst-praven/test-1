#!/usr/bin/env python3

import os
from datetime import datetime
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/details', methods=['GET'])
def get_details():
    # Get user from environment variable, default to "World" if not set
    user = os.getenv('USER', 'World')
    
    # Get current date and time
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    current_day = now.strftime("%A")
    current_date = now.strftime("%Y-%m-%d")
    current_time_only = now.strftime("%H:%M:%S")
    
    # Return details in JSON format
    return jsonify({
        "message": f"Hello {user}",
        "timestamp": current_time,
        "date": current_date,
        "time": current_time_only,
        "day": current_day,
        "app": "Test-1 Application",
        "status": "running"
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "app": "Test-1 Application"
    })

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Test-1 Application",
        "endpoints": [
            "/api/details - Get application details",
            "/health - Health check"
        ]
    })

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False) 