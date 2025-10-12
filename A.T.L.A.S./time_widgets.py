import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QToolButton, QSpinBox
from PyQt5.QtCore import QTimer, QTime, Qt, QUrl
from PyQt5.QtMultimedia import QSoundEffect

class ClockPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(self.time_label)
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        self.update_time()

    def update_time(self):
        self.time_label.setText(QTime.currentTime().toString('hh:mm:ss'))

class StopwatchPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.time_label = QLabel("00:00:00.000")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        button_layout = QHBoxLayout()
        self.btn_start = QPushButton("Başlat")
        self.btn_stop = QPushButton("Durdur")
        self.btn_reset = QPushButton("Sıfırla")
        button_layout.addWidget(self.btn_start)
        button_layout.addWidget(self.btn_stop)
        button_layout.addWidget(self.btn_reset)
        layout.addWidget(self.time_label)
        layout.addLayout(button_layout)
        self.timer = QTimer(self)
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_stopwatch)
        self.elapsed_time = QTime(0, 0, 0)
        self.btn_start.clicked.connect(self.timer.start)
        self.btn_stop.clicked.connect(self.timer.stop)
        self.btn_reset.clicked.connect(self.reset_stopwatch)

    def update_stopwatch(self):
        self.elapsed_time = self.elapsed_time.addMSecs(10)
        self.time_label.setText(self.elapsed_time.toString("hh:mm:ss.zzz"))
    
    def reset_stopwatch(self):
        self.timer.stop()
        self.elapsed_time.setHMS(0,0,0,0)
        self.time_label.setText("00:00:00.000")

class TimerPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.time_label = QLabel("00:05:00")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        input_layout = QHBoxLayout()
        self.spin_minutes = QSpinBox()
        self.spin_minutes.setRange(0, 999)
        self.spin_minutes.setValue(5)
        self.spin_seconds = QSpinBox()
        self.spin_seconds.setRange(0, 59)
        input_layout.addWidget(QLabel("Dakika:"))
        input_layout.addWidget(self.spin_minutes)
        input_layout.addWidget(QLabel("Saniye:"))
        input_layout.addWidget(self.spin_seconds)
        button_layout = QHBoxLayout()
        self.btn_start = QPushButton("Başlat")
        self.btn_stop = QPushButton("Durdur")
        self.btn_reset = QPushButton("Sıfırla")
        button_layout.addWidget(self.btn_start)
        button_layout.addWidget(self.btn_stop)
        button_layout.addWidget(self.btn_reset)
        layout.addWidget(self.time_label)
        layout.addLayout(input_layout)
        layout.addLayout(button_layout)
        
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer)
        self.remaining_seconds = 300
        
        self.finish_sound = QSoundEffect(self)
        sound_file_path = os.path.abspath("sounds/bell.wav")
        self.finish_sound.setSource(QUrl.fromLocalFile(sound_file_path))
        
        self.btn_start.clicked.connect(self.start_timer)
        self.btn_stop.clicked.connect(self.timer.stop)
        self.btn_reset.clicked.connect(self.reset_timer)

    def format_time_from_seconds(self, total_seconds):
        sign = "-" if total_seconds < 0 else ""
        total_seconds = abs(total_seconds)
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            return f"{sign}{hours:02d}:{minutes:02d}:{seconds:02d}"
        return f"{sign}{minutes:02d}:{seconds:02d}"

    def start_timer(self):
        if not self.timer.isActive():
            self.remaining_seconds = (self.spin_minutes.value() * 60) + self.spin_seconds.value()
            self.time_label.setText(self.format_time_from_seconds(self.remaining_seconds))
            self.timer.start()

    def update_timer(self):
        self.remaining_seconds -= 1
        self.time_label.setText(self.format_time_from_seconds(self.remaining_seconds))
        if self.remaining_seconds == 0:
            self.finish_sound.play()

    def reset_timer(self):
        self.timer.stop()
        self.remaining_seconds = (self.spin_minutes.value() * 60) + self.spin_seconds.value()
        self.time_label.setText(self.format_time_from_seconds(self.remaining_seconds))

class TimeWidgets(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout = QHBoxLayout()
        self.left_arrow = QToolButton()
        self.left_arrow.setArrowType(Qt.LeftArrow)
        self.mode_label = QLabel("Saat")
        self.mode_label.setAlignment(Qt.AlignCenter)
        self.right_arrow = QToolButton()
        self.right_arrow.setArrowType(Qt.RightArrow)
        nav_layout.addWidget(self.left_arrow)
        nav_layout.addWidget(self.mode_label)
        nav_layout.addWidget(self.right_arrow)
        self.pages = QStackedWidget()
        self.page_names = ["Saat", "Kronometre", "Zamanlayıcı"]
        self.pages.addWidget(ClockPage())
        self.pages.addWidget(StopwatchPage())
        self.pages.addWidget(TimerPage())
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.pages)
        self.left_arrow.clicked.connect(self.prev_page)
        self.right_arrow.clicked.connect(self.next_page)
        self.pages.currentChanged.connect(self.update_mode_label)
        
        self.pages.wheelEvent = self.wheel_event_handler

    def prev_page(self):
        index = self.pages.currentIndex()
        new_index = (index - 1) % self.pages.count()
        self.pages.setCurrentIndex(new_index)

    def next_page(self):
        index = self.pages.currentIndex()
        new_index = (index + 1) % self.pages.count()
        self.pages.setCurrentIndex(new_index)

    def update_mode_label(self, index):
        self.mode_label.setText(self.page_names[index])
        
    def wheel_event_handler(self, event):
        delta = event.angleDelta().y()
        if delta > 0: self.prev_page()
        elif delta < 0: self.next_page()
        event.accept()