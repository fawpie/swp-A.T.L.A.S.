import sys
import pyperclip
from datetime import date, timedelta
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QMessageBox, QTextEdit, QDialog, QCalendarWidget
)
from PyQt5.QtCore import QThread, pyqtSignal, QDate
from src import automator
from src.tracker_window import TrackerWindow
from src.translations import get_string, STRINGS

class CalendarDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tarih Seç")
        layout = QVBoxLayout(self)
        self.calendar = QCalendarWidget(self)
        self.calendar.setMinimumDate(QDate.currentDate())
        layout.addWidget(self.calendar)
        self.btn_ok = QPushButton("Tamam", self)
        self.btn_ok.clicked.connect(self.accept)
        layout.addWidget(self.btn_ok)
        self.selected_date = self.calendar.selectedDate()
        self.calendar.selectionChanged.connect(self.date_selected)

    def date_selected(self):
        self.selected_date = self.calendar.selectedDate()

class AutomatorThread(QThread):
    finished = pyqtSignal(bool)
    progress = pyqtSignal(str)
    def run(self):
        try:
            self.progress.emit("API'ye bağlanılıyor...")
            success = automator.get_gemini_response()
            self.finished.emit(success)
        except Exception as e:
            self.progress.emit(f"Bir hata oluştu: {e}")
            self.finished.emit(False)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(get_string("creator_window_title"))
        self.setGeometry(100, 100, 450, 500)
        self.setup_ui()
        self.automator_thread = None
        self.start_date = date.today()

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(QLabel(get_string("goal_label")))
        self.input_goal = QLineEdit(self)
        self.input_goal.setPlaceholderText("Örn: YKS TYT sınavına hazırlanmak")
        self.layout.addWidget(self.input_goal)
        self.layout.addWidget(QLabel(get_string("duration_label")))
        self.input_duration = QLineEdit(self)
        self.input_duration.setPlaceholderText("Örn: 3 Ay")
        self.layout.addWidget(self.input_duration)
        self.layout.addWidget(QLabel(get_string("type_label")))
        self.combo_type = QComboBox(self)
        self.combo_type.addItems(["Günlük", "Haftalık", "Aylık"])
        self.layout.addWidget(self.combo_type)
        self.layout.addWidget(QLabel("Programa Ne Zaman Başlanacak?"))
        self.combo_start_date = QComboBox(self)
        self.start_date_options = {
            "Bugün": date.today(),
            "Yarın": date.today() + timedelta(days=1),
            "Gelecek Hafta": date.today() + timedelta(weeks=1),
            "Takvimden Seç...": None
        }
        self.combo_start_date.addItems(self.start_date_options.keys())
        self.combo_start_date.currentTextChanged.connect(self.handle_date_selection)
        self.layout.addWidget(self.combo_start_date)
        self.layout.addWidget(QLabel(get_string("language_label")))
        self.combo_lang = QComboBox(self)
        self.combo_lang.addItems([lang.upper() for lang in STRINGS.keys()])
        self.layout.addWidget(self.combo_lang)
        self.button_automate = QPushButton(get_string("create_button"))
        self.layout.addWidget(self.button_automate)
        self.layout.addWidget(QLabel(get_string("log_label")))
        self.log_box = QTextEdit(self)
        self.log_box.setReadOnly(True)
        self.log_box.setPlaceholderText("İşlem adımları burada görünecek...")
        self.layout.addWidget(self.log_box)
        self.button_automate.clicked.connect(self.start_automation)

    def handle_date_selection(self, text):
        if text == "Takvimden Seç...":
            dialog = CalendarDialog(self)
            if dialog.exec_() == QDialog.Accepted and dialog.selected_date:
                self.start_date = dialog.selected_date.toPyDate()
                display_text = f"Seçilen: {self.start_date.strftime('%d-%m-%Y')}"
                if self.combo_start_date.findText(display_text) == -1:
                    self.combo_start_date.addItem(display_text)
                self.combo_start_date.setCurrentText(display_text)
            else:
                self.combo_start_date.setCurrentIndex(0)
        elif "Seçilen:" not in text:
            self.start_date = self.start_date_options[text]

    def generate_prompt_and_copy(self):
        goal = self.input_goal.text(); duration = self.input_duration.text()
        program_type = self.combo_type.currentText(); lang = self.combo_lang.currentText().lower()
        if not goal or not duration:
            self.show_message("Giriş Hatası", "Lütfen 'Amaç' ve 'Süre' alanlarını doldurun.")
            return False
        if program_type == "Günlük": format_example = "--- GÜN 1 ---\n[ ] ANA GÖREV\n    [ ] ALT GÖREV\n--- GÜN 2 ---"
        elif program_type == "Aylık": format_example = "--- AY 1 ---\n[ ] ANA GÖREV\n    [ ] ALT GÖREV\n--- AY 2 ---"
        else: format_example = "--- HAFTA 1 ---\n[ ] ANA GÖREV\n    [ ] ALT GÖREV\n--- HAFTA 2 ---"
        system_prompt = f"""SENİN GÖREVİN: Sana verilen kullanıcı isteğine göre, son derece detaylı ve eksiksiz bir program çıktısı oluşturacaksın.

KURALLAR:
1. Çıktın SADECE ve SADECE HAM METİN olmalıdır. Asla Python kodu, markdown (```) veya sohbet cümleleri ekleme.
2. Programı, kullanıcının istediği "{program_type}" zaman dilimlerine göre böl.
3. KESİNLİKLE TEMBELLİK YAPMA. "Bu döngüyü tekrarla", "önceki haftalara benzer şekilde" gibi ifadeler kullanmak YASAKTIR. İstenen sürenin tamamı için EKSİKSİZ ve DETAYLI bir plan oluşturmalısın.
4. Çıktı formatı KESİNLİKLE şöyle olmalıdır:
HEDEF: [Kullanıcının belirttiği hedef]
SÜRE: [Kullanıcının belirttiği süre]
{format_example}
5. Tüm program bittiğinde, çıktının EN SONUNA KESİNLİKLE şu özel bitiş sinyalini ekle: //--END_OF_ATLAS_PROGRAM--//
"""
        user_request = f"""KULLANICI İSTEĞİ:
- Hedef: {goal}
- Süre: {duration}
- Program Tipi: {program_type}
- Başlangıç Tarihi: {self.start_date.strftime('%d-%m-%Y')}
- Program Dili: {lang}"""
        final_prompt = f"{system_prompt.strip()}\n\n---\n\n{user_request.strip()}"
        pyperclip.copy(final_prompt)
        self.log_box.append("✅ API komutu oluşturuldu ve panoya kopyalandı.")
        return True

    def start_automation(self):
        self.log_box.clear()
        if not self.generate_prompt_and_copy(): return
        self.button_automate.setEnabled(False)
        self.button_automate.setText("Program Oluşturuluyor...")
        self.automator_thread = AutomatorThread()
        self.automator_thread.progress.connect(self.update_log)
        self.automator_thread.finished.connect(self.on_automation_finished)
        self.automator_thread.start()

    def update_log(self, message):
        self.log_box.append(message)

    def on_automation_finished(self, success):
        self.button_automate.setEnabled(True)
        self.button_automate.setText(get_string("create_button"))
        if success:
            self.log_box.append("🎉 Program başarıyla oluşturuldu! Takip arayüzü açılıyor...")
            self.close()
            self.tracker = TrackerWindow()
            self.tracker.show()
        else:
            self.log_box.append("❌ API hatası. Detaylar için terminali kontrol edin.")
            self.show_message("Hata", "Program oluşturulamadı. Lütfen terminaldeki hata mesajlarına bakın.")

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information if title == "Başarılı" else QMessageBox.Warning)
        msg_box.exec_()