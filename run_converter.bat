@echo off
echo Starting PDF to Word Converter...
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.7 or higher from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

:: Check if requirements are installed
echo Checking dependencies...
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Failed to install dependencies.
        pause
        exit /b 1
    )
)

:: Run the application
echo Starting application...
python run.py %*

pause