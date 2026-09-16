@echo off
title Test Dependencies

echo ========================================
echo   Testing Python Dependencies
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [FAIL] Python not found
    pause
    exit /b 1
)

echo [OK] Python version:
python --version
echo.

REM Check Python version
python -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)" >nul 2>&1
if %errorlevel% neq 0 (
    echo [FAIL] Python version too old (requires 3.9+)
    pause
    exit /b 1
)

echo [OK] Python version compatible
echo.

echo Testing imports...
echo.

python -c "import PyQt5; print('[OK] PyQt5')" 2>nul || echo [FAIL] PyQt5 not installed
python -c "import pytesseract; print('[OK] pytesseract')" 2>nul || echo [FAIL] pytesseract not installed
python -c "import PIL; print('[OK] Pillow')" 2>nul || echo [FAIL] Pillow not installed
python -c "import mss; print('[OK] mss')" 2>nul || echo [FAIL] mss not installed
python -c "import deep_translator; print('[OK] deep-translator')" 2>nul || echo [FAIL] deep-translator not installed
python -c "import numpy; print('[OK] numpy')" 2>nul || echo [FAIL] numpy not installed
python -c "import translators; print('[OK] translators')" 2>nul || echo [FAIL] translators not installed

echo.
echo ========================================

if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
    echo [OK] Tesseract OCR installed
) else (
    echo [FAIL] Tesseract OCR not found
    echo       Install using: install-tesseract.bat
)

echo ========================================
echo.
pause
