@echo off
echo ================================================================================
echo   Installing OCR Dependencies for Image Upload Feature
echo ================================================================================
echo.

cd backend

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing OCR packages...
echo.

pip install pytesseract==0.3.10
pip install Pillow==10.1.0
pip install opencv-python==4.8.1.78
pip install easyocr==1.7.1

echo.
echo ================================================================================
echo   Installation Complete!
echo ================================================================================
echo.
echo IMPORTANT: Install Tesseract OCR binary:
echo 1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
echo 2. Install to: C:\Program Files\Tesseract-OCR
echo 3. Add to PATH or set TESSERACT_CMD environment variable
echo.
echo Note: EasyOCR will download models (~100MB) on first use
echo.
echo ================================================================================
pause

