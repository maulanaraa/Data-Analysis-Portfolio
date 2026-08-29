@echo off
title Executive Dashboard Superstore Runner
echo ========================================================
echo   Starting Executive Dashboard - Superstore (Streamlit)
echo ========================================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python tidak ditemukan! Silakan install Python dari python.org.
    pause
    exit /b
)

if not exist "venv" (
    echo Membuat virtual environment 'venv'...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Menginstall dependensi...
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

echo Menjalankan aplikasi Streamlit...
streamlit run app.py
pause
