"""
Check MCP Setup Script

This script verifies the MCP setup for Unreal Engine integration with Cursor and Claude Desktop.
It checks for necessary components and configurations and provides diagnostic information.
"""

import os
import sys
import json
import importlib
import platform
import subprocess

def check_mark():
    """Return a green check mark for success."""
    return "\033[92m✓\033[0m" if os.name != 'nt' else "\033[92mOK\033[0m"

def x_mark():
    """Return a red X mark for failure."""
    return "\033[91m✗\033[0m" if os.name != 'nt' else "\033[91mFAIL\033[0m"

def info_mark():
    """Return a blue info mark."""
    return "\033[94mi\033[0m" if os.name != 'nt' else "\033[94mINFO\033[0m"

def print_status(message, success=None):
    """Print a status message with appropriate formatting."""
    if success is None:
        print(f" {info_mark()} {message}")
    elif success:
        print(f" {check_mark()} {message}")
    else:
        print(f" {x_mark()} {message}")

def check_python():
    """Check Python installation."""
    print("\n=== Python Environment ===")
    print_status(f"Python version: {platform.python_version()}", True)
    
    # Check virtualenv
    try:
        import virtualenv
        print_status(f"virtualenv is installed (version: {virtualenv.__version__})", True)
    except ImportError:
        print_status("virtualenv is not installed", False)
    
    # Check MCP package
    try:
        import mcp
        version = getattr(mcp, "__version__", "unknown")
        print_status(f"MCP package is installed (version: {version})", True)
    except ImportError:
        print_status("MCP package is not installed", False)
    
    # Check if python_env exists
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_dir = os.path.join(script_dir, "python_env")
    if os.path.exists(env_dir):
        print_status(f"Python virtual environment exists at: {env_dir}", True)
    else:
        print_status(f"Python virtual environment not found at: {env_dir}", False)
    
    # Check if run_unreal_mcp.bat exists
    run_script = os.path.join(script_dir, "run_unreal_mcp.bat")
    if os.path.exists(run_script):
        print_status(f"Run script exists at: {run_script}", True)
    else:
        print_status(f"Run script not found at: {run_script}", False)

def check_claude_setup():
    """Check Claude Desktop setup."""
    print("\n=== Claude Desktop Setup ===")
    
    # Check if Claude Desktop is installed
    claude_installed = False
    if os.name == 'nt':  # Windows
        claude_paths = [
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'Claude Desktop', 'Claude Desktop.exe'),
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'Claude Desktop', 'Claude Desktop.exe'),
            os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Claude Desktop', 'Claude Desktop.exe')
        ]
        for path in claude_paths:
            if os.path.exists(path):
                print_status(f"Claude Desktop is installed at: {path}", True)
                claude_installed = True
                break
    elif os.name == 'darwin':  # macOS
        claude_paths = [
            '/Applications/Claude Desktop.app',
            os.path.expanduser('~/Applications/Claude Desktop.app')
        ]
        for path in claude_paths:
            if os.path.exists(path):
                print_status(f"Claude Desktop is installed at: {path}", True)
                claude_installed = True
                break
    
    if not claude_installed:
        print_status("Claude Desktop installation not found", False)
    
    # Check Claude config
    config_file = None
    if os.name == 'nt':  # Windows
        config_file = os.path.join(os.environ.get('APPDATA', ''), 'Claude', 'claude_desktop_config.json')
    elif os.name == 'darwin':  # macOS
        config_file = os.path.expanduser('~/Library/Application Support/Claude/claude_desktop_config.json')
    
    if config_file and os.path.exists(config_file):
        print_status(f"Claude Desktop configuration file exists at: {config_file}", True)
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            if 'mcpServers' in config and 'unreal' in config['mcpServers']:
                cmd = config['mcpServers']['unreal'].get('command', '')
                print_status(f"Unreal MCP configuration found with command: {cmd}", True)
                if not os.path.exists(cmd):
                    print_status(f"Warning: The configured command path does not exist: {cmd}", False)
            else:
                print_status("Unreal MCP configuration not found in Claude Desktop config", False)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print_status(f"Error reading Claude Desktop config: {str(e)}", False)
    else:
        print_status(f"Claude Desktop configuration file not found at: {config_file}", False)
    
    # Check Claude logs
    log_file = None
    if os.name == 'nt':  # Windows
        log_file = os.path.join(os.environ.get('APPDATA', ''), 'Claude', 'logs', 'mcp-server-unreal.log')
    elif os.name == 'darwin':  # macOS
        log_file = os.path.expanduser('~/Library/Application Support/Claude/logs/mcp-server-unreal.log')
    
    if log_file and os.path.exists(log_file):
        print_status(f"Claude Desktop MCP log file exists at: {log_file}", True)
        # Optionally show last few lines of log
        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()
                if lines:
                    print("\n   Last log entry:")
                    print(f"   {lines[-1].strip()}")
        except Exception:
            pass
    else:
        print_status(f"Claude Desktop MCP log file not found at: {log_file}", None)
        print_status("This is normal if you haven't run the MCP server with Claude Desktop yet", None)

