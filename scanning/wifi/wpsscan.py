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

WPS SCAN & TARGET MODULE
'''

import subprocess
import utils.utils as utils
import interfaces.interfaces as interface
import time
import os
import json

def get_target(device):
    utils.header("WiFi (WPS) Scan + Capture", "Do note that this tool may not work depending conditions not suitable for \'wash\' to run.")
    utils.getch()

    utils.header("WiFi (WPS) Scan + Capture", "WPS Scan and Select target WiFi network.")
    interface.print_device_summary(device)
    print("")
    utils.print_bar(len("WPS Scan and Select target WiFi network."))

    rescan = True
    while rescan:
        #wps_list = scan_wifi(device)
        wps_list = utils.parseWashOutput("others/test/wash.txt")
        utils.header("WiFi (WPS) Scan + Capture","WPS Scan Finished")
        if len(wps_list) == 1:
            utils.header("WiFi (WPS) Scan + Capture", 
                            [
                                "WPS Scan failed to find WPS WiFi networks",
                                "You may need to replug your WLAN device and reconfigure WLAN selection."
                            ]
                        )
            utils.getch()
            if not utils.yesNo("WiFi (WPS) Scan + Capture", question="Do you want to do a rescan?", explicit=False):
                rescan = False
        else:
            rescan = False
            invalid = True
            target_id = -1
            while invalid:
                utils.header("WiFi (WPS) Scan + Capture","WPS Scan Finished")
                filtered_list = utils.simplify_wifi_list(wps_list, True)
                pretty_print(filtered_list)
                print("")
                try:
                    print("Enter \'0\' to cancel target selection.")
                    target_id = int(input("Enter ID# of target WiFi network: "))
                    if target_id == 0:
                        rescan = False
                        invalid = False
                    elif target_id < 1 or target_id > len(filtered_list)-1:
                        invalid = True
                    else:
                        invalid = False
                        return filtered_list[target_id-1]
                except ValueError:
                    invalid = True
    return None

def scan_wifi(device):
    service_status = True
    device_logicalname = interface.get_logicalname(device)
    device_macaddress = interface.get_macaddress(device)
    device_driver = interface.get_driver(device)
    wps_list= []

    #Disable WLAN/Network Services
    while service_status:
        utils.header("Disabling possible interfering WLAN processes...")
        service_status = interface.terminate_services()
    utils.header("Possible interfering WLAN processes disabled!")
    utils.getch()

    #Ask for min time for scanning; Max at 60seconds
    valid = False
    countdown = -1
    min = 60
    max = 240
    while not valid:
        utils.header("WiFi WPS Scan Time")
        try:
            entry = int(input("Enter time (sec) to scan (limited " + str(min) + "s to " + str(max) + "s): "))
            if entry >= min and entry < max:
                countdown = entry
                valid = True
            elif entry > max:
                utils.header("Time entered exceeds max limit!","Time set to " + str(max) + " seconds.")
                countdown = max
                valid = True
            elif entry < min:
                utils.header("Invalid time, please try again!")
                utils.getch()
        except ValueError:
            valid = False

    #Prepare command
    filename = utils.getFormattedDT()
    command = "sudo wash -i " + device_logicalname + " > " + filename + ".txt"

    #Execute command
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1)

    #Terminate at specified time; Does not indicate networks scanned.
    while countdown:
        utils.header("Scanning Network...", ["Mode: WPS","\n","Time Left: " + str(countdown) + " seconds"])
        time.sleep(1)
        countdown -= 1
    process.kill()

    #Rename file to remove <filename>-xx.csv suffix
    #Show as "Loading..."
    utils.header("Loading results...")

    #Print collected information
    wps_list = utils.parseWashOutput(filename + ".txt")

    os.remove(filename + ".txt")

    return wps_list

def pretty_print(filtered_list:str):
    print("ID".ljust(4)+"MAC Address".ljust(21)+"SSID".ljust(36)+"Power (dBm)".ljust(13))
    for wifi in filtered_list:
        print(wifi["id"].ljust(4)+ wifi["bssid"].ljust(21)+
            wifi["essid"].ljust(36)+wifi["power"].ljust(13)) 