@echo off
title Abstractive Summarizer (UTF-8 Enabled)

REM --- Set console to UTF-8 for proper Hindi display ---
chcp 65001 >nul
set PYTHONIOENCODING=utf-8

REM --- Optional: Increase buffer size for clean display ---
mode con: cols=120 lines=500

REM --- Activate virtual environment ---
echo Activating virtual environment...
call ".venv\Scripts\activate.bat"

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Unable to activate virtual environment!
    echo Make sure your venv folder exists at:
    echo     %cd%\.venv
    echo.
    pause
    exit /b
)

REM --- Run Python summarizer ---
echo Running summarizer script...
python interactive_summarizer_withHindi.py

echo.
echo =====================================================
echo Summary program finished.
echo Press any key to close window...
pause >nul
