@echo off
REM Create distribution package for vibe-local EXE
REM This script creates a ready-to-distribute folder with:
REM   - vibe-local.exe
REM   - data\ folder
REM   - excel\ folder
REM   - Documentation

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   vibe-local Distribution Package Creator                     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if EXE exists
if not exist "dist\vibe-local.exe" (
    echo ❌ Error: vibe-local.exe not found in dist\ folder
    echo.
    echo Please run build_exe.bat first to create the EXE
    pause
    exit /b 1
)

echo ✓ Found dist\vibe-local.exe
echo.

REM Create distribution folder
set DIST_FOLDER=vibe-local-dist
if exist %DIST_FOLDER% (
    echo Removing existing distribution folder...
    rmdir /s /q %DIST_FOLDER%
)

echo Creating distribution folder structure...
mkdir %DIST_FOLDER%
mkdir %DIST_FOLDER%\data
mkdir %DIST_FOLDER%\excel

if !errorlevel! neq 0 (
    echo ❌ Failed to create folder structure
    pause
    exit /b 1
)

echo ✓ Folder structure created
echo.

REM Copy EXE
echo Copying vibe-local.exe...
copy /Y dist\vibe-local.exe %DIST_FOLDER%\ >nul
if !errorlevel! neq 0 (
    echo ❌ Failed to copy EXE
    pause
    exit /b 1
)

echo ✓ EXE copied
echo.

REM Copy documentation
echo Copying documentation...
if exist README.md copy /Y README.md %DIST_FOLDER%\ >nul
if exist VIBE_LOCAL_README.md copy /Y VIBE_LOCAL_README.md %DIST_FOLDER%\ >nul
if exist SETUP_EXE.md copy /Y SETUP_EXE.md %DIST_FOLDER%\ >nul
if exist LICENSE copy /Y LICENSE %DIST_FOLDER%\ >nul

echo ✓ Documentation copied
echo.

REM Create marker files in data and excel folders
echo Creating folder markers...
echo. > %DIST_FOLDER%\data\.gitkeep
echo. > %DIST_FOLDER%\excel\.gitkeep

REM Create a sample setup batch file
echo Creating setup helper scripts...
(
    echo @echo off
    echo REM Quick setup for vibe-local
    echo REM Set your Azure OpenAI or Gemini API credentials here
    echo.
    echo REM Option 1: Azure OpenAI (recommended^)
    echo REM setx AZURE_OPENAI_API_KEY "your-api-key-here"
    echo REM setx AZURE_OPENAI_ENDPOINT "https://your-resource.openai.azure.com"
    echo REM setx AZURE_OPENAI_DEPLOYMENT "gpt-4-turbo"
    echo REM setx AZURE_OPENAI_API_VERSION "2024-08-01-preview"
    echo.
    echo REM Option 2: Google Gemini
    echo REM setx GEMINI_API_KEY "your-api-key-here"
    echo.
    echo REM After setting credentials, open a new CMD and run:
    echo REM   vibe-local.exe
    echo.
    echo pause
) > %DIST_FOLDER%\setup_credentials.bat

echo ✓ Setup scripts created
echo.

REM Display summary
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   Distribution Package Created Successfully!                  ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo 📦 Package location: %CD%\%DIST_FOLDER%\
echo.

echo 📋 Folder structure:
echo   %DIST_FOLDER%\
echo   ├── vibe-local.exe          (main application)
echo   ├── data\                   (SQLite files go here)
echo   ├── excel\                  (Excel files go here)
echo   ├── README.md
echo   ├── VIBE_LOCAL_README.md
echo   ├── SETUP_EXE.md
echo   └── setup_credentials.bat   (helper script)
echo.

echo 🚀 Next steps for distribution:
echo   1. Copy vibe-local-dist\ folder to your distribution media
echo   2. Users should:
echo      a. Extract vibe-local-dist\ folder
echo      b. Run setup_credentials.bat to set API keys
echo      c. Double-click vibe-local.exe to start
echo      d. Place SQLite files in data\ folder
echo      e. Place Excel files in excel\ folder
echo.

echo 💾 To add sample data:
echo   1. Copy sample SQLite database to: %DIST_FOLDER%\data\
echo   2. Copy sample Excel file to: %DIST_FOLDER%\excel\
echo   3. Update README with file descriptions
echo.

echo ✓ Distribution package ready!
echo.

pause
