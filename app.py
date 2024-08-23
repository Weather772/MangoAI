from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__)

# Your Hugging Face API key and model endpoint
HF_API_KEY = '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'
MODEL_ENDPOINT = 'https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill'

headers = {
    'Authorization': f'Bearer {HF_API_KEY}'
}

@app.route('/')
def index():
    # Serve the HTML file
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # Handle POST requests to /chat
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    response = requests.post(MODEL_ENDPOINT, headers=headers, json={"inputs": user_input})
    if response.status_code == 200:
        result = response.json()
        reply = result[0]['generated_text']
        return jsonify({'reply': reply})
    else:
        return jsonify({'error': 'Failed to get a response from the model'}), response.status_code

if __name__ == '__main__':
    # Run the Flask app on all network interfaces, port 5000
    app.run(host='0.0.0.0', port=5000)
