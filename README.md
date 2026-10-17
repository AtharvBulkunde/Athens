# ATHEN JARVIS — Windows Desktop AI Assistant

A local-first JARVIS-inspired assistant with a cyan HUD interface, browser voice input/output, Ollama local or cloud AI, and a small allowlist of safe desktop actions.

## Features
- Futuristic cyan/blue HUD with animated reactor and live system status.
- Voice input using browser Speech Recognition (browser support varies).
- Spoken replies using browser speech synthesis.
- AI chat through local Ollama or the Ollama Cloud API.
- Optional local offline fallback for basic date/time/help replies.
- Allowlisted actions: Notepad, Calculator, Paint, Google, YouTube, GitHub, date and time.
- Local chat history stored in this browser.
- FastAPI backend for the browser dashboard.

## Requirements
- Windows 10/11
- Python 3.10+
- Current Chrome or Edge recommended for voice input
- Internet access for package installation and Ollama Cloud

## Install and run the browser app
1. Download/extract the project.
2. In PowerShell, from the project folder run:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   Copy-Item .env.example .env
   python -m uvicorn main:app --host 127.0.0.1 --port 8000
   ```

3. Open http://127.0.0.1:8000

## Configure Ollama Cloud or local Ollama

Edit the local `.env` file. **Never commit a real API key to GitHub or put it in browser JavaScript.**

For Ollama Cloud, create a key at https://ollama.com/settings/keys, then set:

```env
OLLAMA_API_KEY=your_new_key_here
OLLAMA_URL=https://ollama.com
OLLAMA_MODEL=gemma4:31b
```

For local Ollama instead, leave `OLLAMA_API_KEY` blank and use:

```env
OLLAMA_API_KEY=
OLLAMA_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.2
```

Restart the app after editing `.env`. The backend sends cloud credentials only in the server-side Authorization header. Never expose the API key in frontend JavaScript or a public repository. Ollama Cloud usage/availability depends on your account and current service limits. See https://docs.ollama.com/api/authentication.

## Native Windows desktop assistant

The repository also includes a separate native PyQt6 desktop app.

1. Install Python 3.12 (recommended for audio dependency compatibility).
2. Double-click `run-desktop.bat`, or use PowerShell:

   ```powershell
   py -3.12 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r desktop-requirements.txt
   Copy-Item .env.example .env
   python desktop_main.py
   ```

3. The desktop app can use the same Ollama Cloud configuration above, or local Ollama with no API key. Type a message or use the voice control if your microphone/audio dependencies work.

### Desktop features and limits
- Native dark/cyan HUD window.
- Typed chat and push-to-talk voice input.
- Speech transcription tries English (India), Marathi, and Hindi; it requires internet for Google's recognition service. Results vary by microphone, installed audio drivers, and language.
- Spoken replies use Windows/system voices available through `pyttsx3`; quality depends on installed voices.
- Persistent memory in a local SQLite database under `memory/`.
- Best-effort DuckDuckGo HTML web search; internet access is required and rate limits/site changes can affect it.
- System status shows CPU, RAM, disk, OS and battery status when available.
- Safe allowlisted local actions. Arbitrary shell commands are not executed.

The native app is a compatible implementation, not a complete port of every MARK LV capability.

## Free local AI alternative
Install Ollama from https://ollama.com/download/windows, then run `ollama pull llama3.2`. Keep Ollama running and set `OLLAMA_API_KEY=` and `OLLAMA_URL=http://127.0.0.1:11434` in your local `.env`.

## Security
- Do not expose the FastAPI development server to the public internet without authentication and security controls.
- Ollama API keys are secrets. Keep them in local environment variables or your hosting provider's secret settings.
- The browser dashboard's app-launch actions execute on the machine running its Python backend. A hosted backend cannot directly open apps on your personal Windows PC. To bridge a hosted website to your local desktop, you still need a separate authenticated local agent and a secure connection; this change connects Ollama AI but does not create that remote-control bridge.

## Structure
```text
Athens/
├── main.py
├── desktop_main.py
├── requirements.txt
├── desktop-requirements.txt
├── .env.example
├── .gitignore
├── run.bat
├── run-desktop.bat
├── README.md
├── desktop/
└── static/
```
