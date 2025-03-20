"""
Script to configure Cursor MCP integration.

This script will update or create the necessary configuration for Cursor
to use the Unreal MCP bridge.
"""

import json
import os
import sys
import shutil
import argparse
from pathlib import Path

def get_cursor_config_dir():
    """Get the Cursor configuration directory based on OS."""
    if os.name == 'nt':  # Windows
        appdata = os.environ.get('APPDATA', '')
        return os.path.join(appdata, 'Cursor', 'User')
    elif os.name == 'darwin':  # macOS
        return os.path.expanduser('~/Library/Application Support/Cursor/User')
    else:  # Linux
        return os.path.expanduser('~/.config/Cursor/User')

def check_cursor_installed():
    """Check if Cursor is installed by looking for common installation paths."""
    cursor_paths = []
    
    if os.name == 'nt':  # Windows
        cursor_paths = [
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'Cursor', 'Cursor.exe'),
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'Cursor', 'Cursor.exe'),
            os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Cursor', 'Cursor.exe')
        ]
    elif os.name == 'darwin':  # macOS
        cursor_paths = [
            '/Applications/Cursor.app',
            os.path.expanduser('~/Applications/Cursor.app')
        ]
    else:  # Linux
        cursor_paths = [
            '/usr/bin/cursor',
            '/usr/local/bin/cursor',
            os.path.expanduser('~/.local/bin/cursor')
        ]
    
    # Check if any of the paths exist
    for path in cursor_paths:
        if os.path.exists(path):
            return True
            
    # Check if config directory exists as a fallback
    return os.path.exists(get_cursor_config_dir())

def configure_cursor_mcp(run_script_path):
    """Configure Cursor to use the Unreal MCP bridge."""
    # First check if Cursor is installed
    if not check_cursor_installed():
        print(f"Cursor doesn't appear to be installed on this system.")
        print("You can download Cursor from: https://cursor.sh/")
        print("After installing Cursor, run this script again.")
        return False
    
    cursor_config_dir = get_cursor_config_dir()
    
    if not os.path.exists(cursor_config_dir):
        try:
            print(f"Creating Cursor configuration directory: {cursor_config_dir}")
            os.makedirs(cursor_config_dir, exist_ok=True)
        except Exception as e:
            print(f"Error creating Cursor configuration directory: {str(e)}")
            return False
    
    # Create settings.json path
    settings_path = os.path.join(cursor_config_dir, 'settings.json')
    
    # Load existing settings or create new ones
    settings = {}
    if os.path.exists(settings_path):
        try:
            with open(settings_path, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            print(f"Could not read existing settings file, creating new one.")
    
    # Ensure the settings structure exists
    settings.setdefault('mcp', {})
    
    # Add UnrealMCP to the MCP servers list
    settings['mcp'].setdefault('servers', {})
    
    # Configure the Unreal MCP server
    settings['mcp']['servers']['unreal'] = {
        'command': run_script_path,
        'args': []
    }
    
    # Enable MCP in Cursor
    settings['mcp']['enabled'] = True
    
    # Save the updated settings file
    try:
        # Create backup of the original file if it exists
        if os.path.exists(settings_path):
            backup_path = settings_path + '.bak'
            shutil.copy2(settings_path, backup_path)
            print(f"Created backup of original settings at: {backup_path}")
        
        # Write the new settings
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=4)
        
        print(f"Successfully updated Cursor settings at: {settings_path}")
        print("Please restart Cursor for the changes to take effect.")
        return True
    except Exception as e:
        print(f"Error saving Cursor settings: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Configure Cursor for Unreal MCP')
    parser.add_argument('--script', help='Path to the run_unreal_mcp.bat script', 
                        default=os.path.abspath(os.path.join(os.path.dirname(__file__), 'run_unreal_mcp.bat')))
    
    args = parser.parse_args()
    
    # Get absolute path to the run script
    run_script_path = os.path.abspath(args.script)
    
    if not os.path.exists(run_script_path):
        print(f"Error: Run script not found at: {run_script_path}")
        return 1
    
    # Configure Cursor
    if configure_cursor_mcp(run_script_path):
        print("\nCursor has been configured to use Unreal MCP!")
        print("\nTo use with Cursor:")
        print("1. Make sure Unreal Engine with MCP plugin is running")
        print("2. Start Cursor and it should automatically use the Unreal MCP tools")
        return 0
    else:
        print("\nFailed to configure Cursor for Unreal MCP.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 