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
            1. WPA Scanning & Handshake Capture
            2. WPA Cracking
            3. WiFi DOS
            4. Other Tools
            5. Windows Saved WiFi Passwords
============================================================

WPA SCAN & TARGET MODULE
'''

import subprocess
import re
import time
import os
import utils.utils as utils
import interfaces.interfaces as interface

#Scan for WiFi (WPA) using WLAN device (device) and return target WiFi based on user selection
def get_target(device):
    utils.header("WiFi WPA Scan + Capture","Scan and Select target WiFi network.")
    interface.print_device_summary(device)
    print("")
    utils.print_bar(len("Scan and Select target WiFi network."))

    #Scan and filter wpa_list
    wpa_list = scan_wifi(device)
    filtered_list = utils.simplify_wifi_list(wpa_list, False) #Print and return filtered selection
    
    #Ask to select WiFi
    target_id = -1 #WiFi selector
    if len(wpa_list) == 0:
        utils.header("WiFi Results",["No WiFi Networks Found!","Can be attributed to ", 
                                    "Lack of WiFi networks available","or",
                                    "WLAN device incapable of monitor/injection mode."])
        utils.getch()
        return None
    else:
        invalid = True
        while invalid:
            utils.header("WiFi WPA Scan + Capture","WiFi Scan Finished!")
            pretty_print(filtered_list)
            print("")
            try:
                print("Enter \'0\' to cancel target selection.")
                target_id = int(input("Enter ID# of target WiFi network: "))
                if target_id == 0:
                    return None
                elif target_id < 0 or target_id > len(filtered_list):
                    invalid = True
                else:
                    invalid = False
                    return filtered_list[target_id-1]
            except ValueError:
                invalid = True

#Delegates WiFi scanning for WPA; Uses airodump-ng
def scan_wifi(device):
    service_status = False
    device_logicalname = interface.get_logicalname(device)
    device_macaddress = interface.get_macaddress(device)
    device_driver = interface.get_driver(device)
    wpa_list = []

    #Disable WLAN/Network Services
    while not service_status:
        utils.header("Loading monitoring mode...")
        enable = interface.enable_monitor(device)
        device = enable[1]
        service_status = enable[0]
    utils.header("Possible interfering WLAN processes disabled!")
    utils.getch()
    
    #Ask for min time for scanning; Max at 60seconds
    countdown = utils.set_countdown("WiFi (WPA) Scan Time", 10, 120)

    #Prepare command
    filename = utils.getFormattedDT()
    command = "airodump-ng " + device_logicalname + " --update 1 --wps --encrypt wpa -w "  + filename + " -o csv" #checks for wpa-only and wps (whether 0 or non-0) and saves as csv

    #Execute command
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1)
    
    #Terminate at specified time; Does not indicate networks scanned.
    utils.display_countdown("Scanning Network...", "Mode: WPA", countdown)
    process.kill()

    #Rename file to remove <filename>-xx.csv suffix
    #Show as "Loading..."
    utils.header("Loading results...")
    utils.renameFile(filename + "-01.csv ", filename + ".csv")
    if not utils.checkFile(filename + ".csv"):
        print("Error occured while loading file, exiting...")
        exit(1)

    #Print collected information and cleanup temp files
    wpa_list = utils.csvToList(filename)
    os.remove(filename + ".csv")

    #Re-enable WLAN/Network Services
    while not service_status:
        utils.header("Ending monitoring mode...")
        service_status = interface.disable_monitor(device) and interface.check_connection()
    utils.header("WLAN/Network Services Restored!")
    utils.getch()

    #Return collected WiFi Networks
    return wpa_list

#Prints the filtered list accordingly
def pretty_print(filtered_list:list):
    print("ID".ljust(4)+"MAC Address".ljust(21)+"SSID".ljust(36)+"Security".ljust(18)+"Cipher".ljust(21)+"Power (dBm)".ljust(13)+"Channel".ljust(7))
    for wifi in filtered_list:
        print(wifi["id"].ljust(4)+ wifi["bssid"].ljust(21)+
            wifi["essid"].ljust(36)+ wifi["privacy"].ljust(18)+ 
            wifi["cipher"].ljust(21)+ wifi["power"].ljust(13)+wifi["channel"].ljust(7)) 