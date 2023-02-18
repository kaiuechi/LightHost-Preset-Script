# LightHost-Preset-Script

*Script is for use with ![LightHost](https://github.com/rolandoislas/LightHost)*

Simple script that lets you save your plugin settings to disk, then quickly swap between saved presets.

### Important

This script works by copying LightHost's settings file.  
LightHost only saves your plugin states to this file when closed normally.  
Thus, if you kill LightHost by running this script, you may lose changes made __since the last time you closed LightHost normally.__  
If you've made recent changes to your plugins, manually close LightHost rather than killing it via this script.

## Setup

### Set up config.txt

* LightHostExecutableName: The name of the LightHost executable. 
  * Unless you make a habit of renaming your .exe files, the default value should be correct
  
* LightHostExecutableName: The *full* path to the LightHost executable.

* LightHostSettingsPath: The *full* path to where LightHost's default "Light Host.settings" file is saved
  * You might find this under AppData/Roaming/Light Host

* LightHostPresetsPath: The path your presets will be saved to.
  * Make sure there won't be anything besides your presets in this directory.
  
#### Alternative Restart Method
If running Windows, there is an alternative method the script can use to restart LightHost that should behave better than the default.

To enable:
* Go to line 225 in the "LHquickswap.py" file
* Uncomment the "subprocess.run(...)" line
* Comment out the "os.startfile(...)" line


