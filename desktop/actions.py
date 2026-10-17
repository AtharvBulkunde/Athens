"""Allowlisted desktop actions. Arbitrary shell commands are never executed."""
import platform
import subprocess
import webbrowser

ALLOWED_APPS = {
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "paint": ["mspaint.exe"],
}
ALLOWED_SITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://github.com",
    "gmail": "https://mail.google.com",
}


def run_allowed_action(text: str) -> str | None:
    value = (text or "").strip().lower()
    for name, command in ALLOWED_APPS.items():
        if value in {f"open {name}", f"launch {name}", name}:
            if platform.system() != "Windows":
                return f"{name.title()} launcher is configured for Windows."
            try:
                subprocess.Popen(command, shell=False)
                return f"Opening {name.title()}."
            except OSError as exc:
                return f"Could not open {name.title()}: {exc}"
    for name, url in ALLOWED_SITES.items():
        if value in {f"open {name}", f"launch {name}", name, f"go to {name}"}:
            webbrowser.open(url)
            return f"Opening {name.title()} in your browser."
    if value in {"what time is it", "tell me the time", "time"}:
        from datetime import datetime
        return f"The current time is {datetime.now().astimezone().strftime('%I:%M %p')}."
    if value in {"what is today's date", "today's date", "date"}:
        from datetime import date
        return f"Today is {date.today().strftime('%d %B %Y')}."
    return None
