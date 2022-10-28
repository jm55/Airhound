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

LINUX SUBDRIVER MODULE
'''


import utils.utils as utils
import scanning.interfaces.interfaces as interfaces
import scanning.wifi.scan as scan
import time
import json

wlan_device = None

#Driver for Linux-based functionalities
#Serves as home menu
#After each function has been completed, please return to this function (within the while-loop)
def run():
    utils.confirm(utils.running_OS())
    invalid = True
    wlan_device = interfaces.get_interfaces()
    while invalid:
        int_choices = ["1","2","3","4","5","6","0"]
        str_choices = [ "WiFi Scan & Capture", "WiFi Cracking",
                        "Full Suite (Scan&Capture + Crack)","WAP Admin Attack", 
                        "WiFi DOS", "Select WLAN Device","Exit"]
        utils.header("Tools Menu", "WLAN Device Selected: " + interfaces.get_logicalname(wlan_device))
        choice = utils.menu(int_choices, str_choices)
        if utils.valid_choice(choice, int_choices):
            if choice == "0": #EXIT
                exit(0)
            elif choice == "1": #WIFI SCAN
                if wlan_device != None:
                    target = scan.get_target(wlan_device)
                else:
                    utils.header(str_choices[0])
                    print("Function not allowed.\nYou haven't selected a WLAN device.")
            elif choice == "2": #WIFI CRACKING
                print("Test: " + str_choices[int(choice)-1])
            elif choice == "3": #WIFI SCAN+CRACK
                print("Test: " + str_choices[int(choice)-1])
            elif choice == "4": #WAP ADMIN ATTACK
                print("Test: " + str_choices[int(choice)-1])
            elif choice == "5": #WIFI DOS
                print("Test: " + str_choices[int(choice)-1])
            elif choice == "6": #SELECT WLAN DEVICE
                wlan_device = interfaces.get_interfaces()
            
            print("")
            utils.getch()
    exit(0)
