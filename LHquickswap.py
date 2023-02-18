#!/usr/bin/env python
# coding: utf-8

# In[1]:


import io
import os
import psutil
import json
import shutil
import time
import subprocess
import sys


# In[2]:


print("Loading config")
with open('config.txt', 'r') as cfgFile:
    cfgRaw = cfgFile.read()
    
cfgDict = json.loads(cfgRaw)

LHExcPath = cfgDict['LightHostExecutablePath'] #path to LH executable
LHExcName = cfgDict['LightHostExecutableName'] #name of LH executable
LHSettingsPath = cfgDict['LightHostSettingsPath'] #location of LH's own settings file
LHPresetsPath = cfgDict['LightHostPresetsPath'] #location to save setting presets to

print("LightHost Executable Path: " + LHExcPath)
print("LightHost Executable Name: " + LHExcName)
print("LightHost Settings Path: " + LHSettingsPath)
print("Saved Presets Path: " + LHPresetsPath)


# In[3]:


def checkProcessRunning(processName):
    for p in psutil.process_iter():
        if processName in p.name():
            return True
        
    return False

    
def killByName(processName): 
    #this might be safer? idk
    #really ought to learn more about how this stuff works
        #but right now i need my funny vst settings
    for p in psutil.process_iter():
        if processName in p.name():
            p.terminate()
            
def saveCurrentSettings():
    #should save current LH settings to preset save path
    #user defines name to save as
    #should warn that reusing a name will save over old preset
    print("Saving existing LightHost plugin settings...")
    print("(Note that saving over an existing preset name will overwrite that preset)")
    print("Enter name of new preset. (type 'back' to cancel)")
    newPresetName = input()
    if newPresetName.lower() == 'back':
        print("Saving canceled.")
        return None
    else:
        shutil.copyfile(LHSettingsPath, LHPresetsPath + newPresetName)
        print("Saved settings to " + LHPresetsPath + newPresetName)
    
def loadPreset():
    #loads an existing preset
    #maybe read presets into dict/list and have user select with a number?
    #might need to implement multiple page display if there is a bunch of presets
    #should warn user that current settings will be overridden and lost
    exitSelection = False
    print("Preparing to load saved preset...")
    print("(Note that currently active LightHost settings will be lost)")
    
    
    #actually i don't need any of this, do i?
    #presetDict = {}
    #w = 1
    #for preset in os.listdir(LHPresetsPath):
    #    #presetPath = LHPresetsPath + preset #lets do this later
    #    presetDict[str(w)] = preset
    #    w += 1
    
    presetList = os.listdir(LHPresetsPath)

    pageStart = 0  #list index the page display starts from
    pageMax = 9 #max items per page
    currentPage = 1 #current page (doesn't control anything, just for ui)
    while not exitSelection:

        nextPageAvailable = False
        prevPageAvailable = False
        
        print("Available Presets:")
        print("(Page " + str(currentPage) + ")")
        w = 0
        validInputs = []
        while (w < pageMax) and ((w + pageStart) < len(presetList)):
            presetDisplay = presetList[w + pageStart]
            print("\t" + str(w + 1) + " - " + presetDisplay)
            validInputs.append(str(w+1))
            w += 1
            
        print("Enter number of preset to load")
        
        #check if next page available
        if (w + pageStart) < len(presetList):
            print("(Enter 'next' for next page)")
            nextPageAvailable = True
        
        #check if prev page available
        if (pageStart > 0) and ((pageStart - pageMax) >= 0):
            print("(Enter 'prev' for previous page)")
            prevPageAvailable = True
            
        print("(Enter 'back' to cancel preset load)")
        
        response = input()
        
        if response in validInputs:
            #copy preset path to settings path
            selection = int(response)
            selectedPreset = presetList[selection - 1 + pageStart]
            print("Loading preset '" + selectedPreset + "' - Confirm? (y/n)")
            loadConfirmation = input()
            if loadConfirmation.lower() == "y":
                print("Loading...")
                presetPath = LHPresetsPath + selectedPreset
                shutil.copyfile(presetPath, LHSettingsPath)
                print("Preset '" + selectedPreset + "' loaded.")
                exitSelection = True
                
            else:
                print("Canceling load...")
        
        elif nextPageAvailable and response.lower() == 'next':
            pageStart = pageStart + pageMax 
            #swapping page like this /looks/ like it could break but so long
            #as i have the checks for next/prevPageAvailable it should be fine
            currentPage += 1
        
        elif prevPageAvailable and response.lower() == 'prev':
            pageStart = pageStart - pageMax
            currentPage -= 1
            
        elif response.lower() == 'back':
            exitSelection = True
            print("Returning to main selection...")
            
        else:
            print("Invalid Syntax")


# In[4]:


#checkProcessRunning(LHExcName)


# In[10]:


#testRunExcName = 'temp'
#os.startfile(testRunExcName) #this works!


# In[9]:


exit = False
killExistingLH = False #gives the go-ahead to kill LH process
restartPrompt = False #triggers prompt to reboot LH on program exit

if checkProcessRunning(LHExcName):
    print('LightHost currently running!')
    print('This script will only run if there is not an active LightHost instance')
    print('Kill running LightHost process now? (y/n)')
    print("\tNOTE!!! Lighthost only saves plugin settings on standard exit.")
    print("\tIf you've made changes to your plugins during this instance,\n\tthen shut down LightHost manually, instead.")
    confirmKill = input()
    
    if confirmKill.lower() == 'y':
        killExistingLH = True
    else:
        exit = True
        print("LightHost process not killed.")
        print("Please close LightHost before running this script.")
else:
    print('LightHost not running')
    print('Continuing...')
    restartPrompt = True
    
if killExistingLH:
    killByName(LHExcName)
    print('LightHost process terminated')
    restartPrompt = True
    
while not exit:
    print('Select action:')
    print("\t'save' - Save current LightHost settings as a preset")
    print("\t'load' - Load a saved LightHost preset")
    print("\t'exit' - Quit")
    response = input()
    if response.lower() == 'exit':
        exit = True
    elif response.lower() == 'save':
        saveCurrentSettings()
    elif response.lower() == 'load':
        loadPreset()
    else:
        print('Invalid Syntax')
        
    
if restartPrompt:
    print('Restart LightHost before exiting? (y/n)')
    restartResponse = input()
    if restartResponse.lower() == 'y':

        #swap to the subprocess line if on windows
        #subprocess.run('explorer "' + LHExcPath + '"', shell=True)
        os.startfile(LHExcPath)

        print("Restarting LightHost...")
        
print('Exiting...')

time.sleep(1.5)


# In[5]:





# In[ ]:




