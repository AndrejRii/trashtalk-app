# app.py - UPDATED WITHOUT API KEY
from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='public')

# Get API key from environment variable only - no hardcoded key
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')

# Serve static files from the public directory
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# Proxy endpoint for Claude API
@app.route('/api/claude', methods=['POST'])
def claude_proxy():
    if not ANTHROPIC_API_KEY:
        return jsonify({"error": {"message": "API key not configured on server"}}), 500
        
    try:
        # Get the data from the frontend
        data = request.json
        
        # Log the request for debugging (without sensitive info)
        print(f"Received request for model: {data.get('model', 'unknown')}")
        
        print(f"System message: {data.get('system', 'None')}")
        print(f"First few messages: {data.get('messages', [])[:2]}")

        # Forward to Anthropic API
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            json=data,
            headers={
                'Content-Type': 'application/json',
                'x-api-key': ANTHROPIC_API_KEY,
                'anthropic-version': '2023-06-01'
            }
        )
        
        # Log the response status for debugging
        print(f"Anthropic API response status: {response.status_code}")
        
        # Return the response from Anthropic
        return jsonify(response.json())
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": {"message": str(e)}}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)