from .settings import SETTINGS

STRINGS = {
    "tr": {
        "welcome_title": "A.T.L.A.S.'a Hoş Geldiniz", "choose_language": "Lütfen bir dil seçin:", "continue_button": "Devam Et",
        "creator_window_title": "A.T.L.A.S. - Yeni Program Oluştur", "goal_label": "Programın Amacı:", "duration_label": "Süre:",
        "type_label": "Program Tipi:", "language_label": "Program Dili:", "create_button": "✨ Programı Oluştur",
        "log_label": "İşlem Günlüğü:", "tracker_window_title": "A.T.L.A.S. - Program Takibi",
        "progress_label": "Genel İlerleme:", "new_program_button": "Yeni Program Oluştur",
        "settings_window_title": "Ayarlar", "theme_label": "Uygulama Teması:", "save_button": "Kaydet ve Yeniden Başlat",
        "restart_notice": "Değişikliklerin etkili olması için uygulama yeniden başlatılacak.", "calendar": "Takvim",
        "settings": "Ayarlar", "app_reset": "Uygulamayı Sıfırla (Debug)", "reset_confirm_title": "Sıfırlamayı Onayla",
        "reset_confirm_text": "Tüm ayarları ve mevcut programı silmek istediğinizden emin misiniz? Bu işlem geri alınamaz.",
        "interesting_fact": "İlginç Bilgi",
    },
    "en": {
        "welcome_title": "Welcome to A.T.L.A.S.", "choose_language": "Please select a language:", "continue_button": "Continue",
        "creator_window_title": "A.T.L.A.S. - Create New Program", "goal_label": "Program Goal:", "duration_label": "Duration:",
        "type_label": "Program Type:", "language_label": "Program Language:", "create_button": "✨ Create Program",
        "log_label": "Activity Log:", "tracker_window_title": "A.T.L.A.S. - Program Tracker",
        "progress_label": "Overall Progress:", "new_program_button": "Create New Program",
        "settings_window_title": "Settings", "theme_label": "Application Theme:", "save_button": "Save and Restart",
        "restart_notice": "The application will restart for the changes to take effect.", "calendar": "Calendar",
        "settings": "Settings", "app_reset": "Reset Application (Debug)", "reset_confirm_title": "Confirm Reset",
        "reset_confirm_text": "Are you sure you want to delete all settings and the current program? This action cannot be undone.",
        "interesting_fact": "Interesting Fact",
    },
    # Diğer diller buraya eklenebilir
}

def get_string(key):
    lang = SETTINGS.get("language", "en")
    return STRINGS.get(lang, STRINGS["en"]).get(key, key)