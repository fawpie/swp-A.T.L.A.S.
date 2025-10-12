import os
import pyperclip
import google.generativeai as genai
from dotenv import load_dotenv

# --- ANA DEĞİŞİKLİK VE ÇÖZÜM BURADA ---
# .env dosyasının tam yolunu bularak yüklemesini sağlıyoruz.
# Bu dosyanın bir üst dizinde olduğunu belirtiyoruz.
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)
# ------------------------------------

try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY, .env dosyasında bulunamadı veya yüklenemedi.")
    genai.configure(api_key=api_key)
    API_CONFIGURED_SUCCESSFULLY = True
except Exception as e:
    print(f"API yapılandırma hatası: {e}")
    API_CONFIGURED_SUCCESSFULLY = False

def get_gemini_response():
    if not API_CONFIGURED_SUCCESSFULLY:
        raise ConnectionError("API anahtarı yapılandırılamadığı için istek gönderilemiyor.")

    prompt_text = pyperclip.paste()
    if not prompt_text:
        print("Hata: Panoda kopyalanmış bir komut bulunamadı.")
        return False

    print("Gemini API'sine bağlanılıyor...")
    try:
        # Daha önce çalıştığını doğruladığımız modeli kullanalım
        model = genai.GenerativeModel('models/gemini-pro-latest')
        
        response = model.generate_content(prompt_text)
        ai_response_text = response.text
        print("API'den yanıt başarıyla alındı.")

        with open('program.txt', 'w', encoding='utf-8') as f:
            f.write(ai_response_text.strip())
            
        print("program.txt başarıyla oluşturuldu!")
        return True
    except Exception as e:
        print(f"API ile iletişim sırasında bir hata oluştu: {e}")
        return False

def get_interesting_fact(lang="tr"):
    # Bu özellik geçici olarak devre dışı
    return "..."