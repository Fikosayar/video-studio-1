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

# Global Model Değişkeni
model = None
if GEMINI_API_KEY:
    try:
        # Gemini 1.5 Flash modeli hızlı ve ekonomiktir
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        logger.error(f"Model başlatılamadı: {e}")

@app.route('/')
def health_check():
    """Coolify Health Check noktası."""
    return jsonify({"status": "active", "service": "Gemini AI Wrapper"}), 200

# --- DÜZELTİLEN KISIM BURASI ---
@app.route('/chat', methods=)
def chat_endpoint():
    """Sohbet uç noktası."""
    if not model:
        return jsonify({"error": "Sunucu hatası: Model başlatılamadı (API Key eksik olabilir)."}), 500

    data = request.get_json(silent=True)
    if not data or 'message' not in data:
        return jsonify({"error": "Geçersiz istek. JSON formatında 'message' alanı zorunludur."}), 400

    user_message = data['message']

    try:
        # Yapay zekadan yanıt al
        response = model.generate_content(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        logger.error(f"API Hatası: {e}")
        return jsonify({"error": f"Yapay zeka servisi hatası: {str(e)}"}), 500

if __name__ == '__main__':
    # Yerel geliştirme için
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
