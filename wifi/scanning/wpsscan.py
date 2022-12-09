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
            6. Bluetooth Reconnaissance
============================================================

WPS SCAN & TARGET MODULE
'''

import subprocess
import utils.utils as utils
import interfaces.interfaces as interface
import time
import os
import json

##Scan for WiFi (WPS) using WLAN device (device) and return target WiFi based on user selection
def get_target(device):
    #Notify about unguaranteed scanning
    utils.header("WiFi Scan + Capture", "Do note that this tool may not work depending conditions not suitable for \'wash\' to run.")
    utils.getch()

    #Scan & Select WiFi Network
    utils.header("WiFi Scan + Capture", "Scan and Select target WiFi network.")
    interface.print_device_summary(device)
    print("")
    utils.print_bar(len("WPS Scan and Select target WiFi network."))
    rescan = True
    while rescan:
        wps_list = scan_wifi(device)
        utils.header("WiFi Scan + Capture","WiFi Scan Finished")
        if len(wps_list) == 1:
            utils.header("WiFi Scan + Capture", 
                            [
                                "WiFi (WPS) Scan failed to find WiFi networks",
                                "You may need to replug your WLAN device and reconfigure WLAN selection."
                            ]
                        )
            utils.getch()
            if not utils.yesNo("WiFi Scan + Capture", question="Do you want to do a rescan?", explicit=False):
                rescan = False
        else:
            rescan = False
            invalid = True
            target_id = -1
            while invalid:
                utils.header("WiFi Scan + Capture","WiFi Scan Finished")
                filtered_list = utils.simplify_wifi_list(wps_list, True)
                pretty_print(filtered_list)
                print("")
                try:
                    print("Enter \'0\' to cancel target selection.")
                    target_id = int(input("Enter ID# of target WiFi network: "))
                    if target_id == 0:
                        rescan = False
                        invalid = False
                    elif target_id < 1 or target_id > len(filtered_list):
                        invalid = True
                    else:
                        invalid = False
                        return filtered_list[target_id-1]
                except ValueError:
                    invalid = True
    return None

def scan_wifi(device):
    service_status = False
    device_logicalname = interface.get_logicalname(device)
    wps_list= []

    #Disable WLAN/Network Services
    while not service_status:
        utils.header("Loading monitoring mode...")
        enable = interface.enable_monitor(device)
        device = enable[1]
        service_status = enable[0]
    utils.header("Possible interfering WLAN processes disabled!")
    utils.getch()

    #Ask for min time for scanning
    countdown = utils.set_countdown("WiFi (WPS) Scan Time", 20, 240)

    #Prepare command
    filename = utils.getFormattedDT()
    wash_command = "wash -i " + device_logicalname + " > " + filename + ".txt"

    #Execute command
    wash = subprocess.Popen(wash_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    #Terminate at specified time; Does not indicate networks scanned.
    utils.display_countdown("Scanning Network...","Mode: WPS", countdown)
    wash.kill()

    #Rename file to remove <filename>-xx.csv suffix
    #Show as "Loading..."
    utils.header("Loading results...")

    #Print collected information and cleanup temp files
    wps_list = utils.parseWashOutput(filename + ".txt")
    os.remove(filename + ".txt")

    while not service_status:
        utils.header("Ending monitoring mode...")
        service_status = interface.disable_monitor(device) and interface.check_connection()
    utils.header("WLAN/Network Services Restored!")
    utils.getch()

    return wps_list

#Prints the filtered list accordingly
def pretty_print(filtered_list:str):
    print("ID".ljust(4)+"MAC Address".ljust(21)+"SSID".ljust(36)+"Power (dBm)".ljust(13)+"Channel".ljust(7))
    for wifi in filtered_list:
        print(wifi["id"].ljust(4)+ wifi["bssid"].ljust(21)+
            wifi["essid"].ljust(36)+wifi["power"].ljust(13)+wifi["channel"].ljust(7)) 