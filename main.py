from pathlib import Path
import datetime
import os
import subprocess
import webbrowser

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

APP_NAME = "ATHEN JARVIS"
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "").strip()
# Use Ollama Cloud automatically when a key is configured, unless OLLAMA_URL overrides it.
OLLAMA_URL = (
    os.getenv("OLLAMA_URL", "").strip().rstrip("/")
    or ("https://ollama.com" if OLLAMA_API_KEY else "http://127.0.0.1:11434")
)
OLLAMA_MODEL = (
    os.getenv("OLLAMA_MODEL", "").strip()
    or ("gpt-oss:120b-cloud" if OLLAMA_API_KEY and OLLAMA_URL.startswith("https://ollama.com") else "llama3.2")
)
OLLAMA_HEADERS = {"Authorization": f"Bearer {OLLAMA_API_KEY}"} if OLLAMA_API_KEY and OLLAMA_URL.startswith("https://") else {}
app = FastAPI(title=APP_NAME, version="1.1.0")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class ActionRequest(BaseModel):
    action: str = Field(min_length=1, max_length=40)


def local_reply(message: str) -> str:
    text = message.lower().strip()
    if any(word in text for word in ("hello", "hi jarvis", "hey jarvis", "hello jarvis")):
        return "Hello. ATHEN JARVIS systems are online. How can I help you?"
    if "time" in text:
        return "The current local time is " + datetime.datetime.now().strftime("%I:%M %p") + "."
    if "date" in text or "today" in text:
        return "Today's date is " + datetime.datetime.now().strftime("%A, %d %B %Y") + "."
    if "help" in text:
        return "I can tell you the date and time, open approved apps and websites, and chat using Ollama local or cloud AI when configured."
    return "The AI engine is not connected. Check OLLAMA_URL, OLLAMA_MODEL and OLLAMA_API_KEY in your local .env file, or start your local Ollama server."


@app.get("/api/health")
def health():
    ollama_available = False
    try:
        ollama_available = requests.get(
            f"{OLLAMA_URL}/api/tags", headers=OLLAMA_HEADERS, timeout=4
        ).ok
    except requests.RequestException:
        pass
    return {
        "status": "online",
        "assistant": APP_NAME,
        "ai_provider": "ollama-cloud" if OLLAMA_API_KEY and OLLAMA_URL.startswith("https://") else "ollama-local",
        "local_ai": "connected" if ollama_available else "offline fallback",
        "model": OLLAMA_MODEL,
    }


@app.post("/api/chat")
def chat(body: ChatRequest):
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            headers=OLLAMA_HEADERS,
            json={
                "model": OLLAMA_MODEL,
                "stream": False,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are ATHEN JARVIS, a helpful assistant. Be concise, clear, and honest. Never claim to have performed a computer action unless the app confirms it.",
                    },
                    {"role": "user", "content": body.message.strip()},
                ],
            },
            timeout=90,
        )
        response.raise_for_status()
        answer = response.json().get("message", {}).get("content", "").strip()
        if answer:
            return {"reply": answer, "engine": "ollama-cloud" if OLLAMA_HEADERS else "ollama-local"}
    except (requests.RequestException, ValueError, KeyError):
        pass
    return {"reply": local_reply(body.message), "engine": "offline"}


@app.post("/api/action")
def run_action(body: ActionRequest):
    action = body.action.strip().lower()
    if action == "time":
        return {"ok": True, "message": "The time is " + datetime.datetime.now().strftime("%I:%M %p") + "."}
    if action == "date":
        return {"ok": True, "message": "Today is " + datetime.datetime.now().strftime("%A, %d %B %Y") + "."}
    apps = {"notepad": ["notepad.exe"], "calculator": ["calc.exe"], "paint": ["mspaint.exe"]}
    if action in apps:
        try:
            subprocess.Popen(apps[action], shell=False)
            return {"ok": True, "message": f"Opening {action.title()}."}
        except OSError:
            raise HTTPException(status_code=500, detail=f"Could not launch {action}. Is it available on this PC?")
    sites = {"youtube": "https://www.youtube.com", "google": "https://www.google.com", "github": "https://github.com"}
    if action in sites:
        webbrowser.open(sites[action], new=2)
        return {"ok": True, "message": f"Opening {action.title()} in your browser."}
    raise HTTPException(status_code=400, detail="Action not allowed. Use Notepad, Calculator, Paint, YouTube, Google, GitHub, date, or time.")


@app.get("/")
def index():
    return FileResponse(BASE_DIR / "static" / "index.html")


app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
