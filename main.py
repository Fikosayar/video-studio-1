import os
import logging
from flask import Flask, request, jsonify
import google.generativeai as genai

# Loglama
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# API Key ve Model Kurulumu
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
model = None

if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY eksik!")
else:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        logger.error(f"Model hatasi: {e}")

@app.route('/')
def health_check():
    return jsonify({"status": "active"}), 200

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    if not model:
        return jsonify({"error": "Model yuklenemedi"}), 500

    data = request.get_json(silent=True)
    if not data or 'message' not in data:
        return jsonify({"error": "Mesaj yok"}), 400

    try:
        response = model.generate_content(data['message'])
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
