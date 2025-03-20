@echo off
setlocal EnableDelayedExpansion

echo ========================================================
echo Unreal MCP - Python Environment Setup
echo ========================================================
echo.

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

REM Set paths for local environment
set "ENV_DIR=%SCRIPT_DIR%\python_env"
set "MODULES_DIR=%SCRIPT_DIR%\python_modules"

REM Parse command line arguments
set "CONFIGURE_CLAUDE=0"
set "CONFIGURE_CURSOR=0"

:parse_args
if "%1"=="" goto :done_parsing
if /i "%1"=="--help" (
    echo Usage: setup_unreal_mcp.bat [OPTIONS]
    echo.
    echo Options:
    echo   --help                 Show this help message
    echo   --configure-claude     Configure Claude Desktop (default)
    echo   --configure-cursor     Configure Cursor
    echo   --configure-both       Configure both Claude and Cursor
    echo   --skip-config          Skip configuration
    echo.
    goto :end
)
if /i "%1"=="--configure-claude" set "CONFIGURE_CLAUDE=1" & set "CONFIGURE_CURSOR=0" & shift & goto :parse_args
if /i "%1"=="--configure-cursor" set "CONFIGURE_CLAUDE=0" & set "CONFIGURE_CURSOR=1" & shift & goto :parse_args
if /i "%1"=="--configure-both" set "CONFIGURE_CLAUDE=1" & set "CONFIGURE_CURSOR=1" & shift & goto :parse_args
if /i "%1"=="--skip-config" set "CONFIGURE_CLAUDE=0" & set "CONFIGURE_CURSOR=0" & shift & goto :parse_args
shift
goto :parse_args
:done_parsing

REM If no config option was specified, show the assistant choice menu first
if "%CONFIGURE_CLAUDE%"=="0" if "%CONFIGURE_CURSOR%"=="0" (
    echo Which AI assistant would you like to configure?
    echo.
    echo 1. Claude Desktop
    echo 2. Cursor
    echo 3. Both Claude Desktop and Cursor
    echo 4. Skip AI assistant configuration
    echo.
    
    set /p AI_CHOICE="Enter choice (1-4): "
    echo.
    
    if "!AI_CHOICE!"=="1" set "CONFIGURE_CLAUDE=1" & set "CONFIGURE_CURSOR=0"
    if "!AI_CHOICE!"=="2" set "CONFIGURE_CLAUDE=0" & set "CONFIGURE_CURSOR=1"
    if "!AI_CHOICE!"=="3" set "CONFIGURE_CLAUDE=1" & set "CONFIGURE_CURSOR=1"
    if "!AI_CHOICE!"=="4" set "CONFIGURE_CLAUDE=0" & set "CONFIGURE_CURSOR=0"
)

echo Setting up Python environment in: %ENV_DIR%
echo.

REM Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python is not installed or not in your PATH.
    echo Please install Python and try again.
    goto :end
)

REM Get Python version and path
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
for /f "tokens=*" %%i in ('where python') do set SYSTEM_PYTHON=%%i
echo Detected %PYTHON_VERSION% at %SYSTEM_PYTHON%
echo.

REM Create directories if they don't exist
if not exist "%ENV_DIR%" (
    echo Creating Python environment directory...
    mkdir "%ENV_DIR%"
)

if not exist "%MODULES_DIR%" (
    echo Creating Python modules directory...
    mkdir "%MODULES_DIR%"
)

REM Check if virtualenv is installed
python -c "import virtualenv" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Installing virtualenv...
    python -m pip install virtualenv
)

REM Create virtual environment if it doesn't exist
if not exist "%ENV_DIR%\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m virtualenv "%ENV_DIR%"
) else (
    echo Virtual environment already exists.
)

REM Activate the virtual environment and install packages
echo.
echo Activating virtual environment and installing packages...
call "%ENV_DIR%\Scripts\activate.bat"

REM Check if activation was successful
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to activate virtual environment.
    goto :end
)

REM Install MCP package in the virtual environment
echo Installing MCP package...
python -m pip install mcp>=0.1.0

REM Also install to modules directory as a backup
echo Installing MCP package to modules directory as backup...
python -m pip install mcp>=0.1.0 -t "%MODULES_DIR%"

REM Verify installation
echo.
echo Verifying MCP installation...
python -c "import mcp; print(f'MCP package installed successfully. Version: {getattr(mcp, \"__version__\", \"unknown\")}')"

