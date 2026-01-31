@echo off
echo ========================================
echo Starting Insight Flow Bridge (Standalone Mode)
echo Port: 8006
echo ========================================
echo.
echo This runs the bridge WITHOUT requiring the full backend.
echo For full features, use start_insight_flow_fixed.bat first.
echo.
cd /d "c:\Users\Ashmit Pandey\Desktop\Core-Bucket_KarmaIntegratedPart-main\Insight_Flow-main"
python insight_flow_bridge_standalone.py
