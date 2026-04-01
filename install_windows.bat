@echo off
echo === Hashcash Installation Script for Windows ===
echo.

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.8 or higher from https://www.python.org/downloads/
    echo After installing Python, run this script again.
    pause
    exit /b 1
)

echo Installing required packages...
pip install -r requirements.txt

echo.
echo === Installation complete! ===
echo To run the application, use: python hashcash.py
echo.
pause