REM Create the run script
echo.
echo Creating run script...
(
echo @echo off
echo setlocal
echo.
echo REM Get the directory where this script is located
echo set "SCRIPT_DIR=%%~dp0"
echo set "SCRIPT_DIR=%%SCRIPT_DIR:~0,-1%%"
echo.
echo REM Set paths for local environment
echo set "ENV_DIR=%%SCRIPT_DIR%%\python_env"
echo set "PYTHON_PATH=%%ENV_DIR%%\Scripts\python.exe"
echo.
echo REM Check if Python environment exists
echo if not exist "%%PYTHON_PATH%%" (
echo     echo ERROR: Python environment not found. Please run setup_unreal_mcp.bat first. ^>^&2
echo     goto :end
echo )
echo.
echo REM Activate the virtual environment silently
echo call "%%ENV_DIR%%\Scripts\activate.bat" ^>nul 2^>^&1
echo.
echo REM Log start message to stderr
echo echo Starting Unreal MCP bridge... ^>^&2
echo.
echo REM Run the Python bridge script
echo python "%%SCRIPT_DIR%%\unreal_mcp_bridge.py" %%*
echo.
echo :end
) > "%SCRIPT_DIR%\run_unreal_mcp.bat"

REM Configure Claude Desktop if requested
if "%CONFIGURE_CLAUDE%"=="1" (
    set "CLAUDE_CONFIG_DIR=%APPDATA%\Claude"
    set "CLAUDE_CONFIG_FILE=%CLAUDE_CONFIG_DIR%\claude_desktop_config.json"

    REM Check if Claude Desktop is installed
    if not exist "%CLAUDE_CONFIG_DIR%" (
        echo Creating Claude configuration directory...
        mkdir "%CLAUDE_CONFIG_DIR%"
    )

    REM Update Claude Desktop configuration using Python
    echo.
    echo Updating Claude Desktop configuration...
    python "%SCRIPT_DIR%\temp_update_config.py" "%CLAUDE_CONFIG_FILE%" "%SCRIPT_DIR%\run_unreal_mcp.bat"
    if %ERRORLEVEL% neq 0 (
        echo WARNING: Failed to update Claude Desktop configuration. Claude Desktop may not be installed.
    ) else (
        echo Claude Desktop configuration updated at: %CLAUDE_CONFIG_FILE%
    )
)

REM Configure Cursor if requested
if "%CONFIGURE_CURSOR%"=="1" (
    echo.
    echo Updating Cursor configuration...
    python "%SCRIPT_DIR%\cursor_setup.py" --script "%SCRIPT_DIR%\run_unreal_mcp.bat"
    if %ERRORLEVEL% neq 0 (
        echo WARNING: Failed to update Cursor configuration. Cursor may not be installed.
    ) else (
        echo Cursor configuration updated successfully!
    )
)

echo.
echo ========================================================
echo Setup complete!
echo.

if "%CONFIGURE_CLAUDE%"=="1" if "%CONFIGURE_CURSOR%"=="0" (
    echo To use with Claude Desktop:
    echo 1. Run run_unreal_mcp.bat to start the MCP bridge
    echo 2. Open Claude Desktop and it should automatically use the correct configuration
) else if "%CONFIGURE_CLAUDE%"=="0" if "%CONFIGURE_CURSOR%"=="1" (
    echo To use with Cursor:
    echo 1. Run run_unreal_mcp.bat to start the MCP bridge
    echo 2. Open Cursor and it should automatically use the UnrealMCP tools
) else if "%CONFIGURE_CLAUDE%"=="1" if "%CONFIGURE_CURSOR%"=="1" (
    echo To use with Claude Desktop:
    echo 1. Run run_unreal_mcp.bat to start the MCP bridge
    echo 2. Open Claude Desktop and it should automatically use the correct configuration
    echo.
    echo To use with Cursor:
    echo 1. Run run_unreal_mcp.bat to start the MCP bridge
    echo 2. Open Cursor and it should automatically use the UnrealMCP tools
) else (
    echo No AI assistant configurations were applied.
    echo To configure an assistant, run this script again with one of these options:
    echo   --configure-claude     Configure Claude Desktop
    echo   --configure-cursor     Configure Cursor
    echo   --configure-both       Configure both Claude and Cursor
)

echo ========================================================
echo.
echo Press any key to exit...
pause >nul

:end