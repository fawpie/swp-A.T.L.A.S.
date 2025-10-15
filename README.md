# 🚀 A.T.L.A.S.  
**A**I-powered **T**ask & **L**ife **A**rrangement **S**ystem  
*Create, track and complete **any** plan – from exam prep to world trips – in under 30 seconds.*

---

## 📌 What is A.T.L.A.S.?
A.T.L.A.S. is a **cross-platform desktop app** that turns **plain-English prompts** into **step-by-step daily plans** and helps you **check-off every task** until the goal is reached.

| Made for | Works for |
|----------|-----------|
| Students | Exam calendars, assignment schedules |
| Travellers | City itineraries, backpacking routes |
| Event planners | Weddings, conferences, birthdays |
| Freelancers | Client projects, content calendars |
| Literally **anyone** | Any goal with a deadline |

---

## ✨ Key Features
| Feature | Description |
|---------|-------------|
| **AI Plan Generator** | Google Gemini under the hood – type a goal, get a day-by-day plan in seconds |
| **Visual Tracker** | Calendar + checkable tree + progress bar |
| **Time Tools** | Clock, stop-watch, Pomodoro timer (25 min default) |
| **Themes** | Dark, Light, Nord, Dracula – switch instantly |
| **Languages** | Turkish, English, German, Spanish, French |
| **Offline First** | Plans are stored locally (JSON + txt) |
| **Portable Builds** | Windows (.exe), Linux (.AppImage), macOS (.dmg) – no admin rights needed |
| **Auto-Re-start** | Change settings → app exits with code 10 → launcher auto-restarts |
| **Fun Facts** | Daily interesting-fact card (Gemini, your language) |

---

## 🎬 30-Second Demo
1. Open A.T.L.A.S.  
2. Enter *"7-day Istanbul sightseeing trip"*, duration *"1 week"*, type *"Daily"*, language *"English"*.  
3. Click **✨ Create Program** → AI writes `program.txt` → tracker opens automatically.  
4. Tick tasks day-by-day → watch progress bar grow.  
5. Use built-in Pomodoro timer to stay focused.

---

## 📸 Screenshots
*(Light theme shown – switch in one click)*

| Plan Creator | Daily Tracker | Time Widgets |
|--------------|---------------|--------------|
| ![creator]() | ![tracker]() | ![timer]() |

---

## 🛠️ Tech Stack
| Layer | Tech |
|-------|------|
| GUI | PyQt5 → migrating to **PySide6** (LGPL) |
| AI | Google Gemini 1.5 Flash |
| Settings | QSettings (native OS backend) |
| Packaging | PyInstaller + GitHub Actions |
| i18n | Python-native string dictionary |
| Styling | QSS (Qt-Style-Sheets) |

---

## 📦 Installation
### Windows (portable)
1. Download `ATLAS_win64.zip` from [Releases]()  
2. Unzip → double-click `ATLAS.exe`  
3. *(Optional)* Add folder to antivirus whitelist (false-positive rate < 1 %)

### Linux
```bash
wget https://github.com/yourname/ATLAS/releases/latest/download/ATLAS.AppImage
chmod +x ATLAS.AppImage
./ATLAS.AppImage
```

### macOS
```bash
brew install --cask atlas-plan
# or drag ATLAS.dmg → Applications
```

### Build from Source
```bash
git clone https://github.com/yourname/ATLAS.git
cd ATLAS
python -m venv venv
source venv/bin/activate  # win: venv\Scripts\activate
pip install -r requirements.txt
python -m src.main
```

---

## 🔑 First Launch
1. Choose language & theme  
2. Click **Continue** – that's it.  
   *(You can change both later via ⚙️ Settings.)*

---

## 🧪 Custom AI Prompts
Edit `src/automator.py` → `prompt` variable.  
Example for **meal-prep**:
```python
goal = "4-week vegetarian meal-prep plan"
duration = "4 weeks"
program_type = "Weekly"
program_language = "en"
```
Any prompt works – the stricter the instructions, the better the output.

---

## 📁 File Structure
```
ATLAS/
├── src/                    # Python package
│   ├── main.py            # Entry point
│   ├── gui.py             # Plan creator
│   ├── tracker_window.py  # Day-by-day tracker
│   ├── automator.py       # Gemini wrapper
│   ├── parser.py          # txt → dict
│   ├── time_widgets.py    # Clock, timer, stopwatch
│   ├── translations.py    # i18n strings
│   └── styles/            # *.qss theme files
├── logs/                  # Runtime logs (auto-created)
├── program.txt            # Your current plan (auto-created)
├── config.json            # Settings (auto-created)
├── requirements.txt
├── start.bat & start.sh   # Auto-restart launchers
└── docs/                  # Screenshots, logos
```

---

## 🔄 Auto-Restart Magic
Changing language or theme exits the app with **exit code 10**.  
The launcher script catches this and instantly restarts A.T.L.A.S. – no manual intervention.

---

## 🌍 Roadmap
| Version | Feature |
|---------|---------|
| 1.2 | Mobile companion (Kivy → Android APK) |
| 1.3 | Cloud sync (WebDAV, Google Drive) |
| 1.4 | Shared plans – send a link, friend imports |
| 1.5 | Plugin system – write your own parsers |

---

## 🤝 Contributing
We love PRs!  
1. Fork → feature branch → commit → push → open PR  
2. Please run `black src/` & `pytest` before submitting  
3. Add a test for new parsers / widgets

---

## 📄 License
**MIT** – see [LICENSE](LICENSE).  
*(PyQt5 parts are GPL-compatible; we are migrating to PySide6 for full MIT compliance in v1.1)*

---

## ☕ Support
| Type | Link |
|------|------|
| Bug Report | [GitHub Issues]() |
| Discussions | [GitHub Discussions]() |
| Buy Me a Coffee | [buymeacoffee.com/fawpie]) |

---

**Plan anything. Track everything. Finish what you start.**  
*ATLAS – your personal AI planner.*
