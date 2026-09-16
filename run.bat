@echo off
title Screen Translator

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ========================================
    echo   ERROR: Python not found
    echo ========================================
    echo.
    echo Please install Python 3.9 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

REM Check Python version (requires 3.9+)
python -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)" >nul 2>&1
if %errorlevel% neq 0 (
    echo ========================================
    echo   ERROR: Python version too old
    echo ========================================
    echo.
    echo This program requires Python 3.9 or higher.
    echo Your current version:
    python --version
    echo.
    echo Please upgrade Python from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Check dependencies
python -c "import PyQt5" >nul 2>&1
if %errorlevel% neq 0 (
    echo ========================================
    echo   Installing Python dependencies...
    echo ========================================
    echo.
    echo This may take a few minutes...
    echo.
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo.
        echo ========================================
        echo   ERROR: Failed to install dependencies
        echo ========================================
        echo.
        echo Please check your internet connection and try again.
        echo.
        pause
        exit /b 1
    )
    echo.
    echo Dependencies installed successfully!
    echo.
)

REM Check Tesseract
if not exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
    echo ========================================
    echo   WARNING: Tesseract OCR not found
    echo ========================================
    echo.
    echo Tesseract OCR is required for text recognition.
    echo.
    echo To install Tesseract:
    echo   - Run: install-tesseract.bat
    echo   - Or download from: https://github.com/UB-Mannheim/tesseract/wiki
    echo.
    pause
    exit /b 1
)

REM Start the application
cls
echo ========================================
echo   Starting Screen Translator...
echo ========================================
echo.
python main.py

REM Check if program exited with error
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo   Program Error
    echo ========================================
    echo.
    echo The program exited with an error.
    echo.
    echo Possible causes:
    echo   - Missing Python dependencies
    echo   - Tesseract not properly installed
    echo   - Configuration error
    echo.
    echo Try running: pip install -r requirements.txt
    echo.
)

pause
