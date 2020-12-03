set-iterm2-background-color
===========================

This Python3 script will change the background color of the current iTerm session. Enable as an AutoLaunch script for each new iTerm2 session to be assigned a new color.

## Installation

1. Make sure iTerm2 Python Runtime Environment is installed
2. Create `AutoLaunch` dir in iTerm2 scripts directory
   ```bash
   mkdir ~/Library/Application\ Support/iTerm2/Scripts/AutoLaunch
   ```
3. Copy `random-color.py` to the `AutoLaunch` dir
   ```bash
   cp random-color.py ~/Library/Application\ Support/iTerm2/Scripts/AutoLaunch/
   ```
4. Enable Python API
   * Preferences > General > Magic > Enable Python API
5. Enable `random-color.py` script
   * Scripts > AutoLaunch > random-color.py (make sure it's checked)
