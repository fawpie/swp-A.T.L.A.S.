import sys
import os
from PyQt5.QtWidgets import QApplication

from src.settings import SETTINGS
from src.first_launch_window import FirstLaunchWindow
from src.gui import MainWindow
from src.tracker_window import TrackerWindow

class AppController:
    """Uygulamanın hangi pencereyi ne zaman açacağını yöneten ana sınıf."""
    def __init__(self, app):
        self.app = app
        self.window = None

    def start(self):
        # Ayarlardan temayı yükle ve uygula
        theme = SETTINGS.get("theme", "dark")
        stylesheet = self.load_stylesheet(theme)
        self.app.setStyleSheet(stylesheet)

        # İlk açılış mı kontrol et
        if not SETTINGS.get("first_launch_completed", False):
            self.show_first_launch()
        else:
            self.show_main_app()

    def show_first_launch(self):
        """İlk açılış ve dil seçimi penceresini gösterir."""
        self.window = FirstLaunchWindow()
        # Kurulum penceresi bittiğinde "show_main_app" fonksiyonunu çalıştır
        self.window.setup_finished.connect(self.show_main_app)
        self.window.show()

    def show_main_app(self):
        """Ana uygulama akışını başlatır (takip veya oluşturma ekranı)."""
        if self.window: # Önceki pencereyi kapat (ilk kurulumdan geliyorsa)
            self.window.close()
            
        if os.path.exists("program.txt"):
            self.window = TrackerWindow()
        else:
            self.window = MainWindow()
        self.window.show()

    def load_stylesheet(self, theme_name):
        path = f"src/styles/{theme_name}_theme.qss"
        try:
            with open(path, "r") as f:
                return f.read()
        except FileNotFoundError:
            print(f"Uyarı: Stil dosyası bulunamadı: {path}")
            return ""

def run():
    app = QApplication(sys.argv)
    controller = AppController(app)
    controller.start()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()