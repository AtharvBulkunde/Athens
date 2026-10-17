"""Push-to-talk microphone input and speech output helpers."""
import threading

import pyttsx3
import speech_recognition as sr

from desktop.language_manager import detect_language


def listen_once(timeout: int = 5, phrase_time_limit: int = 12) -> str:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.35)
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    # Start with locale detection unavailable before transcription; try common locales.
    for locale in ("en-IN", "mr-IN", "hi-IN"):
        try:
            text = recognizer.recognize_google(audio, language=locale)
            if text.strip():
                return text.strip()
        except sr.UnknownValueError:
            continue
        except sr.RequestError as exc:
            raise RuntimeError(f"Speech recognition service unavailable: {exc}") from exc
    raise RuntimeError("I couldn't understand that. Please try speaking more clearly.")


def speak(text: str) -> None:
    """Speak asynchronously so the UI remains responsive."""
    def worker():
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception:
            # Text remains available in the UI if no compatible speech voice is installed.
            pass
    threading.Thread(target=worker, daemon=True).start()
