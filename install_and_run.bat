@echo off
REM Windows installation script for vibe-local
REM This script sets up the environment and installs dependencies

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║           vibe-local Installation Script (Windows)            ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo ❌ Error: Python is not installed or not in PATH
    echo.
    echo Please install Python from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VER=%%i
echo ✓ Found: %PYTHON_VER%
echo.

REM Install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

if !errorlevel! neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ✓ Installation complete!
echo.
echo Configuration:
echo   1. Set environment variables:
echo      - For Azure OpenAI:
echo        set AZURE_OPENAI_API_KEY=your_key_here
echo        set AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
echo        set AZURE_OPENAI_DEPLOYMENT=gpt-4-turbo
echo      - OR for Google Gemini:
echo        set GEMINI_API_KEY=your_key_here
echo.
echo   2. Create data folder:
echo      mkdir %%LOCALAPPDATA%%\vibe-local\data
echo.
echo   3. Create Excel folder:
echo      mkdir %%LOCALAPPDATA%%\vibe-local\excel
echo.
echo Running application...
echo.

python vibe_local_chat.py

pause
