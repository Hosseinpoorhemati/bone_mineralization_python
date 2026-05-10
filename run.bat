@echo off
REM Quick launcher script for Bone Mineralization Simulator (Windows)

echo.
echo Bone Mineralization Integrated Model - Python Version
echo ==================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed. Please install Python 3.8 or later.
    pause
    exit /b 1
)

echo OK: Python found.
echo.

REM Install/update dependencies
echo Installing/updating dependencies...
pip install -q -r requirements.txt

if errorlevel 1 (
    echo Error: Failed to install dependencies.
    pause
    exit /b 1
)

echo OK: Dependencies installed successfully.
echo.

echo Launching Bone Mineralization Simulator...
echo.
echo    Opening at: http://localhost:8501
echo    Press Ctrl+C to stop the server
echo.

REM Run the single-page app
streamlit run app_single.py

pause
