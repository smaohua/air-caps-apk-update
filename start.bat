@echo off
REM Air-Caps Smart Glasses Rework Tool Launcher
REM This batch file launches the rework tool on Windows

echo ================================================
echo  Air-Caps Smart Glasses Rework Tool
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://www.python.org/
    pause
    exit /b 1
)

REM Check if ADB is available
adb version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] ADB is not found in PATH
    echo Please install Android SDK Platform Tools
    echo The application will start but device detection may not work
    echo.
    timeout /t 3 >nul
)

REM Start the application
echo Starting Air-Caps Rework Tool...
echo.
python main.py

REM If the application exits with an error
if errorlevel 1 (
    echo.
    echo [ERROR] Application exited with an error
    pause
)
