@echo off
echo ========================================
echo   DebugBot - System Diagnostics
echo ========================================
echo.

set ERRORS=0

REM Check Python
echo [1/7] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Python not found
    echo        Install from: https://www.python.org/downloads/
    set /a ERRORS+=1
) else (
    python --version
    echo [PASS] Python installed
)
echo.

REM Check pip
echo [2/7] Checking pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] pip not found
    set /a ERRORS+=1
) else (
    echo [PASS] pip available
)
echo.

REM Check Flask
echo [3/7] Checking Flask installation...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo [FAIL] Flask not installed
    echo        Run: pip install flask flask-cors requests
    set /a ERRORS+=1
) else (
    echo [PASS] Flask installed
)
echo.

REM Check flask-cors
echo [4/7] Checking flask-cors...
python -c "import flask_cors" 2>nul
if errorlevel 1 (
    echo [FAIL] flask-cors not installed
    echo        Run: pip install flask-cors
    set /a ERRORS+=1
) else (
    echo [PASS] flask-cors installed
)
echo.

REM Check requests
echo [5/7] Checking requests library...
python -c "import requests" 2>nul
if errorlevel 1 (
    echo [FAIL] requests not installed
    echo        Run: pip install requests
    set /a ERRORS+=1
) else (
    echo [PASS] requests installed
)
echo.

REM Check Ollama
echo [6/7] Checking Ollama...
where ollama >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Ollama not found
    echo        Install from: https://ollama.com/download/windows
    set /a ERRORS+=1
) else (
    echo [PASS] Ollama installed
    
    REM Check if Ollama is running
    curl -s http://localhost:11434/api/tags >nul 2>&1
    if errorlevel 1 (
        echo [WARN] Ollama not running - Start Ollama from Start Menu
    ) else (
        echo [PASS] Ollama is running
    )
)
echo.

REM Check CodeLlama model
echo [7/7] Checking CodeLlama model...
ollama list | findstr "codellama" >nul 2>&1
if errorlevel 1 (
    echo [FAIL] CodeLlama model not found
    echo        Run: ollama pull codellama
    set /a ERRORS+=1
) else (
    echo [PASS] CodeLlama model available
)
echo.

REM Check required files
echo [EXTRA] Checking DebugBot files...
if exist "app.py" (
    echo [PASS] app.py found
) else (
    echo [FAIL] app.py not found
    set /a ERRORS+=1
)

if exist "index.html" (
    echo [PASS] index.html found
) else (
    echo [WARN] index.html not found
)

if exist "admin.html" (
    echo [PASS] admin.html found
) else (
    echo [WARN] admin.html not found
)
echo.

REM Summary
echo ========================================
echo           DIAGNOSTIC SUMMARY
echo ========================================
if %ERRORS% EQU 0 (
    echo Status: [READY] All systems operational!
    echo You can run start_debugbot.bat now
) else (
    echo Status: [NOT READY] Found %ERRORS% error(s)
    echo Please fix the issues above before running DebugBot
)
echo ========================================
echo.

pause