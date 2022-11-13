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
import utils.converters as converters
import utils.benchmark as benchmark
import interfaces.interfaces as interface
import wifi.scanning.wpascan as wpascan
import wifi.capture.wpacapture as wpacapture
import wifi.scanning.wpsscan as wpsscan
import cracking.wpa as wpacracking
import cracking.wps as wpscracking
import deauth.deauth as deauth
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
    int_choices = ["1","2","3","4","5","6","7","0"]
    str_choices = [ "WPA Scan & Capture", "WPA Cracking",
                    "WPA Full Suite (Scan & Capture + Crack)","WPS Scan and Crack BETA", 
                    "WiFi DOS", "Select WLAN Device","Utilities","Exit"]
    while invalid:
        desc = "WLAN Device Selected: " + str(interface.get_logicalname(wlan_device) + " (" + str(interface.get_driver(wlan_device)) + ")")
        utils.header("Tools Menu", desc)   
        choice = utils.menu(int_choices, str_choices)
        if utils.valid_choice(choice, int_choices):
            
            #Exit
            if choice == "0":
                if wlan_device != None:
                    interface.disable_monitor(wlan_device)
                utils.cls()
                exit(0)
            
            #Commands that need WLAN device in monitoring mode
            elif choice == "1" or choice == "3" or choice == "4" or choice == "5":
                #No WLAN device specified
                if wlan_device == None:
                    utils.header("No WLAN device selected", 
                                    [
                                    "Please proceed to \"6 - Select WLAN Device\"",
                                    "on the main menu to select WLAN device."
                                    ]
                                )
                    utils.getch()
                #w/ WLAN device specified
                else:
                    if choice == "1": #WIFI SCAN+CAPTURE
                        raw_capture = wpa_scan_capture(wlan_device)
                        if raw_capture != None:
                            capture_filename = raw_capture[0]
                    elif choice == "3": #FULL SUITE (WIFI SCAN+CAPTURE & WIFI CRACKING)
                        fullsuite(wlan_device)
                    elif choice == "4": #WPS SCAN+CRACK
                        wps_halted = False
                        
                        if not wps_halted:
                            utils.header("WPS Scan + Cracking", ["Note","This feature of the program is not guaranteed to work all", " the time due to WAPs having protection against Reaver attacks."])
                            utils.getch()
                            wps_wifi = wps_scan(wlan_device)
                            if wps_wifi == None:
                                utils.header("WPS Scan + Cracking", "No WPS WiFi network selected")
                            else:
                                pin = wps_cracking(wps_wifi, wlan_device)
                                if pin != "":
                                    result = ["Target: " + wps_wifi["ssid"],"PIN: " + pin]
                                    utils.header("WPS Scan + Cracking", result)
                                else:
                                    utils.header("WPS Scan + Cracking", "No PIN attained")
                            utils.getch()
                        else:
                            utils.header("WPS Scan + Cracking", "This feature is indefinitely deprecated!")
                            utils.getch()
                    
                    elif choice == "5": #WIFI DOS
                        print("Test: " + str_choices[int(choice)-1])
                        wifi_dos(wlan_device)
                    else:
                        exit(1)
            elif choice == "2": #WPA CRACKING
                password = wpa_cracking(None)
                if password == None or password == "":
                    utils.header("WiFi Cracking", "No Password Cracked!")
                else:
                    utils.header("WiFi Cracking", "Cracked Password: " + password)
                utils.getch()
            elif choice == "6": #SELECT WLAN DEVICE
                wlan_device = interface.get_interface()
            elif choice == "7": #UTILITIES
                utilities()
            interface.disable_monitor(wlan_device)
    exit(0)

#Utilities
def utilities():
    utils.header("Utilities")
    int_mode = ["1","2","3","0"]
    str_mode = ["HashCat Capture File Conversion", "HashCat 3.6 Capture File Conversion", "WPA Cracking Benchmark", "Exit"]

    mode = ""
    while True:
        utils.header("Utilities")
        mode = utils.menu(int_mode, str_mode)
        if utils.valid_choice(mode, int_mode):
            break
    output = ""
    if mode == "1":
        utils.header("HashCat Capture File Conversion Result", "Output file: " + converters.cap_to_HS())
    elif mode == "2":
        utils.header("HashCat 3.6 Capture File Conversion Result", "Output file: " + converters.cap_to_HS3())
    elif mode == "3":
        benchmark.wpa_cracking_benchmark()
    utils.getch()

#Full Suite WPA
def fullsuite(wlan_device):
    if wlan_device == None or wlan_device == "":
        utils.header("WiFi WPA Full Suite", "No WLAN device found")
        utils.getch()
    else:
        capture = wpa_scan_capture(wlan_device)
        if capture == None:
            utils.header("WiFi WPA Full Suite", "No target WiFi selected")
        else:
            filename = capture[1]
            wifi = capture[0]
            password = wpa_cracking(filename, wifi)
            if password == None or password == "":
                utils.header("WiFi WPA Full Suite", "No Password Cracked!")
            else:
                utils.header("WiFi WPA Full Suite", "Cracked Password: " + password)
        utils.getch()

#WPA Cracking
def wpa_cracking(wifi:dict, filename=""):
    utils.header("WiFi Cracking (WPA)")
    if filename != "":
        return wpacracking.crack(filename, wifi)
    filename = input("Enter filename: ")
    if filename.strip() == "":
        return None
    return wpacracking.crack(filename, wifi)

#WPS Cracking
def wps_cracking(wifi:dict, wlan_device):
    password = wpscracking.crack(wifi, wlan_device)
    return password

#WPA Scan & Capture
def wpa_scan_capture(wlan_device):
    target = wpascan.get_target(wlan_device) #Find target WiFi network (via Scanning and Targetting)
    if target != None:
        return wpacapture.capture_handshake(wlan_device, target), target #Capture Handhake (includes Deauth if set)
    else:
        utils.header("WiFi WPA Scan + Capture","No target WiFi selected!")
        utils.getch()
        return None #Return captured filename

#WPS Scan
def wps_scan(wlan_device):
    return wpsscan.get_target(wlan_device)
    
#WiFi DOS
def wifi_dos(wlan_device):
    deauth.wifi_dos(wlan_device)
    utils.display_countdown("WiFi DOS (Deauth) Attack", "Stopping deauth attack...", 5)