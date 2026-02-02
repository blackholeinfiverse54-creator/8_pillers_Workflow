@echo off
echo ========================================
echo Starting 9-Pillar System
echo ========================================
echo.

echo [1/11] Starting Karma (8000)...
start "Karma" cmd /k "cd karma_chain_v2-main && python main.py"
timeout /t 5 /nobreak >nul

echo [2/11] Starting Bucket (8001)...
start "Bucket" cmd /k "cd BHIV_Central_Depository-main && python main.py"
timeout /t 5 /nobreak >nul

echo [3/11] Starting Core (8002)...
start "Core" cmd /k "cd v1-BHIV_CORE-main && python mcp_bridge.py"
timeout /t 5 /nobreak >nul

echo [4/11] Starting Workflow Executor (8003)...
start "Workflow Executor" cmd /k "cd workflow-executor-main && python main.py"
timeout /t 5 /nobreak >nul

echo [5/11] Starting UAO (8004)...
start "UAO" cmd /k "cd Unified Action Orchestration && python action_orchestrator.py"
timeout /t 5 /nobreak >nul

echo [6/11] Starting Insight Core (8005)...
start "Insight Core" cmd /k "cd insightcore-bridgev4x-main && python insight_service.py"
timeout /t 5 /nobreak >nul

echo [7/11] Starting Insight Flow Bridge (8006)...
start "Insight Flow" cmd /k "cd Insight_Flow-main && start_bridge_standalone.bat"
timeout /t 5 /nobreak >nul

echo [8/11] Starting Workflow Bridge (8008)...
start "Workflow Bridge" cmd /k "cd workflow-blackhole-main\bridge && python workflow_bridge.py"
timeout /t 5 /nobreak >nul

echo [9/11] Starting Workflow Backend (5001)...
start "Workflow Backend" cmd /k "cd workflow-blackhole-main\server && npm start"
timeout /t 10 /nobreak >nul

echo [10/11] Starting Workflow Frontend (5173)...
start "Workflow Frontend" cmd /k "cd workflow-blackhole-main\client && npm run dev"
timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo All services started!
echo ========================================
echo.
echo Services:
echo   Karma:              http://localhost:8000
echo   Bucket:             http://localhost:8001
echo   Core:               http://localhost:8002
echo   Workflow Executor:  http://localhost:8003
echo   UAO:                http://localhost:8004
echo   Insight Core:       http://localhost:8005
echo   Insight Flow:       http://localhost:8006
echo   Workflow Bridge:    http://localhost:8008
echo   Workflow Backend:   http://localhost:5001
echo   Workflow Frontend:  http://localhost:5173
echo.
echo Press any key to exit...
pause >nul
