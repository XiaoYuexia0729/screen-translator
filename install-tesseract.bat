@echo off
title Tesseract OCR Installer

echo ========================================
echo   Tesseract OCR Installer
echo ========================================
echo.

REM Check if already installed
if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
    echo Tesseract OCR is already installed!
    echo Location: C:\Program Files\Tesseract-OCR\
    echo.
    pause
    exit /b 0
)

echo This will open the Tesseract download page in your browser.
echo.
echo Steps to follow:
echo 1. Find "Tesseract at UB Mannheim" section
echo 2. Click the first Windows installer link
echo 3. Save and run the downloaded file
echo 4. During installation:
echo    - Select English language pack
echo    - Install to: C:\Program Files\Tesseract-OCR
echo.
pause

start https://github.com/UB-Mannheim/tesseract/wiki

echo.
echo Browser opened with download page.
echo.
echo After installing Tesseract, run run.bat to start the translator.
echo.
pause
