# PowerShell script to build vibe-local EXE
# This script builds the standalone EXE application
#
# Prerequisites:
#   - Python 3.8+ installed and in PATH
#   - pip install pyinstaller
#   - pip install -r requirements.txt
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File build_exe.ps1

# Set UTF-8 encoding for proper display
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗"
Write-Host "║    vibe-local EXE Build Script (PowerShell)                   ║"
Write-Host "╚════════════════════════════════════════════════════════════════╝"
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..."
$pythonCheck = & python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python from https://www.python.org/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✓ Found: $pythonCheck" -ForegroundColor Green
Write-Host ""

# Check if PyInstaller is installed
Write-Host "Checking PyInstaller..."
$pyinstallerCheck = & pyinstaller --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  PyInstaller not found. Installing..." -ForegroundColor Yellow
    & pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install PyInstaller" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    $pyinstallerCheck = & pyinstaller --version 2>&1
}

Write-Host "✓ PyInstaller is available: $pyinstallerCheck" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "Checking dependencies..."
& pip install -q -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✓ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Clean previous builds
Write-Host "Cleaning previous builds..."
if (Test-Path "dist") {
    Remove-Item -Path "dist" -Recurse -Force -ErrorAction SilentlyContinue
}
if (Test-Path "build") {
    Remove-Item -Path "build" -Recurse -Force -ErrorAction SilentlyContinue
}
if (Test-Path "__pycache__") {
    Remove-Item -Path "__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host "✓ Clean complete" -ForegroundColor Green
Write-Host ""

# Build EXE
Write-Host "Building EXE application..."
Write-Host "This may take 1-2 minutes..."
Write-Host ""

& pyinstaller vibe_local.spec

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "✓ Build complete!" -ForegroundColor Green
Write-Host ""

# Show output location
$exePath = "dist\vibe-local.exe"
if (Test-Path $exePath) {
    Write-Host "✓ EXE created: $exePath" -ForegroundColor Green
    Write-Host ""
    Write-Host "📦 Distribution package:" -ForegroundColor Cyan
    Write-Host "   Location: $(Get-Location)\dist\" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📋 Before distribution, create this folder structure:" -ForegroundColor Cyan
    Write-Host "   vibe-local.exe" -ForegroundColor Cyan
    Write-Host "   data\              (create this folder)" -ForegroundColor Cyan
    Write-Host "   excel\             (create this folder)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "💾 Place these files alongside vibe-local.exe:" -ForegroundColor Cyan
    Write-Host "   - SQLite databases in: data\" -ForegroundColor Cyan
    Write-Host "   - Excel files in: excel\" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🚀 To run:" -ForegroundColor Cyan
    Write-Host "   1. Create data\ and excel\ folders in the same directory as vibe-local.exe" -ForegroundColor Cyan
    Write-Host "   2. Double-click vibe-local.exe to start" -ForegroundColor Cyan
    Write-Host "   3. (or from command prompt) vibe-local.exe" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📝 User must set API credentials before running:" -ForegroundColor Cyan
    Write-Host "   setx AZURE_OPENAI_API_KEY 'your-key'" -ForegroundColor Cyan
    Write-Host "   setx AZURE_OPENAI_ENDPOINT 'https://...'" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "❌ EXE not found at expected location" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "🔧 Next steps:" -ForegroundColor Yellow
Write-Host "   1. create_distribution.ps1 を実行して配布パッケージを作成" -ForegroundColor Yellow
Write-Host "   2. または以下のコマンドで直接テスト実行:" -ForegroundColor Yellow
Write-Host "      $exePath" -ForegroundColor Yellow
Write-Host ""
Write-Host "Done!" -ForegroundColor Green
Read-Host "Press Enter to exit"
