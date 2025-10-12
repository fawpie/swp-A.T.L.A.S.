import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QLabel, QComboBox, QPushButton, QMessageBox, 
    QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import QCoreApplication
from .settings import save_settings, SETTINGS
from .translations import STRINGS, get_string

class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(get_string("settings_window_title"))
        self.setGeometry(300, 300, 400, 250)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        self.layout.addWidget(QLabel(get_string("choose_language")))
        self.combo_lang = QComboBox()
        self.combo_lang.addItems([lang.upper() for lang in STRINGS.keys()])
        self.combo_lang.setCurrentText(SETTINGS.get("language", "en").upper())
        self.layout.addWidget(self.combo_lang)

        self.layout.addWidget(QLabel(get_string("theme_label")))
        self.combo_theme = QComboBox()
        self.combo_theme.addItems(["dark", "light", "nord", "dracula"])
        self.combo_theme.setCurrentText(SETTINGS.get("theme", "dark"))
        self.layout.addWidget(self.combo_theme)

        self.button_save = QPushButton(get_string("save_button"))
        self.button_save.clicked.connect(self.save_and_restart)
        self.layout.addWidget(self.button_save)

        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.button_reset = QPushButton(get_string("app_reset"))
        self.button_reset.setStyleSheet("background-color: #c0392b;")
        self.button_reset.clicked.connect(self.reset_application)
        self.layout.addWidget(self.button_reset)

    def save_and_restart(self):
        SETTINGS["language"] = self.combo_lang.currentText().lower()
        SETTINGS["theme"] = self.combo_theme.currentText()
        save_settings(SETTINGS)
        
        QMessageBox.information(self, "Bilgi", get_string("restart_notice"))
        self.restart_app()

    def reset_application(self):
        reply = QMessageBox.question(self, get_string("reset_confirm_title"), 
                                     get_string("reset_confirm_text"), 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            print("Uygulama sıfırlanıyor...")
            try:
                if os.path.exists("config.json"): os.remove("config.json")
                if os.path.exists("program.txt"): os.remove("program.txt")
                QMessageBox.information(self, "Bilgi", "Uygulama sıfırlandı ve yeniden başlatılacak.")
                self.restart_app()
            except Exception as e:
                QMessageBox.warning(self, "Hata", f"Sıfırlama sırasında hata oluştu: {e}")
    
    def restart_app(self):
        """Uygulamayı, start.sh'e yeniden başlatma sinyali göndererek kapatır."""
        # 10, bizim start.sh'e gönderdiğimiz özel "yeniden başlat" sinyalidir.
        QCoreApplication.instance().exit(10)