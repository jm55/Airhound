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
import interfaces.interfaces as interface

def get_target(device):
    utils.header("Scan","Scan and Select target WiFi network.")
    interface.print_device_summary(device)
    print("")
    utils.print_bar(len("Scan and Select target WiFi network."))

    wifi_list = scan_wifi(device)
    
    return None

def scan_wifi(device):
    service_status = True
    device_logicalname = interface.get_logicalname(device)
    device_macaddress = interface.get_macaddress(device)
    device_driver = interface.get_driver(device)

    #Disable WLAN/Network Services
    while service_status:
        utils.header("Disabling possible interfering WLAN processes...")
        service_status = interface.terminate_services()
    utils.header("Possible interfering WLAN processes disabled!")
    utils.getch()
        

    #Re-enable WLAN/Network Services
    while not service_status:
        utils.header("Disabling possible interfering WLAN processes...")
        service_status = interface.restart_services()
    utils.header("Possible interfering WLAN processes disabled!")
    utils.getch()

    #Return collected WiFi Networks
    return None

#IMPLEMENT ANYTHING HERE ACCORDINGLY