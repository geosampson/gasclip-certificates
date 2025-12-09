@echo off
echo ========================================
echo GasClip Certificates Generator
echo Windows Installation Script
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

python --version
echo.

echo Installing required packages...
echo.

pip install PyPDF2==3.0.1
pip install reportlab==4.0.7
pip install Pillow==10.1.0

echo.
echo ========================================
echo Installation complete!
echo ========================================
echo.
echo To run the application, double-click: run_app.bat
echo Or run: python app.py
echo.
pause
