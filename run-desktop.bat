@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  echo Python launcher not found. Install Python 3.11 or 3.12 and enable Add Python to PATH.
  pause
  exit /b 1
)
if not exist ".venv\Scripts\python.exe" py -3.12 -m venv .venv
if not exist ".venv\Scripts\python.exe" (
  echo Could not create the virtual environment. Install Python 3.12 or edit this script to use your installed version.
  pause
  exit /b 1
)
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
python -m pip install -r desktop-requirements.txt
if not exist ".env" copy ".env.example" ".env"
python desktop_main.py
pause
