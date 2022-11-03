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

UTILITY CONVERTERS MODULE
'''

import subprocess
import utils.utils as utils

def cap_to_HS():
    filename = ""
    while True:
        utils.header("Utility Converter", ["Convert captured file to Hashcat Capture file",".cap to .hccap"])
        filename = input("Enter filename: ")
        if filename.strip() == "":
            break
    if ".cap" not in filename:
        filename += ".cap"

    #ASK FOR OUTPUT FILENAME

    #CHECK FILE

    #DO AIRCRACK COMMAND: aircrack-ng -j hashcat w_handshake.cap
    return None

def cap_to_HS3():
    return None