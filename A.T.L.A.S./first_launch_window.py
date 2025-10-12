import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import pyqtSignal
from .settings import save_settings, SETTINGS
from .translations import STRINGS, get_string

class FirstLaunchWindow(QMainWindow):
    setup_finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle(get_string("welcome_title"))
        self.setGeometry(300, 300, 400, 150)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        self.label = QLabel(get_string("choose_language"))
        self.layout.addWidget(self.label)
        
        self.combo_lang = QComboBox()
        self.combo_lang.addItems([lang.upper() for lang in STRINGS.keys()])
        self.combo_lang.setCurrentText(SETTINGS.get("language", "en").upper())
        self.layout.addWidget(self.combo_lang)
        
        self.button = QPushButton(get_string("continue_button"))
        self.button.clicked.connect(self.save_and_continue)
        self.layout.addWidget(self.button)

    def save_and_continue(self):
        selected_lang = self.combo_lang.currentText().lower()
        SETTINGS["language"] = selected_lang
        SETTINGS["first_launch_completed"] = True
        save_settings(SETTINGS)
        
        self.setup_finished.emit()