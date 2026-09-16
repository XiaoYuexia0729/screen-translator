@echo off
title Install Python Dependencies

echo ========================================
echo   Python Dependencies Installer
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo.
    echo Please install Python 3.9+ from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Check Python version
python -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python version too old!
    echo.
    echo This program requires Python 3.9 or higher.
    echo Your version:
    python --version
    echo.
    echo Please upgrade from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python version check passed!
python --version
echo.

echo Installing dependencies from requirements.txt...
echo This may take a few minutes...
echo.

pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   Installation Complete!
    echo ========================================
    echo.
    echo All dependencies installed successfully.
    echo You can now run: run.bat
    echo.
) else (
    echo.
    echo ========================================
    echo   Installation Failed
    echo ========================================
    echo.
    echo Please check:
    echo 1. Internet connection is working
    echo 2. pip is up to date: python -m pip install --upgrade pip
    echo 3. No firewall blocking pip
    echo.
)

pause
