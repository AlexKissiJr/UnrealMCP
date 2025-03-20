# UnrealMCP Plugin
[![smithery badge](https://smithery.ai/badge/@AlexKissiJr/unrealmcp)](https://smithery.ai/server/@AlexKissiJr/unrealmcp)

# VERY WIP REPO
I'm working on adding more tools now and cleaning up the codebase, 
I plan to allow for easy tool extension outside the main plugin

This is very much a work in progress, and I need to clean up a lot of stuff!!!!!

Also, I only use windows, so I don't know how this would be setup for mac/unix

## Overview
UnrealMCP is an Unofficial Unreal Engine plugin designed to control Unreal Engine with AI tools. It implements a Machine Control Protocol (MCP) within Unreal Engine, allowing external AI systems to interact with and manipulate the Unreal environment programmatically.

I only just learned about MCP a few days ago, so I'm not that familiar with it, I'm still learning so things might be initially pretty rough.
I've implemented this using https://github.com/ahujasid/blender-mcp as a reference, which relies on Claude for Desktop. It now works with both Claude for Desktop and Cursor. If you experiment with other models, please let me know!

## ⚠️ DISCLAIMER
This plugin allows AI agents to directly modify your Unreal Engine project. While it can be a powerful tool, it also comes with risks:

- AI agents may make unexpected changes to your project
- Files could be accidentally deleted or modified
- Project settings could be altered
- Assets could be overwritten

**IMPORTANT SAFETY MEASURES:**
1. Always use source control (like Git or Perforce) with your project
2. Make regular backups of your project
3. Test the plugin in a separate project first
4. Review changes before committing them

By using this plugin, you acknowledge that:
- You are solely responsible for any changes made to your project
- The plugin author is not responsible for any damage, data loss, or issues caused by AI agents
- You use this plugin at your own risk

## Features
- TCP server implementation for remote control of Unreal Engine
- JSON-based command protocol for AI tools integration
- Editor UI integration for easy access to MCP functionality
- Comprehensive scene manipulation capabilities
- Python companion scripts for client-side interaction

## Roadmap
These are what I have in mind for development as of 3/14/2025
I'm not sure what's possible yet, in theory anything, but it depends on how
good the integrated LLM is at utilizing these tools.
- [X] Basic operations working
- [X] Python working
- [X] Materials
- [ ] User Extensions (in progress)
- [ ] Asset tools
- [ ] Blueprints
- [ ] Niagara VFX
- [ ] Metasound
- [ ] Landscape (I might hold off on this because Epic has mentioned they are going to be updating the landscape tools)
- [ ] Modeling Tools
- [ ] PCG

## Requirements
- Unreal Engine 5.5 (I have only tested on this version, may work with earlier, but no official support)
- C++ development environment configured for Unreal Engine
- Python 3.7+ for client-side scripting
- Model to run the commands, in testing I've been using Claude for Desktop https://claude.ai/download

## Prerequisites to run
- Unreal Editor Installation (Tested with 5.3, but should work on 5.0+)
- Python 3.7+ (This can run with your existing python install)
- MCP compatible LLM (Claude for Desktop, Cursor, etc.)
- Setup: run setup_unreal_mcp.bat in MCP folder as per instructions in MCP/README_MCP_SETUP.md

## Quick Start for Cursor Users
If you want to use UnrealMCP with Cursor, follow these simple steps:

1. Clone or download this repository as a zip
2. Create a new Unreal Project, or open an existing one
3. Create a "Plugins" folder in your project directory if it doesn't exist
4. Unzip or copy this repository into the Plugins folder
5. Run `setup_cursor_mcp.bat` in the MCP folder
6. Open your Unreal project and enable the plugin in Edit > Plugins (if not already enabled)
7. Start Cursor and ask it to work with your Unreal project

That's it! The setup script will automatically configure everything needed for Cursor integration.

## Installation

### Installing via Smithery

To install unrealmcp for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@AlexKissiJr/unrealmcp):

```bash
npx -y @smithery/cli install @AlexKissiJr/unrealmcp --client claude
```

1. Clone or download this repository as a zip
2. Create a new Unreal Project, or open an existing one
3. Create a "Plugins" folder in your project directory if it doesn't exist
4. Unzip or copy this repository into the Plugins folder
5. Setup MCP 
    - Run the `setup_unreal_mcp.bat` script in the MCP folder (see `MCP/README_MCP_SETUP.md` for details)
    - This will configure Python and your AI assistant (Claude for Desktop or Cursor)
6. Open your Unreal project, the plugin should be available in the Plugins menu
7. If not, enable the plugin in Edit > Plugins
8. Choose your preferred AI assistant:
    - For Claude for Desktop: follow the instructions in the "With Claude for Desktop" section below
    - For Cursor: follow the instructions in the "With Cursor" section below

## With Claude for Desktop
You will need to find your installation directory for Claude for Desktop. Find claude_desktop_config.json and add an entry and make it look like so:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
    "mcpServers": {
        "unreal": {
            "command": "C:/path/to/your/project/Plugins/UnrealMCP/MCP/run_unreal_mcp.bat",
            "args": []
        }
    }
}
```

Alternatively the unreal_mcp_setup.bat script should do this for you.

To find the path to your claude for desktop install you can go into settings and click 'Edit Config'
This is usually in 
```
C:\Users\USERNAME\AppData\Roaming\Claude
```

## With Cursor
Cursor should be automatically configured if you've run the setup script with the Cursor option. If you need to manually configure it:

**Windows:** `%APPDATA%\Cursor\User\settings.json`

Add or update the settings with:
```json
{
    "mcp": {
        "enabled": true,
        "servers": {
            "unreal": {
                "command": "C:/path/to/your/project/Plugins/UnrealMCP/MCP/run_unreal_mcp.bat",
                "args": []
            }
        }
    }
}
```

## Testing
Once everything is setup you need to launch the unreal editor.
Note: Nothing else has to be started or set up to run the mcp bridge, it will run when needed.

Open Claude for Desktop or Cursor, ensure that the tools have successfully enabled, ask your AI assistant to work in Unreal.

Here are some example prompts to try:
- "What actors are in the current level?" 
- "Create a cube at position (0, 0, 100)"
- "List available commands I can use with Unreal Engine"

## Usage
### In Unreal Editor
Once the plugin is enabled, you'll find MCP controls in the editor toolbar button. 
![image](https://github.com/user-attachments/assets/68338e7a-090d-4fd9-acc9-37c0c1b63227)

![image](https://github.com/user-attachments/assets/34f734ee-65a4-448a-a6db-9e941a588e93)

The TCP server can be started/stopped from here.
Check the output log under log filter LogMCP for extra information.

Once the server is confirmed up and running from the editor.
Open Claude for Desktop, ensure that the tools have successfully enabled, ask Claude to work in unreal.

Currently only basic operations are supported, creating objects, modfiying their transforms, getting scene info, and running python scripts.
Claude makes a lot of errors with unreal python as I believe there aren't a ton of examples for it, but let it run and it will usually figure things out.
I would really like to improve this aspect of how it works but it's low hanging fruit for adding functionality into unreal.

### Client-Side Integration
Use the provided Python scripts in the `MCP` directory to connect to and control your Unreal Engine instance:

```python
from unreal_mcp_client import UnrealMCPClient

