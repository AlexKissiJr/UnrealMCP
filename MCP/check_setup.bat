@echo off
echo ========================================================
echo Unreal MCP - Setup Diagnosis Tool
echo ========================================================
echo.
echo This tool will check your MCP setup and provide diagnostic information.
echo.

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

REM Try to run with the virtual environment first
if exist "%SCRIPT_DIR%\python_env\Scripts\python.exe" (
    echo Using Python from virtual environment...
    call "%SCRIPT_DIR%\python_env\Scripts\activate.bat"
    python "%SCRIPT_DIR%\check_mcp_setup.py"
) else (
    echo Using system Python...
    python "%SCRIPT_DIR%\check_mcp_setup.py"
)

echo.
echo Press any key to exit...
pause >nul 