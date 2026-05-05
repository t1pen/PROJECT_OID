@echo off
REM EDA Interactive Dashboard - Quick Start Script

echo.
echo ============================================
echo   EDA Interactive Dashboard Launcher
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not available
    echo Please ensure Python is properly installed
    pause
    exit /b 1
)

echo [OK] pip found
echo.

REM Install dependencies
echo Installing required packages...
echo This may take a few minutes...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [OK] Dependencies installed successfully
echo.

REM Launch Streamlit app
echo Launching EDA Interactive Dashboard...
echo.
echo The app will open in your browser at: http://localhost:8501
echo Press Ctrl+C to stop the app
echo.

streamlit run app.py

pause
