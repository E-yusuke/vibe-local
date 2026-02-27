@echo off
REM Quick launcher for vibe-local chat application
REM Place your API credentials in environment variables before running

setlocal

REM Check if required environment variable is set
if not defined AZURE_OPENAI_API_KEY (
    if not defined GEMINI_API_KEY (
        echo Error: No API credentials found
        echo.
        echo Please set one of these:
        echo   - AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT
        echo   - GEMINI_API_KEY
        echo.
        echo See README for setup instructions.
        pause
        exit /b 1
    )
)

REM Run the chat application
python "%~dp0vibe_local_chat.py" %*

endlocal
