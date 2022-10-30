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

LINUX SUBDRIVER MODULE
'''

import utils.utils as utils
import interfaces.interfaces as interface
import scanning.wifi.scan as scan
import scanning.wifi.capture as capture
import deauth.deauth as deauth
import time
import json

#Driver for Linux-based functionalities
#Serves as home menu
#After each function has been completed, please return to this function (within the while-loop)
def run():    
    wlan_device = None #type json; refer to interfaces.get_interface()
    capture_filename = None #type file
    
    utils.confirm(utils.running_OS())
    invalid = True
    wlan_device = interface.get_interface()
    while invalid:
        int_choices = ["1","2","3","4","5","6","0"]
        str_choices = [ "WiFi Scan & Capture", "WiFi Cracking",
                        "Full Suite (Scan&Capture + Crack)","WAP Admin Attack", 
                        "WiFi DOS", "Select WLAN Device","Exit"]
        descs = [
                    "WLAN Device Selected: " + str(interface.get_logicalname(wlan_device)),
                    "Previous Captured File: " + str(capture_filename)
                ]
        utils.header("Tools Menu", descs)
        choice = utils.menu(int_choices, str_choices)
        if utils.valid_choice(choice, int_choices):
            if choice == "0": #EXIT
                exit(0)
            elif choice == "1" or choice == "3" or choice == "5":
                if wlan_device == None:
                    utils.header("No WLAN device selected", 
                                    [
                                    "Please proceed to \"6 - Select WLAN Device\"",
                                    "on the main menu to select WLAN device."
                                    ]
                                )
                else:
                    if choice == "1": #WIFI SCAN+CAPTURE
                        capture_filename = wifi_scan_capture(wlan_device)
                    elif choice == "3": #FULL SUITE (WIFI SCAN+CAPTURE & WIFI CRACKING)
                        print("Test: " + str_choices[int(choice)-1])
                    elif choice == "5": #WIFI DOS
                        print("Test: " + str_choices[int(choice)-1])
                        wifi_dos(wlan_device)
                    else:
                        print("How did you get here??")
                        exit(1)
            elif choice == "2": #WIFI CRACKING
                print("Test: " + str_choices[int(choice)-1])
                utils.yesNo("WiFi Cracking", "This function expects that you have a captured file already.", "Do you have a captured file?", False)
            elif choice == "4": #WAP ADMIN ATTACK
                print("Test: " + str_choices[int(choice)-1])
            elif choice == "6": #SELECT WLAN DEVICE
                wlan_device = interface.get_interface()
            print("")
            utils.getch()
    exit(0)

def wifi_scan_capture(wlan_device):
    if wlan_device != None:
        target = scan.get_target(wlan_device) #Find target WiFi network
        if target != None:
            bssid = target["bssid"] #mac-address
            essid = target["essid"] #ssid
            return capture.capture_handshake(wlan_device, target)
        else:   
            print("No target WiFi selected!")
            utils.getch()
    else:
        utils.header(str_choices[0])
        print("Function not allowed.\nYou haven't selected a WLAN device.")
    return None #Return captured filename

def wifi_dos(wlan_device):
    print("WiFi_DOS")