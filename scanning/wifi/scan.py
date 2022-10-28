'''
==============================
NSSECU2 - Hacking Tool Project
==============================
Members: Escalona, Fadrigo, Fortiz, Manzano, Sy
Topic: WiFi Hacking Tool
Description: The objective of this project is to create a packaged tool that will be able to do Wi-Fi scanning, cracking, and admin control access.
Objective Functionalities:
    1. WiFi Scanning
    2. WiFi Cracking
    3. WAP/Router Admin Control Access

WIFI SCAN & TARGET MODULE
'''

import subprocess
import utils.utils as utils
import scanning.interfaces.interfaces as interface

def get_target(device:str):
    utils.header("Scan","Scan and Select target WiFi network.")
    
    print("WLAN Device Details")
    print("WLAN Logicalname: ".ljust(20) + interface.get_logicalname(device))
    print("WLAN MAC Address: ".ljust(20) + interface.get_macaddress(device))
    print("WLAN Driver: ".ljust(20) + interface.get_driver(device))
    print("")
    utils.print_bar(len("Scan and Select target WiFi network."))
    
    '''
    Implement any function that would return 
    a list containing [ssid, mac-address] of
    the target WiFi network.

    Use the device variable (containing raw JSON)
    for device selection on airmon-ng.

    If user has not selected a target WiFi network, return as None
    '''

    return None

#IMPLEMENT ANYTHING HERE ACCORDINGLY