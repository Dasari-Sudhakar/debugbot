@echo off
echo ========================================
echo    DebugBot - Starting Backend
echo ========================================
cd F:\Event\Hackthorn\BOT\python app.py
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [OK] Python found

REM Check if Ollama is running
echo [INFO] Checking Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Ollama is not responding
    echo Please make sure Ollama is running (check system tray)
    echo Starting Ollama...
    start ollama serve
    timeout /t 5 /nobreak >nul
)

echo [OK] Ollama is running

REM Navigate to DebugBot directory
cd /d "%~dp0"

REM Check if required files exist
if not exist "app.py" (
    echo [ERROR] app.py not found in current directory
    echo Please make sure app.py is in the same folder as this batch file
    pause
    exit /b 1
)

echo [OK] All files found
echo.

REM Start the Flask backend
echo ========================================
echo Starting DebugBot Backend...
echo Backend will run at: http://localhost:5000
echo Press Ctrl+C to stop
echo ========================================
echo.

python app.py

REM If Python exits
echo.
echo ========================================
echo DebugBot has stopped
echo ========================================
pause