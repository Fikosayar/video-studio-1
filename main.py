import os
import logging
from flask import Flask, request, jsonify, render_template # render_template eklendi
import google.generativeai as genai

# Loglama
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# API Key ve Model
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

# --- GÜNCELLENEN KISIM ---
# Artık sadece JSON değil, HTML arayüzünü döndürüyoruz.
@app.route('/')
def home():
    return render_template('index.html')

# API Uç Noktası (Arayüz buraya istek atacak)
@app.route('/chat', methods=['GET', 'POST'])
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
    # Localhost ayarını Coolify panelinden (127.0.0.1:3000:3000) yaptığınız için
    # burası 0.0.0.0 olarak kalmalıdır.
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
