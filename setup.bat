@echo off
REM Quick Start Script for Smart Complaint Routing System (Windows)

echo.
echo ==========================================
echo Smart Complaint Routing System
echo Quick Start Setup (Windows)
echo ==========================================
echo.

REM Check Python
echo [INFO] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Please install Python 3.8+
    pause
    exit /b 1
)
python --version

REM Check Node
echo [INFO] Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo Node.js not found. Please install Node.js 16+
    pause
    exit /b 1
)
node --version
npm --version

REM Backend Setup
echo.
echo [INFO] Setting up Backend...
cd backend

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Copy .env
if not exist ".env" (
    copy .env.example .env
    echo [SUCCESS] Created .env file
)

REM Initialize database
echo Initializing database...
python init_db.py

echo [SUCCESS] Backend setup complete!
echo.

REM Frontend Setup
echo [INFO] Setting up Frontend...
cd ..\frontend

REM Install npm dependencies
if not exist "node_modules" (
    echo Installing npm dependencies...
    call npm install
)

echo [SUCCESS] Frontend setup complete!
echo.

REM Final instructions
echo ==========================================
echo [SUCCESS] Setup Complete!
echo ==========================================
echo.
echo To run the system:
echo.
echo Terminal 1 - Backend:
echo   cd backend
echo   venv\Scripts\activate
echo   uvicorn app.main:app --reload
echo.
echo Terminal 2 - Frontend:
echo   cd frontend
echo   npm run dev
echo.
echo Then open: http://localhost:5173
echo.
echo Test Accounts:
echo   Student: test@karunya.edu.in (register new)
echo   Faculty: cse@karunya.edu / admin123
echo.

pause
