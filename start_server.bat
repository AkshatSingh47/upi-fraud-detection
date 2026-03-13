@echo off
echo ========================================
echo UPI Fraud Detection - Starting Servers
echo ========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo [1/6] Setting up Python virtual environment...
if not exist "backend\venv" (
    echo Creating virtual environment...
    cd backend
    python -m venv venv
    cd ..
)

echo.
echo [2/6] Installing backend dependencies...
cd backend
call venv\Scripts\activate.bat
pip install -r requirements.txt
cd ..

echo.
echo [3/6] Training ML model...
cd ml
call ..\backend\venv\Scripts\activate.bat
python retrain_model.py
cd ..

echo.
echo [4/6] Installing frontend dependencies...
cd frontend
if not exist "node_modules" (
    npm install
)
cd ..

echo.
echo [5/6] Starting Backend Server (Port 8000)...
start "UPI Fraud Detection - Backend" cmd /k "cd backend && venv\Scripts\activate.bat && python run.py"

timeout /t 3 /nobreak >nul

echo.
echo [6/6] Starting Frontend Server (Port 3000)...
start "UPI Fraud Detection - Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo ✓ Servers are starting!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit this window...
echo (The servers will continue running)
pause >nul

