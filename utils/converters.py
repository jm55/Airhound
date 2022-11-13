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

def cap_to_EWSA():
    filename = ""
    output_filename = ""
    '''
    Do similar to other cap_to_###()

    Command: Use -E instead of -J or -j
    '''
    return output_filename 

def cap_to_HS():
    filename = ""
    while True:
        utils.header("Utility Converter", ["Convert captured file to Hashcat Capture file",".cap to .hccap"])
        filename = input("Enter filename: ")
        if filename.strip() != "":
            break
    if ".cap" not in filename:
        filename += ".cap"

    hcap = "aircrack-ng -J hashcat " + filename
    subprocess.Popen(hcap, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).wait()
    
    output_filename = filename[:len(filename)-4] + ".hccap"
    subprocess.Popen("mv hashcat.hccap " + output_filename, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).wait()
    return output_filename

def cap_to_HS3():
    filename = ""
    while True:
        utils.header("Utility Converter", ["Convert captured file to Hashcat Capture file",".cap to .hccapx"])
        filename = input("Enter filename: ")
        if filename.strip() != "":
            break
    if ".cap" not in filename:
        filename += ".cap"

    hcapx = "aircrack-ng -j hashcat " + filename
    subprocess.Popen(hcapx, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).wait()
    
    output_filename = filename[:len(filename)-4] + ".hccapx"
    subprocess.Popen("mv hashcat.hccapx " + output_filename, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).wait()
    return output_filename