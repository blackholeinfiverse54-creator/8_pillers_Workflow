@echo off
echo Starting Workflow Blackhole Bridge (Port 8008)...
cd /d "%~dp0"
python workflow_bridge.py
pause
