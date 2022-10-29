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

WIFI SCAN & TARGET MODULE
'''

import subprocess
import utils.utils as utils
import scanning.interfaces.interfaces as interface

def get_target(device):
    utils.header("Scan","Scan and Select target WiFi network.")
    interface.print_device_summary(device)
    print("")
    utils.print_bar(len("Scan and Select target WiFi network."))
    
    #Use these device details however needed
    device_logicalname = interface.get_logicalname(device)
    device_macaddress = interface.get_macaddress(device)
    device_driver = interface.get_driver(device)
    '''
    =======================
    Airmon-ng Terminologies
    =======================
    ssid        = essid
    mac-address = bssid 

    =======================================================================
                                INSTRUCTIONS
    =======================================================================
    Implement any function that would return 
    a list containing [ssid, mac-address] of
    the selected/target WiFi network.

    Use the device variable (containing raw JSON)
    for device selection on airmon-ng.

    You may have to consider executing 'sudo airmon-ng start <device>'
    before running any airmon-ng scanning and airodump-ng capture commands.

    If user has not selected a target WiFi network, return as None
    Otherwise return target WiFi details in [ssid, mac-address]
    '''
    return None

#IMPLEMENT ANYTHING HERE ACCORDINGLY