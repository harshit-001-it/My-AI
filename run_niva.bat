@echo off
title NIVA_OS | UNIFIED_LAUNCH_PROTOCOL
echo.
echo ─────────────────────────────────────────────────────────────
echo   INITIALISING NIVA_OS CORE [GRID_SYNC_ACTIVE]
echo ─────────────────────────────────────────────────────────────
echo.

:: Check the current Python environment
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found in system path. Please install Python 3.11+.
    pause
    exit /b
)

:: Install core dependencies silently if missing
echo [#] ANALYZING LOGIC NODES...
python -m pip install -r requirements.txt --quiet

:: Start the NIVA controller
echo [#] DEPLOYING OBSIDIAN_KINETIC_HUD...
python main.py

echo.
echo [!] NIVA SESSION TERMINATED. PROTECTING MASTER'S DATA.
pause
