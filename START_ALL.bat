@echo off
echo ===============================================
echo   RápidoLingo - Starting All Services
echo ===============================================
echo.

REM Kill existing processes
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul
timeout /t 2 >nul

echo [1/3] Starting Backend API...
cd backend
start "Backend API" cmd /k "python main.py"
timeout /t 3 >nul

echo [2/3] Starting LiveKit Agent Worker...
start "LiveKit Agent" cmd /k "python working_agent.py dev"
timeout /t 3 >nul

echo [3/3] Starting Frontend...
cd ..\frontend
start "Frontend Dev Server" cmd /k "npm run dev"

echo.
echo ===============================================
echo   All services starting!
echo ===============================================
echo.
echo   Backend API:     http://localhost:8000
echo   Frontend:        http://localhost:3000
echo   Agent Worker:    Running in background
echo.
echo   Check the opened windows for logs
echo ===============================================
pause

