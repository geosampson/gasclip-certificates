@echo off
echo Starting GasClip Certificates Generator...
python app.py
if errorlevel 1 (
    echo.
    echo ERROR: Failed to start the application
    echo Make sure you have run install_windows.bat first
    pause
)
