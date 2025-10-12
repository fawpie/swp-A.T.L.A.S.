import json
import os

CONFIG_FILE = "config.json"

def get_default_settings():
    return {
        "language": "en",
        "theme": "dark",
        "first_launch_completed": False
    }

def load_settings():
    if not os.path.exists(CONFIG_FILE):
        return get_default_settings()
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return get_default_settings()

def save_settings(settings):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Ayarlar kaydedilirken hata oluştu: {e}")

SETTINGS = load_settings()