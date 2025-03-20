@echo off
echo ========================================================
echo Unreal MCP - Cursor Setup
echo ========================================================
echo.
echo This script will set up the MCP bridge for Cursor.
echo.

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

REM Run the main setup script with the cursor configuration flag
call "%SCRIPT_DIR%\setup_unreal_mcp.bat" --configure-cursor

echo.
echo Setup complete! You can now use UnrealMCP with Cursor.
echo. 