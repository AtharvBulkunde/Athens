"""Lightweight language detection for English, Hindi and Marathi voice input."""
import re

DEVANAGARI = re.compile(r"[\u0900-\u097F]")
MARATHI_HINTS = {
    "आहे", "आहेस", "मला", "काय", "कर", "करा", "उघड", "सांग", "वेळ",
    "धन्यवाद", "माझे", "माझं", "तू", "कुठे", "हो", "नाही", "चालू",
}


def detect_language(text: str) -> tuple[str, str]:
    """Return (display name, speech locale)."""
    value = (text or "").strip().lower()
    if not value:
        return "English", "en-IN"
    if DEVANAGARI.search(value):
        words = set(value.split())
        if words & MARATHI_HINTS:
            return "Marathi", "mr-IN"
        return "Hindi", "hi-IN"
    return "English", "en-IN"


def voice_locale_for(language_name: str) -> str:
    return {"Marathi": "mr-IN", "Hindi": "hi-IN"}.get(language_name, "en-IN")
