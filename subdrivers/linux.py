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
import wifi.scanning.wpascan as wpascan
import wifi.capture.wpacapture as wpacapture
import wifi.scanning.wpsscan as wpsscan
import wifi.capture.wpscapture as wpscapture
import deauth.deauth as deauth
import admin.admin as admin
import time
import json

#Driver for Linux-based functionalities
#Serves as home menu
#After each function has been completed, please return to this function (within the while-loop)
def run():    
    wlan_device = None #type json; refer to interfaces.get_interface()
    capture_filename = None #type str

    utils.confirm(utils.running_OS())
    invalid = True
    wlan_device = interface.get_interface()
    int_choices = ["1","2","3","4","5","6","0"]
    str_choices = [ "WiFi Scan & Capture", "WiFi Cracking",
                    "Full Suite (Scan&Capture + Crack)","WAP Admin Attack", 
                    "WiFi DOS", "Select WLAN Device","Exit"]
    while invalid:
        desc = "WLAN Device Selected: " + str(interface.get_logicalname(wlan_device))
        utils.header("Tools Menu", desc)    
        choice = utils.menu(int_choices, str_choices)
        if utils.valid_choice(choice, int_choices):
            if choice == "0": #EXIT
                if wlan_device != None:
                    interface.disable_monitor(wlan_device)
                utils.cls()
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
                        mode_invalid = True
                        while mode_invalid:
                            utils.header("WiFi Scan + Capture","Select Mode")
                            int_mode = ["1","2","0"]
                            str_mode = ["WPA Search", "WPS Search", "Exit"]
                            mode = utils.menu(int_mode, str_mode)
                            if utils.valid_choice(mode, int_mode):
                                mode_invalid = False
                                if mode == "1":
                                    capture_filename = wpa_scan_capture(wlan_device)
                                elif mode == "2":
                                    capture_filename = wps_scan_capture(wlan_device)
                                elif mode == "0":
                                    mode_invalid = False
                            else:
                                print("Invalid choice!")
                                utils.getch()
                    elif choice == "3": #FULL SUITE (WIFI SCAN+CAPTURE & WIFI CRACKING)
                        print("Test: " + str_choices[int(choice)-1])
                    elif choice == "5": #WIFI DOS
                        print("Test: " + str_choices[int(choice)-1])
                        wifi_dos(wlan_device)
                    else:
                        exit(1)
            elif choice == "2": #WIFI CRACKING
                print("Test: " + str_choices[int(choice)-1])
                utils.yesNo("WiFi Cracking", "This function expects that you have a captured file already.", "Do you have a captured file?", False)
            elif choice == "4": #WAP ADMIN ATTACK
                credentials = admin_access()
                if credentials != None:
                    utils.header("WAP Admin Attack", ["Username: " + credentials[0], "Password: " + credentials[1]])
            elif choice == "6": #SELECT WLAN DEVICE
                wlan_device = interface.get_interface()
            interface.disable_monitor(wlan_device)
    exit(0)

def admin_access():
    utils.header("WAP Admin Attack")
    credentials = admin.scrape_credentials()

    if credentials == None:
        utils.header("WAP Admin Attack", "No credentials attained")
        utils.getch()
    return credentials #Return a tuple/dictionary containing the username and password of the network device, none if exit or nothing is really attained.

def wpa_scan_capture(wlan_device):
    target = wpascan.get_target(wlan_device) #Find target WiFi network (via Scanning and Targetting)
    if target != None:
        return wpacapture.capture_handshake(wlan_device, target) #Capture Handhake (includes Deauth if set)
    else:   
        print("No target WiFi selected!")
        utils.getch()
        return None #Return captured filename

def wps_scan_capture(wlan_device):
    if check_wlan(wlan_device):
        target = wpsscan.get_target(wlan_device)
    else:
        print("Function not allowed.\nYou haven't selected a WLAN device.")

def wifi_dos(wlan_device):
    deauth.wifi_dos(wlan_device)
    utils.display_countdown("WiFi DOS (Deauth) Attack", "Stopping deauth attack...", 5)