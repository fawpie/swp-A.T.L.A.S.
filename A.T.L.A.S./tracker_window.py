import sys
from datetime import date, timedelta
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTreeWidget, QTreeWidgetItem, QCheckBox, QProgressBar, QPushButton, QCalendarWidget, QStackedWidget, QSpacerItem, QSizePolicy, QToolButton, QTreeWidgetItemIterator
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QDate, QPoint, QEvent
from src import parser, automator
from src.translations import get_string, SETTINGS
from src.settings_window import SettingsWindow
from src.time_widgets import TimeWidgets

class FactLoaderThread(QThread):
    fact_loaded = pyqtSignal(str)
    def run(self):
        lang = SETTINGS.get("language", "en")
        fact = automator.get_interesting_fact(lang)
        self.fact_loaded.emit(fact)

class SwipeStackedWidget(QStackedWidget):
    swiped = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_pos = QPoint(); self.swipe_threshold = 50
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton: self.start_pos = event.pos()
        super().mousePressEvent(event)
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            diff = event.pos().x() - self.start_pos.x()
            if diff > self.swipe_threshold: self.swiped.emit(-1)
            elif diff < -self.swipe_threshold: self.swiped.emit(1)
        super().mouseReleaseEvent(event)

class TrackerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(get_string("tracker_window_title"))
        self.setGeometry(100, 100, 1000, 750)
        self.program_data = parser.parse_program()
        if not self.program_data:
            self.close(); return
        
        self.start_date = self.get_start_date_from_program()
        self.settings_win = None
        self.current_page_index = 0
        self.setup_ui()
        self.update_progress()
        # self.load_fact() # İlginç Bilgi API isteğini geçici olarak kapattık

    def get_start_date_from_program(self):
        header_str = self.program_data.get("header", "")
        for line in header_str.split('\n'):
            if "Başlangıç Tarihi:" in line:
                try:
                    date_str = line.split(":", 1)[1].strip()
                    day, month, year = map(int, date_str.split('-'))
                    return QDate(year, month, day)
                except (ValueError, IndexError): break
        return QDate.currentDate()

    def setup_ui(self):
        main_widget = QWidget(); self.setCentralWidget(main_widget); main_layout = QHBoxLayout(main_widget)
        sidebar_widget = QWidget(); sidebar_layout = QVBoxLayout(sidebar_widget); sidebar_widget.setFixedWidth(250)
        time_widget_container = TimeWidgets()
        fact_group = QWidget(); fact_group.setObjectName("factCard"); fact_group_layout = QVBoxLayout(fact_group)
        fact_group_layout.addWidget(QLabel(f"<b>{get_string('interesting_fact')}</b>")); self.fact_label = QLabel("..."); self.fact_label.setWordWrap(True); fact_group_layout.addWidget(self.fact_label)
        self.calendar = QCalendarWidget(); self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.clicked.connect(self.calendar_day_clicked)
        button_layout = QHBoxLayout()
        self.new_program_button = QPushButton(get_string("new_program_button")); self.settings_button = QToolButton(); self.settings_button.setText("⚙️"); self.settings_button.setFixedSize(40, 40)
        self.settings_button.clicked.connect(self.open_settings_window); self.new_program_button.clicked.connect(self.open_main_window)
        button_layout.addWidget(self.new_program_button); button_layout.addWidget(self.settings_button)
        brand_label = QLabel("@fawpie"); brand_label.setAlignment(Qt.AlignCenter); brand_label.setStyleSheet("color: #7f8c8d; margin-top: 10px;")
        sidebar_layout.addWidget(self.calendar); sidebar_layout.addWidget(time_widget_container); sidebar_layout.addWidget(fact_group)
        sidebar_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        sidebar_layout.addLayout(button_layout); sidebar_layout.addWidget(brand_label)
        
        content_widget = QWidget(); content_layout = QVBoxLayout(content_widget)
        header_label = QLabel(self.program_data.get("header", "Program")); header_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        
        day_nav_layout = QHBoxLayout()
        self.left_arrow = QToolButton(); self.left_arrow.setArrowType(Qt.LeftArrow); self.left_arrow.clicked.connect(self.prev_page)
        self.right_arrow = QToolButton(); self.right_arrow.setArrowType(Qt.RightArrow); self.right_arrow.clicked.connect(self.next_page)
        self.page_label = QLabel(""); self.page_label.setAlignment(Qt.AlignCenter); self.page_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        day_nav_layout.addWidget(self.left_arrow); day_nav_layout.addWidget(self.page_label); day_nav_layout.addWidget(self.right_arrow)
        day_nav_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.task_pages = SwipeStackedWidget()
        self.task_pages.swiped.connect(lambda direction: self.next_page() if direction == 1 else self.prev_page())
        
        self.populate_task_pages(); self.progress_bar = QProgressBar()
        
        content_layout.addWidget(header_label); content_layout.addLayout(day_nav_layout); content_layout.addWidget(self.task_pages);
        content_layout.addWidget(QLabel(get_string("progress_label"))); content_layout.addWidget(self.progress_bar)
        main_layout.addWidget(sidebar_widget); main_layout.addWidget(content_widget)
        
        content_widget.installEventFilter(self)
        self.update_page_view()

    def eventFilter(self, source, event):
        if event.type() == QEvent.Wheel:
            # Fare tekerleği olayını SwipeStackedWidget'a yönlendir
            delta = event.angleDelta().y()
            if delta > 0: self.prev_page()
            elif delta < 0: self.next_page()
            return True # Olayın işlendiğini belirt
        return super().eventFilter(source, event)

    def load_fact(self):
        self.fact_thread = FactLoaderThread(); self.fact_thread.fact_loaded.connect(self.fact_label.setText); self.fact_thread.start()
    def populate_task_pages(self):
        for division_data in self.program_data.get("weeks", []):
            page_widget = QTreeWidget(); page_widget.setHeaderHidden(True)
            current_main_task = None
            for task_text in division_data.get("tasks", []):
                clean_text = task_text.replace("[ ]", "").strip(); is_subtask = task_text.startswith("    ")
                if not is_subtask:
                    current_main_task = QTreeWidgetItem(page_widget); task_checkbox = QCheckBox(clean_text); task_checkbox.stateChanged.connect(self.update_progress); page_widget.setItemWidget(current_main_task, 0, task_checkbox)
                else:
                    if current_main_task:
                        sub_item = QTreeWidgetItem(current_main_task); sub_checkbox = QCheckBox(clean_text); sub_checkbox.stateChanged.connect(self.update_progress); page_widget.setItemWidget(sub_item, 0, sub_checkbox)
            page_widget.expandAll(); self.task_pages.addWidget(page_widget)
    def calendar_day_clicked(self, q_date):
        if self.start_date:
            days_diff = self.start_date.daysTo(q_date)
            page_index = days_diff 
            if 0 <= page_index < self.task_pages.count(): self.go_to_page(page_index)
    def go_to_page(self, index):
        self.current_page_index = index; self.update_page_view()
    def next_page(self):
        if self.current_page_index < self.task_pages.count() - 1:
            self.current_page_index += 1; self.update_page_view()
    def prev_page(self):
        if self.current_page_index > 0:
            self.current_page_index -= 1; self.update_page_view()
    def update_page_view(self):
        self.task_pages.setCurrentIndex(self.current_page_index)
        current_title = self.program_data["weeks"][self.current_page_index]["title"]
        self.page_label.setText(current_title)
        if self.start_date:
            target_date = self.start_date.addDays(self.current_page_index)
            self.calendar.setSelectedDate(target_date)
    def update_progress(self):
        total_tasks, completed_tasks = 0, 0
        for i in range(self.task_pages.count()):
            tree = self.task_pages.widget(i)
            if tree:
                iterator = QTreeWidgetItemIterator(tree)
                while iterator.value():
                    widget = tree.itemWidget(iterator.value(), 0)
                    if isinstance(widget, QCheckBox):
                        total_tasks += 1
                        if widget.isChecked(): completed_tasks += 1
                    iterator += 1
        if total_tasks > 0: self.progress_bar.setValue(int((completed_tasks / total_tasks) * 100))
        else: self.progress_bar.setValue(0)
    def open_main_window(self):
        from src.gui import MainWindow
        self.main_creator_window = MainWindow(); self.main_creator_window.show(); self.close()
    def open_settings_window(self):
        if self.settings_win is None or not self.settings_win.isVisible():
            self.settings_win = SettingsWindow(); self.settings_win.show()