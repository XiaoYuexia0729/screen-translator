"""
Configuration file
Set Tesseract path if not installed in default location
"""

import pytesseract
import os

# Windows default installation path
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Check if path exists and set it
if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
    print(f'Tesseract found at: {TESSERACT_PATH}')
else:
    print(f'Warning: Tesseract not found at {TESSERACT_PATH}')
    print('Please install Tesseract or update the path in config.py')
