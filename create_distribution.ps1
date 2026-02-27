# PowerShell script to create distribution package for vibe-local
# This script creates a ready-to-distribute folder with:
#   - vibe-local.exe
#   - data\ folder
#   - excel\ folder
#   - Documentation
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File create_distribution.ps1

# Set UTF-8 encoding for proper display
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗"
Write-Host "║   vibe-local Distribution Package Creator (PowerShell)        ║"
Write-Host "╚════════════════════════════════════════════════════════════════╝"
Write-Host ""

# Check if EXE exists
if (-not (Test-Path "dist\vibe-local.exe")) {
    Write-Host "❌ Error: vibe-local.exe not found in dist\ folder" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please run build_exe.ps1 first to build the EXE" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✓ Found vibe-local.exe" -ForegroundColor Green
Write-Host ""

# Create distribution folder
$distDir = "vibe-local-dist"
Write-Host "Creating distribution folder: $distDir"

if (Test-Path $distDir) {
    Write-Host "⚠️  Folder already exists. Removing old version..." -ForegroundColor Yellow
    Remove-Item -Path $distDir -Recurse -Force
}

New-Item -ItemType Directory -Path $distDir -Force | Out-Null
Write-Host "✓ Distribution folder created" -ForegroundColor Green
Write-Host ""

# Copy EXE
Write-Host "Copying EXE..."
Copy-Item -Path "dist\vibe-local.exe" -Destination "$distDir\vibe-local.exe"
Write-Host "✓ EXE copied" -ForegroundColor Green
Write-Host ""

# Create data folder
Write-Host "Creating data folder..."
$dataDir = "$distDir\data"
New-Item -ItemType Directory -Path $dataDir -Force | Out-Null
New-Item -ItemType File -Path "$dataDir\.gitkeep" -Force | Out-Null
Write-Host "✓ data folder created" -ForegroundColor Green
Write-Host ""

# Create excel folder
Write-Host "Creating excel folder..."
$excelDir = "$distDir\excel"
New-Item -ItemType Directory -Path $excelDir -Force | Out-Null
New-Item -ItemType File -Path "$excelDir\.gitkeep" -Force | Out-Null
Write-Host "✓ excel folder created" -ForegroundColor Green
Write-Host ""

# Copy documentation
Write-Host "Copying documentation..."
$docFiles = @(
    "README.md",
    "README_EXE.md",
    "VIBE_LOCAL_README.md",
    "SETUP_EXE.md",
    "DEFAULT_CONFIG_GUIDE.md"
)

foreach ($docFile in $docFiles) {
    if (Test-Path $docFile) {
        Copy-Item -Path $docFile -Destination "$distDir\$docFile"
        Write-Host "  ✓ Copied: $docFile" -ForegroundColor Green
    }
}

Write-Host ""

# Create setup helper script
Write-Host "Creating setup helper script..."
$setupScript = @"
@echo off
REM Setup script to help users configure API credentials
REM This script is provided for convenience

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   vibe-local API Credentials Setup Helper                     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Option 1: Azure OpenAI (uncomment to use)
REM setx AZURE_OPENAI_API_KEY "your-api-key-here"
REM setx AZURE_OPENAI_ENDPOINT "https://your-resource.openai.azure.com"
REM setx AZURE_OPENAI_DEPLOYMENT "gpt-4-turbo"
REM setx AZURE_OPENAI_API_VERSION "2024-08-01-preview"

REM Option 2: Google Gemini (uncomment to use)
REM setx GEMINI_API_KEY "your-api-key-here"
REM setx GEMINI_MODEL "gemini-2.0-flash"

echo Instructions:
echo 1. Open PowerShell as Administrator
echo 2. Run the following command (replace with your actual credentials):
echo.
echo    [Environment]::SetEnvironmentVariable("AZURE_OPENAI_API_KEY", "your-key", "User")
echo    [Environment]::SetEnvironmentVariable("AZURE_OPENAI_ENDPOINT", "https://your-resource.openai.azure.com", "User")
echo.
echo 3. Close and reopen PowerShell/CMD for changes to take effect
echo 4. Run vibe-local.exe
echo.
echo For more details, see: SETUP_EXE.md or DEFAULT_CONFIG_GUIDE.md
echo.
pause
"@

Set-Content -Path "$distDir\setup_credentials.bat" -Value $setupScript -Encoding ASCII
Write-Host "✓ setup_credentials.bat created" -ForegroundColor Green
Write-Host ""

# Show summary
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║   vibe-local Distribution Package Created Successfully!       ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "📦 Package location: $(Get-Location)\$distDir\" -ForegroundColor Cyan
Write-Host ""

Write-Host "📋 Folder structure:" -ForegroundColor Cyan
Write-Host "   $distDir\" -ForegroundColor Cyan
Write-Host "   ├── vibe-local.exe" -ForegroundColor Cyan
Write-Host "   ├── data\" -ForegroundColor Cyan
Write-Host "   ├── excel\" -ForegroundColor Cyan
Write-Host "   ├── README.md" -ForegroundColor Cyan
Write-Host "   ├── README_EXE.md" -ForegroundColor Cyan
Write-Host "   ├── VIBE_LOCAL_README.md" -ForegroundColor Cyan
Write-Host "   ├── SETUP_EXE.md" -ForegroundColor Cyan
Write-Host "   ├── DEFAULT_CONFIG_GUIDE.md" -ForegroundColor Cyan
Write-Host "   └── setup_credentials.bat" -ForegroundColor Cyan
Write-Host ""

Write-Host "✅ Ready to distribute!" -ForegroundColor Green
Write-Host ""

Write-Host "📝 Distribution steps:" -ForegroundColor Yellow
Write-Host "   1. ZIP the '$distDir\' folder" -ForegroundColor Yellow
Write-Host "   2. Send to users" -ForegroundColor Yellow
Write-Host "   3. Users extract and run vibe-local.exe" -ForegroundColor Yellow
Write-Host ""

Read-Host "Press Enter to exit"
