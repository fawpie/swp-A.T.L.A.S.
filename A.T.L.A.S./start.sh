#!/bin/bash

# --- AYARLAR ---
export GEMINI_API_KEY="API_ANAHTARINIZI_BURAYA_YAPIŞTIRIN"
# ---------------

# Log klasörünün var olduğundan emin ol
mkdir -p logs

# Her çalıştırmada yeni bir log dosyası oluştur
LOG_FILE="logs/atlas_$(date +%Y-%m-%d_%H-%M-%S).log"

# Projenin sanal ortamını aktif et
source venv/bin/activate

# Uygulamayı yeniden başlatma döngüsü içinde çalıştır
while true; do
    echo "API anahtarı ayarlandı. Sanal ortam aktif. A.T.L.A.S. başlatılıyor..."
    echo "Tüm çıktılar şu dosyaya kaydediliyor: $LOG_FILE"
    
    # Python uygulamasını çalıştır ve tüm çıktıları (stdout ve stderr) hem terminale hem de log dosyasına yönlendir
    python -m src.main 2>&1 | tee -a "$LOG_FILE"
    
    # Python'dan gelen çıkış kodunu al (pipe kullandığımız için özel bir yöntemle)
    exit_code=${PIPESTATUS[0]}
    
    if [ $exit_code -ne 10 ]; then
        break
    fi
    
    echo "Ayarlar kaydedildi, uygulama yeniden başlatılıyor..." | tee -a "$LOG_FILE"
    sleep 1
done

echo "A.T.L.A.S. kapatıldı." | tee -a "$LOG_FILE"