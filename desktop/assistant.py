"""Response engine: optional Gemini API, safe local actions, and offline fallback."""
import os
import requests

from desktop.actions import run_allowed_action
from desktop.language_manager import detect_language

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"


class AssistantEngine:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()

    def reply(self, user_text: str) -> tuple[str, str]:
        language, _locale = detect_language(user_text)
        action_reply = run_allowed_action(user_text)
        if action_reply:
            return action_reply, language
        if not user_text.strip():
            return "Please say or type a command.", language
        if self.api_key:
            try:
                response = requests.post(
                    GEMINI_URL,
                    params={"key": self.api_key},
                    json={"contents": [{"parts": [{"text":
                        "You are ATHEN JARVIS, a helpful Windows desktop assistant. "
                        "Reply in the same language as the user's latest message. "
                        "Use concise, clear responses. Never claim you performed a computer action "
                        "unless the local action handler confirms it. User: " + user_text
                    }]}]},
                    timeout=25,
                )
                response.raise_for_status()
                data = response.json()
                answer = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                return answer, language
            except (requests.RequestException, KeyError, IndexError, ValueError) as exc:
                return f"I couldn't reach the AI service. Check your connection or API key. ({exc})", language
        return (
            "I can open approved apps and websites, tell the time/date, and handle basic commands. "
            "For general AI conversation, add GEMINI_API_KEY to your local .env file. "
            "The key is not included in GitHub.",
            language,
        )
