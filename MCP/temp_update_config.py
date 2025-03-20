"""
Script to configure Claude Desktop MCP integration.

This script will update or create the necessary configuration for Claude Desktop
to use the Unreal MCP bridge.
"""

import json
import os
import sys
import shutil
from pathlib import Path

def check_claude_installed():
    """Check if Claude Desktop is installed by looking for common installation paths."""
    claude_paths = []
    
    if os.name == 'nt':  # Windows
        claude_paths = [
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'Claude Desktop', 'Claude Desktop.exe'),
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'Claude Desktop', 'Claude Desktop.exe'),
            os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Claude Desktop', 'Claude Desktop.exe')
        ]
    elif os.name == 'darwin':  # macOS
        claude_paths = [
            '/Applications/Claude Desktop.app',
            os.path.expanduser('~/Applications/Claude Desktop.app')
        ]
    
    # Check if any of the paths exist
    for path in claude_paths:
        if os.path.exists(path):
            return True
    
    # Check if config directory exists as a fallback
    claude_config_dir = os.environ.get('APPDATA', '')
    if os.name == 'nt':  # Windows
        claude_config_dir = os.path.join(claude_config_dir, 'Claude')
    elif os.name == 'darwin':  # macOS
        claude_config_dir = os.path.expanduser('~/Library/Application Support/Claude')
    
    return os.path.exists(claude_config_dir)

def update_claude_config(config_file, run_script):
    """Update the Claude Desktop configuration file."""
    # Check if Claude is installed
    if not check_claude_installed():
        print(f"Claude Desktop doesn't appear to be installed on this system.")
        print("You can download Claude Desktop from: https://claude.ai/download")
        print("After installing Claude Desktop, run this script again.")
        return False
    
    # Make sure the config directory exists
    config_dir = os.path.dirname(config_file)
    if not os.path.exists(config_dir):
        try:
            print(f"Creating Claude configuration directory: {config_dir}")
            os.makedirs(config_dir, exist_ok=True)
        except Exception as e:
            print(f"Error creating Claude configuration directory: {str(e)}")
            return False
    
    # Load existing config or create new one
    config = {}
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Creating new Claude Desktop configuration file.")
    
    # Create backup of the original file if it exists
    if os.path.exists(config_file):
        backup_path = config_file + '.bak'
        try:
            shutil.copy2(config_file, backup_path)
            print(f"Created backup of original configuration at: {backup_path}")
        except Exception as e:
            print(f"Warning: Couldn't create backup: {str(e)}")
    
    # Update the config
    config.setdefault('mcpServers', {})['unreal'] = {'command': run_script, 'args': []}
    
    # Save the updated configuration
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
        
        print(f"Successfully updated Claude Desktop configuration at: {config_file}")
        return True
    except Exception as e:
        print(f"Error saving Claude Desktop configuration: {str(e)}")
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage: python temp_update_config.py <config_file> <run_script>")
        return 1
    
    config_file = sys.argv[1]
    run_script = sys.argv[2]
    
    # Get absolute paths
    config_file = os.path.abspath(config_file)
    run_script = os.path.abspath(run_script)
    
    if not os.path.exists(run_script):
        print(f"Error: Run script not found at: {run_script}")
        return 1
    
    # Update the configuration
    if update_claude_config(config_file, run_script):
        print("\nClaude Desktop has been configured to use Unreal MCP!")
        print("\nTo use with Claude Desktop:")
        print("1. Make sure Unreal Engine with MCP plugin is running")
        print("2. Start Claude Desktop and it should automatically use the Unreal MCP tools")
        return 0
    else:
        print("\nFailed to configure Claude Desktop for Unreal MCP.")
        return 1

if __name__ == "__main__":
    sys.exit(main())