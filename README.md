# ATHEN JARVIS — Windows Desktop AI Assistant

A local-first JARVIS-inspired assistant with a cyan HUD interface, browser voice input/output, optional local AI via Ollama, and a small allowlist of safe desktop actions.

## Features
- Futuristic cyan/blue HUD with animated reactor and live system status.
- Voice input using browser Speech Recognition (browser support varies).
- Spoken replies using browser speech synthesis.
- AI chat with a local Ollama model; no cloud API key is required.
- Offline fallback for basic date/time/help replies.
- Allowlisted actions: Notepad, Calculator, Paint, Google, YouTube, GitHub, date and time.
- Local chat history stored in this browser.
- FastAPI backend bound to localhost by the launcher.

## Requirements
- Windows 10/11
- Python 3.10+
- Current Chrome or Edge recommended for voice input
- Optional: Ollama for full local AI chat

## Install and run
1. Extract/download the project.
2. Double-click `run.bat`, or in PowerShell run:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   py -m pip install -r requirements.txt
   Copy-Item .env.example .env
   py -m uvicorn main:app --host 127.0.0.1 --port 8000
   ```

3. Open http://127.0.0.1:8000

Package installation requires internet access.

## Native Windows desktop assistant (MARK LV-inspired)

The repository also includes a separate **native PyQt6 desktop app**. It does not replace the existing browser dashboard.

### Run the desktop app
1. Install **Python 3.12** (recommended for audio dependency compatibility).
2. Double-click `run-desktop.bat`, or use PowerShell:
   ```powershell
   py -3.12 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r desktop-requirements.txt
   Copy-Item .env.example .env
   python desktop_main.py
   ```
3. Type a message, or press **VOICE** and allow microphone access at the Windows level if requested.
4. For AI chat, add your own Gemini API key to the local `.env` file as `GEMINI_API_KEY=your_key_here`. Never commit a real key.

### Desktop features and limits
- Native dark/cyan HUD window.
- Typed chat and push-to-talk voice input.
- Speech transcription tries English (India), Marathi, and Hindi; it requires internet for Google's recognition service. Results may vary by microphone, installed audio drivers, and language.
- Spoken replies use Windows/system voices available through `pyttsx3`; voice language quality depends on installed voices.
- Optional Gemini text API for conversational responses; usage and availability depend on the provider's current account limits.
- Safe allowlisted local actions: Notepad, Calculator, Paint, selected websites, date, and time.
- The desktop app is a **new compatible implementation**, not a complete port of every MARK LV capability. It does not yet include Gemini Live streaming, holographic avatar/lip-sync, plugin marketplace, persistent long-term memory, remote dashboard, or autonomous background monitoring.

### Desktop source structure
```text
desktop_main.py
desktop-requirements.txt
run-desktop.bat
desktop/
  assistant.py
  actions.py
  language_manager.py
  voice.py
  ui.py
```

### Advanced free local features

The native app also includes these no-key features:
- **Persistent memory:** `remember that my project is ATHEN JARVIS`, then `what do you remember`. Notes are stored in a local SQLite database under `memory/` on this PC.
- **Web search:** `search web for Python 3.12 setup`. This uses a best-effort DuckDuckGo HTML results parser, not an official search API; internet access is required and site changes/rate limits can break results.
- **System status:** type `system status` to view CPU, RAM, disk usage, OS and battery status when available.
- **Safe desktop actions:** `open notepad`, `open calculator`, `open paint`, `open youtube`, `open github`, plus date/time. Arbitrary shell commands are not executed.

### Updated desktop setup

From the extracted project folder in PowerShell:
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r desktop-requirements.txt
Copy-Item .env.example .env
python desktop_main.py
```
Or double-click `run-desktop.bat`. Python's Windows documentation recommends using the `py` launcher and `python -m pip` for installing packages. <https://docs.python.org/3.12/installing/>

**Free-only AI:** Gemini is optional. For local AI chat without a cloud API key, install [Ollama for Windows](https://github.com/ollama/ollama/blob/main/docs/windows.mdx), open PowerShell and run `ollama pull llama3.2`, then keep Ollama running. The desktop app will try the local Ollama model when `GEMINI_API_KEY` is not set. Model download size and performance depend on your PC. You can configure `OLLAMA_URL` and `OLLAMA_MODEL` in your local `.env` file.

## Enable free local AI
1. Install Ollama from https://ollama.com/download/windows
2. Run:

   ```powershell
   ollama pull llama3.2
   ```

3. Keep Ollama running and restart ATHEN JARVIS.

Model downloads can require several GB of disk space and sufficient RAM. Without Ollama, the app still works with a limited offline fallback.

## Voice
- Click **MIC**, allow microphone access, speak, then review the recognized text before sending.
- Click **SPEAK** to read the latest assistant response aloud.
- Speech recognition support depends on browser and OS; some recognition providers may need internet.

## Safe desktop actions
- `open notepad`
- `open calculator`
- `open paint`
- `open google`
- `open youtube`
- `open github`
- `what time is it`
- `what is today's date`

Only named allowlisted actions can be launched; arbitrary terminal commands are not executed. Do not expose the server to your network or public internet without authentication and security controls.

## Structure
```text
Athens/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── run.bat
├── README.md
└── static/
    ├── index.html
    ├── style.css
    └── app.js
```
