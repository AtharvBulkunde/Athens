"""Compact native cyan HUD UI for ATHEN JARVIS."""
from datetime import datetime
import threading

from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QLineEdit,
    QPushButton, QMessageBox, QFrame
)

from desktop.assistant import AssistantEngine
from desktop.voice import listen_once, speak


class UiSignals(QObject):
    message = pyqtSignal(str, str)
    status = pyqtSignal(str)


class JarvisWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.engine = AssistantEngine()
        self.signals = UiSignals()
        self.signals.message.connect(self.add_message)
        self.signals.status.connect(self.set_status)
        self.setWindowTitle("ATHEN JARVIS — Desktop Command Center")
        self.resize(980, 700)
        self.setMinimumSize(700, 520)
        self.setStyleSheet("""
            QWidget { background:#050b13; color:#dffaff; font-family:'Segoe UI'; }
            QLabel#title { color:#55eaff; font-size:25px; font-weight:700; letter-spacing:3px; }
            QLabel#status { color:#6faab8; font-size:12px; }
            QTextEdit { background:#081522; border:1px solid #16495b; border-radius:12px;
                        padding:14px; font-size:14px; }
            QLineEdit { background:#0b1925; border:1px solid #1c6174; border-radius:9px;
                        padding:12px; color:#effcff; }
            QPushButton { background:#0b3443; border:1px solid #36cce5; border-radius:9px;
                          padding:11px 17px; color:#e8fcff; font-weight:600; }
            QPushButton:hover { background:#125064; }
            QFrame#header { border:1px solid #123d4b; border-radius:12px; }
        """)
        root = QVBoxLayout(self)
        root.setContentsMargins(22, 20, 22, 20)
        root.setSpacing(14)
        header = QFrame()
        header.setObjectName("header")
        h = QHBoxLayout(header)
        brand = QVBoxLayout()
        title = QLabel("ATHEN JARVIS")
        title.setObjectName("title")
        subtitle = QLabel("NATIVE DESKTOP ASSISTANT  /  VOICE • AI • SAFE ACTIONS")
        subtitle.setObjectName("status")
        brand.addWidget(title)
        brand.addWidget(subtitle)
        h.addLayout(brand)
        h.addStretch()
        self.status = QLabel("SYSTEM ONLINE")
        self.status.setObjectName("status")
        h.addWidget(self.status)
        root.addWidget(header)
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        root.addWidget(self.chat, 1)
        controls = QHBoxLayout()
        self.prompt = QLineEdit()
        self.prompt.setPlaceholderText("Type a message or command…")
        self.prompt.returnPressed.connect(self.send_text)
        self.send_button = QPushButton("SEND")
        self.send_button.clicked.connect(self.send_text)
        self.mic_button = QPushButton("🎙 VOICE")
        self.mic_button.clicked.connect(self.start_listening)
        controls.addWidget(self.prompt, 1)
        controls.addWidget(self.mic_button)
        controls.addWidget(self.send_button)
        root.addLayout(controls)
        self.add_message("ATHEN", "System ready. Try “open notepad”, “open YouTube”, or speak in English, Hindi, or Marathi.")

    def set_status(self, value: str):
        self.status.setText(value)

    def add_message(self, speaker: str, message: str):
        stamp = datetime.now().strftime("%H:%M:%S")
        safe = message.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
        self.chat.append(f'<span style="color:#5eeaff">[{stamp}] {speaker}</span><br>{safe}<br>')

    def send_text(self):
        text = self.prompt.text().strip()
        if not text:
            return
        self.prompt.clear()
        self.add_message("YOU", text)
        self.set_status("THINKING…")
        self.send_button.setEnabled(False)
        threading.Thread(target=self._process, args=(text,), daemon=True).start()

    def _process(self, text: str):
        answer, language = self.engine.reply(text)
        self.signals.message.emit(f"ATHEN · {language.upper()}", answer)
        self.signals.status.emit("SYSTEM ONLINE")
        speak(answer)
        self.send_button.setEnabled(True)

    def start_listening(self):
        self.mic_button.setEnabled(False)
        self.set_status("LISTENING…")
        threading.Thread(target=self._listen_worker, daemon=True).start()

    def _listen_worker(self):
        try:
            text = listen_once()
            self.signals.message.emit("YOU · VOICE", text)
            self.signals.status.emit("THINKING…")
            answer, language = self.engine.reply(text)
            self.signals.message.emit(f"ATHEN · {language.upper()}", answer)
            speak(answer)
            self.signals.status.emit("SYSTEM ONLINE")
        except Exception as exc:
            self.signals.message.emit("VOICE", str(exc))
            self.signals.status.emit("SYSTEM ONLINE")
        finally:
            self.mic_button.setEnabled(True)
