import os
import logging
from flask import Flask, request, jsonify
import google.generativeai as genai

# Loglama ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# API Anahtarı Kontrolü
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY ortam değişkeni bulunamadı!")
else:
    genai.configure(api_key=GEMINI_API_KEY)
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        logger.error(f"Model başlatılamadı: {e}")

@app.route('/')
def health_check():
    """Sağlık kontrolü."""
    return jsonify({"status": "active", "service": "Gemini AI Wrapper"}), 200

# HATA BURADAYDI, DÜZELTİLDİ: methods= eklendi
@app.route('/chat', methods=)
def chat_endpoint():
    """Sohbet uç noktası."""
    if not GEMINI_API_KEY:
        return jsonify({"error": "API Key eksik"}), 500

    data = request.get_json(silent=True)
    if not data or 'message' not in data:
        return jsonify({"error": "Geçersiz istek. 'message' alanı gerekli."}), 400

    try:
        response = model.generate_content(data['message'])
        return jsonify({"reply": response.text})
    except Exception as e:
        logger.error(f"API Hatası: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
