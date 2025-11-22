import os
from flask import Flask, request, jsonify
import google.generativeai as genai

# Flask uygulamasını başlatıyoruz
app = Flask(__name__)

# KONFIGURASYON YÖNETİMİ
# API anahtarını doğrudan koda yazmak büyük bir güvenlik riskidir.
# Bu anahtarı Coolify panelinden 'Environment Variables' olarak gireceğiz.
GOOGLE_API_KEY = os.environ.get('GEMINI_API_KEY')

# API anahtarı kontrolü ve konfigürasyonu
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    # Anahtar yoksa uygulama çökmemeli ama uyarı vermeli
    print("UYARI: GEMINI_API_KEY çevresel değişkeni bulunamadı!")

@app.route('/')
def health_check():
    """
    Coolify Health Check Mekanizması için Endpoint.
    Coolify, uygulamanın ayakta olup olmadığını anlamak için periyodik olarak
    bu adrese istek atar. 200 OK dönmesi şarttır.
    """
    return jsonify({"status": "running", "service": "AI Wrapper"}), 200

@app.route('/chat', methods=)
def chat():
    """
    Ana işlem fonksiyonu. Kullanıcıdan gelen mesajı alır,
    Google Gemini'ye iletir ve cevabı döndürür.
    """
    if not GOOGLE_API_KEY:
        return jsonify({"error": "Sunucu konfigürasyon hatası: API Key eksik"}), 500
    
    # JSON verisini al
    data = request.get_json(silent=True)
    if not data or 'message' not in data:
        return jsonify({"error": "Geçersiz istek. 'message' parametresi gerekli."}), 400

    user_message = data['message']

    try:
        # Google Gemini modelini çağırıyoruz (Gemini 1.5 Flash hızlı ve etkilidir)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # İçerik üretimi
        response = model.generate_content(user_message)
        
        # Cevabı metin olarak döndür
        return jsonify({"response": response.text})
    
    except Exception as e:
        # Hata durumunda detaylı bilgi (Loglara düşmesi için print edilebilir)
        print(f"Gemini API Hatası: {e}")
        return jsonify({"error": "Yapay zeka servisiyle iletişimde hata oluştu."}), 500

if __name__ == "__main__":
    # Bu blok SADECE yerel bilgisayarınızda `python main.py` dediğinizde çalışır.
    # Coolify üzerinde Gunicorn kullanacağımız için bu blok atlanır.
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)
