@echo off
REM Quick start script for Windows
REM This script activates the conda environment first

echo Activating Drawlingo environment...

REM Try to activate using conda
call conda activate Drawlingo 2>nul
if errorlevel 1 (
    REM If conda activate fails, use direct path method
    set "CONDA_BASE=D:\Apps\MiniConda"
    call "%CONDA_BASE%\Scripts\activate.bat" Drawlingo
)

if errorlevel 1 (
    echo ERROR: Could not activate Drawlingo environment!
    echo Please run: activate_env.bat instead
    pause
    exit /b 1
)

echo Starting Drawlingo...
python main.py
pause