def check_cursor_setup():
    """Check Cursor setup."""
    print("\n=== Cursor Setup ===")
    
    # Check if Cursor is installed
    cursor_installed = False
    if os.name == 'nt':  # Windows
        cursor_paths = [
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'Cursor', 'Cursor.exe'),
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'Cursor', 'Cursor.exe'),
            os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Cursor', 'Cursor.exe')
        ]
        for path in cursor_paths:
            if os.path.exists(path):
                print_status(f"Cursor is installed at: {path}", True)
                cursor_installed = True
                break
    elif os.name == 'darwin':  # macOS
        cursor_paths = [
            '/Applications/Cursor.app',
            os.path.expanduser('~/Applications/Cursor.app')
        ]
        for path in cursor_paths:
            if os.path.exists(path):
                print_status(f"Cursor is installed at: {path}", True)
                cursor_installed = True
                break
    elif os.name == 'posix':  # Linux
        cursor_paths = [
            '/usr/bin/cursor',
            '/usr/local/bin/cursor',
            os.path.expanduser('~/.local/bin/cursor')
        ]
        for path in cursor_paths:
            if os.path.exists(path):
                print_status(f"Cursor is installed at: {path}", True)
                cursor_installed = True
                break
    
    if not cursor_installed:
        print_status("Cursor installation not found", False)
    
    # Check Cursor config
    config_file = None
    if os.name == 'nt':  # Windows
        config_file = os.path.join(os.environ.get('APPDATA', ''), 'Cursor', 'User', 'settings.json')
    elif os.name == 'darwin':  # macOS
        config_file = os.path.expanduser('~/Library/Application Support/Cursor/User/settings.json')
    elif os.name == 'posix':  # Linux
        config_file = os.path.expanduser('~/.config/Cursor/User/settings.json')
    
    if config_file and os.path.exists(config_file):
        print_status(f"Cursor configuration file exists at: {config_file}", True)
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            mcp_enabled = config.get('mcp', {}).get('enabled', False)
            print_status(f"MCP enabled in Cursor config: {mcp_enabled}", mcp_enabled)
            
            servers = config.get('mcp', {}).get('servers', {})
            if 'unreal' in servers:
                cmd = servers['unreal'].get('command', '')
                print_status(f"Unreal MCP configuration found with command: {cmd}", True)
                if not os.path.exists(cmd):
                    print_status(f"Warning: The configured command path does not exist: {cmd}", False)
            else:
                print_status("Unreal MCP configuration not found in Cursor config", False)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print_status(f"Error reading Cursor config: {str(e)}", False)
    else:
        print_status(f"Cursor configuration file not found at: {config_file}", False)

def check_unreal_plugin():
    """Check Unreal Engine plugin setup."""
    print("\n=== Unreal Engine Plugin ===")
    
    # Get plugin directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    plugin_dir = os.path.abspath(os.path.join(script_dir, ".."))
    
    # Check for plugin file
    plugin_file = os.path.join(plugin_dir, "UnrealMCP.uplugin")
    if os.path.exists(plugin_file):
        print_status(f"UnrealMCP plugin file exists at: {plugin_file}", True)
    else:
        print_status(f"UnrealMCP plugin file not found at: {plugin_file}", False)
    
    # Check for Source directory
    source_dir = os.path.join(plugin_dir, "Source")
    if os.path.exists(source_dir) and os.path.isdir(source_dir):
        print_status(f"Plugin Source directory exists at: {source_dir}", True)
    else:
        print_status(f"Plugin Source directory not found at: {source_dir}", False)
    
    # Check if the plugin can be loaded by Unreal
    print_status("Note: To check if the plugin is loaded in Unreal Engine:", None)
    print_status("1. Open your Unreal project", None)
    print_status("2. Go to Edit > Plugins", None)
    print_status("3. Search for 'UnrealMCP' and ensure it's enabled", None)

def main():
    """Main function."""
    print("\n========================================================")
    print("           Unreal MCP Setup Diagnosis Tool              ")
    print("========================================================")
    
    check_python()
    check_claude_setup()
    check_cursor_setup()
    check_unreal_plugin()
    
    print("\n========================================================")
    print("                    Diagnosis Complete                  ")
    print("========================================================")
    print("\nIf you encountered any issues, please try running:")
    print("1. setup_unreal_mcp.bat - To set up the Python environment")
    print("2. setup_cursor_mcp.bat - For Cursor integration")
    print("\nFor more help, see the README.md or open an issue on GitHub.")

if __name__ == "__main__":
    main() 