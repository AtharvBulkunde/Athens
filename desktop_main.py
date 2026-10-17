"""Native ATHEN JARVIS desktop entry point.

Run with: py -m pip install -r desktop-requirements.txt
          py desktop_main.py
"""
from pathlib import Path
import sys

from dotenv import load_dotenv
from PyQt6.QtWidgets import QApplication


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def main() -> int:
    from desktop.ui import JarvisWindow

    app = QApplication(sys.argv)
    app.setApplicationName("ATHEN JARVIS")
    app.setStyle("Fusion")
    window = JarvisWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
