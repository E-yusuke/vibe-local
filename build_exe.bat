@echo off
chcp 65001 >nul
REM PyInstaller build script for vibe-local
REM This script builds the standalone EXE application
REM
REM Prerequisites:
REM   - Python 3.8+ installed and in PATH
REM   - pip install pyinstaller
REM   - pip install -r requirements.txt
REM
REM Usage:
REM   build_exe.bat

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║    vibe-local EXE Build Script (Windows)                      ║
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
echo ✓ Found: !PYTHON_VER!
echo.

REM Check if PyInstaller is installed
pyinstaller --version >nul 2>&1
if !errorlevel! neq 0 (
    echo ⚠️  PyInstaller not found. Installing...
    pip install pyinstaller
    if !errorlevel! neq 0 (
        echo ❌ Failed to install PyInstaller
        pause
        exit /b 1
    )
)

echo ✓ PyInstaller is available
echo.

REM Install dependencies if needed
echo Checking dependencies...
pip install -q -r requirements.txt
if !errorlevel! neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✓ Dependencies installed
echo.

REM Clean previous builds
echo Cleaning previous builds...
if exist dist rmdir /s /q dist >nul 2>&1
if exist build rmdir /s /q build >nul 2>&1
if exist __pycache__ rmdir /s /q __pycache__ >nul 2>&1

echo ✓ Clean complete
echo.

REM Build EXE
echo Building EXE application...
echo This may take 1-2 minutes...
echo.

pyinstaller vibe_local.spec

if !errorlevel! neq 0 (
    echo ❌ Build failed
    pause
    exit /b 1
)

echo.
echo ✓ Build complete!
echo.

REM Show output location
set EXE_PATH=dist\vibe-local.exe
if exist !EXE_PATH! (
    echo ✓ EXE created: !EXE_PATH!
    echo.
    echo 📦 Distribution package:
    echo   Location: !CD!\dist\
    echo.
    echo 📋 Before distribution, create this folder structure:
    echo   vibe-local.exe
    echo   data\              (create this folder)
    echo   excel\             (create this folder)
    echo.
    echo 💾 Place these files alongside vibe-local.exe:
    echo   - SQLite databases in: data\
    echo   - Excel files in: excel\
    echo.
    echo 🚀 To run:
    echo   1. Create data\ and excel\ folders in the same directory as vibe-local.exe
    echo   2. Double-click vibe-local.exe to start
    echo   3. (or from command prompt) vibe-local.exe
    echo.
    echo 📝 User must set API credentials before running:
    echo   setx AZURE_OPENAI_API_KEY "your-key"
    echo   setx AZURE_OPENAI_ENDPOINT "https://..."
    echo.
) else (
    echo ❌ EXE not found at expected location
    pause
    exit /b 1
)

echo.
echo 🔧 Next steps:
echo   1. create_distribution.bat を実行して配布パッケージを作成
echo   2. または以下のコマンドで直接テスト実行:
echo      !EXE_PATH!
echo.
echo Done!
pause
endlocal
