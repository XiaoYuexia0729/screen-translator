@echo off
title Building Screen Translator EXE

echo ========================================
echo   Building Screen Translator EXE
echo ========================================
echo.

REM Check Python version
python -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python 3.9 or higher is required!
    echo.
    pause
    exit /b 1
)

REM Check if PyInstaller is installed
python -m PyInstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo Failed to install PyInstaller!
        pause
        exit /b 1
    )
    echo.
)

echo.
echo Building executable...
echo This may take a few minutes...
echo.

REM Use python -m to run PyInstaller
python -m PyInstaller --clean --noconfirm ScreenTranslator.spec

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   Build Complete!
    echo ========================================
    echo.
    echo The executable is located at:
    echo   dist\ScreenTranslator.exe
    echo.
    echo You can now:
    echo 1. Run dist\ScreenTranslator.exe
    echo 2. Create a desktop shortcut to dist\ScreenTranslator.exe
    echo 3. Move dist\ScreenTranslator.exe anywhere you want
    echo.
    echo Note: Make sure Tesseract is installed at:
    echo   C:\Program Files\Tesseract-OCR\
    echo.
) else (
    echo.
    echo Build failed! Please check the error messages above.
    echo.
)

pause
