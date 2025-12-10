@echo off
REM Activate Drawlingo conda environment and run the app
REM This script works even if conda init hasn't been run

echo Activating Drawlingo environment...

REM Find conda installation
set "CONDA_BASE=D:\Apps\MiniConda"

REM Activate conda environment using the batch file method
call "%CONDA_BASE%\Scripts\activate.bat" Drawlingo

if errorlevel 1 (
    echo ERROR: Failed to activate Drawlingo environment!
    echo Please make sure the environment exists: conda env list
    pause
    exit /b 1
)

echo Environment activated successfully!
echo.
echo Starting Drawlingo...
python main.py

pause