# Connect to the Unreal MCP server
client = UnrealMCPClient("localhost", 13377)

# Example: Create a cube in the scene
client.create_object(
    class_name="StaticMeshActor",
    asset_path="/Engine/BasicShapes/Cube.Cube",
    location=(0, 0, 100),
    rotation=(0, 0, 0),
    scale=(1, 1, 1),
    name="MCP_Cube"
)
```

## Command Reference
The plugin supports various commands for scene manipulation:
- `get_scene_info`: Retrieve information about the current scene
- `create_object`: Spawn a new object in the scene
- `delete_object`: Remove an object from the scene
- `modify_object`: Change properties of an existing object
- `execute_python`: Run Python commands in Unreal's Python environment
- And more to come...

Refer to the documentation in the `Docs` directory for a complete command reference.

## Security Considerations
- The MCP server accepts connections from any client by default
- Limit server exposure to localhost for development
- Validate all incoming commands to prevent injection attacks

## Troubleshooting
- Ensure Unreal Engine is running with the MCP plugin.
- Check logs in Claude for Desktop for stderr output.
- Reach out on the discord, I just made it, but I will check it periodically
  Discord (Dreamatron Studios): https://discord.gg/abRftdSe
  
### Project Structure
- `Source/UnrealMCP/`: Core plugin implementation
  - `Private/`: Internal implementation files
  - `Public/`: Public header files
- `Content/`: Plugin assets
- `MCP/`: Python client scripts and examples
- `Resources/`: Icons and other resources

## License
MIT License

Copyright (c) 2025 kvick

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Credits
- Created by: kvick
- X: [@kvickart](https://x.com/kvickart)
- Discord: https://discord.gg/abRftdSe
  
### Thank you to testers!!!
- https://github.com/TheMurphinatur
  
- [@sidahuj](https://x.com/sidahuj) for the inspriation



## Contributing
Contributions are welcome, but I will need some time to wrap my head around things and cleanup first, lol
