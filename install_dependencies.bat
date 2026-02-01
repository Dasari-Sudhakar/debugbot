@echo off
echo ========================================
echo   DebugBot - Dependency Installer
echo ========================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python first:
    echo 1. Go to: https://www.python.org/downloads/
    echo 2. Download Python 3.10 or higher
    echo 3. During installation, CHECK "Add Python to PATH"
    echo 4. Run this script again after installation
    echo.
    pause
    exit /b 1
)

python --version
echo [OK] Python found
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install Flask
echo ========================================
echo Installing Flask...
echo ========================================
pip install flask
if errorlevel 1 (
    echo [ERROR] Failed to install Flask
    pause
    exit /b 1
)
echo [OK] Flask installed
echo.

REM Install flask-cors
echo ========================================
echo Installing flask-cors...
echo ========================================
pip install flask-cors
if errorlevel 1 (
    echo [ERROR] Failed to install flask-cors
    pause
    exit /b 1
)
echo [OK] flask-cors installed
echo.

REM Install requests
echo ========================================
echo Installing requests...
echo ========================================
pip install requests
if errorlevel 1 (
    echo [ERROR] Failed to install requests
    pause
    exit /b 1
)
echo [OK] requests installed
echo.

REM Verify installations
echo ========================================
echo Verifying installations...
echo ========================================

python -c "import flask; print('Flask version:', flask.__version__)"
python -c "import flask_cors; print('Flask-CORS: OK')"
python -c "import requests; print('Requests version:', requests.__version__)"

echo.
echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo All Python dependencies are installed.
echo.
echo Next steps:
echo 1. Install Ollama from: https://ollama.com/download/windows
echo 2. Run: ollama pull codellama
echo 3. Run: start_debugbot.bat
echo.
pause