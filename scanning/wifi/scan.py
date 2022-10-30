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
import re
import time
import utils.utils as utils
import interfaces.interfaces as interface

def get_target(device):
    utils.header("Scan","Scan and Select target WiFi network.")
    interface.print_device_summary(device)
    print("")
    utils.print_bar(len("Scan and Select target WiFi network."))

    wifi_list = scan_wifi(device)

    filtered_list = simplify_wifi_list(wifi_list) #Print and return filtered selection

    target_id = -1 #WiFi selector

    if len(wifi_list) == 0:
        utils.header("WiFi Results",["No WiFi Networks Found!","Can be attributed to ", 
                                    "Lack of WiFi networks available","or",
                                    "WLAN device incapable of monitor/injection mode."])
        utils.getch()
        return None
    else:
        invalid = True
        while invalid:
            utils.header("WiFi Scan Finished!")
            pretty_print(filtered_list)
            print("")
            try:
                target_id = int(input("Enter ID# of target WiFi network: "))
                invalid = False
            except ValueError:
                invalid = True

    return filtered_list[target_id-1]



def scan_wifi(device):
    service_status = True
    device_logicalname = interface.get_logicalname(device)
    device_macaddress = interface.get_macaddress(device)
    device_driver = interface.get_driver(device)
    wifi_list = []

    #Disable WLAN/Network Services
    while service_status:
        utils.header("Disabling possible interfering WLAN processes...")
        service_status = interface.terminate_services()
    utils.header("Possible interfering WLAN processes disabled!")
    utils.getch()
    
    #Ask for min time for scanning; Max at 60seconds
    valid = False
    countdown = -1
    min = 10
    max = 300
    while not valid:
        utils.header("WiFi Scan Time")
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
    command = "airodump-ng " + device_logicalname + " --update 1 --wps --encrypt wpa -w "  + filename + " -o csv" #checks for wpa-only and wps (whether 0 or non-0) and saves as csv

    #Execute command
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1)
    
    #Terminate at specified time; Does not indicate networks scanned.
    while countdown:
        utils.header("Scanning Network...", "Time Left: " + str(countdown) + " seconds")
        time.sleep(1)
        countdown -= 1
    process.kill()

    #Rename file to remove <filename>-xx.csv suffix
    #Show as "Loading..."
    utils.header("Loading results...")
    utils.renameFile(filename + "-01.csv ", filename + ".csv")
    if not utils.checkFile(filename + ".csv"):
        print("Error occured while loading file, exiting...")
        exit(1)

    #Print collected information
    wifi_list = utils.csvToList(filename)

    #Re-enable WLAN/Network Services
    while not service_status:
        utils.header("Re-enabling possibly killed WLAN processes...")
        service_status = interface.restart_services() and interface.check_connection()
    utils.header("WLAN/Network Services Restored!")
    utils.getch()

    #Return collected WiFi Networks
    return wifi_list

#Returns a slimmed down version of raw inputted wifi_list from post airodump WiFi Scan
def simplify_wifi_list(wifi_list: list):
    ctr = 2
    print("ID".ljust(4)+"MAC Address".ljust(21)+"SSID".ljust(36)+"Security".ljust(18)+"Cipher".ljust(21)+"Power (dBm)".ljust(13))
    filtered = []
    while ctr < len(wifi_list):
        wifi = wifi_list[ctr]
        # Important Cols:   0-BSSID, 3-Channel
        #                   5-Privacy, 6-Cipher
        #                   7-Authentication, 8-Power
        #                   13-ESSID
        if(len(wifi) == 0):
            break
        else:
            s_ctr = 0
            select = [str(ctr-1), wifi[0], wifi[13], wifi[5], wifi[6], wifi[8]] #BSSID, ESSID, Privacy, Cipher, Power
            select = {
                "id":str(ctr-1).strip(),
                "bssid": wifi[0].strip(),
                "essid": wifi[13].strip(),
                "privacy": wifi[5].strip(),
                "cipher": wifi[6].strip(),
                "power": wifi[8].strip()
            }
            filtered.append(select)
        ctr += 1
    return filtered

#Prints the filtered list accordingly
def pretty_print(filtered_list:list):
    print("ID".ljust(4)+"MAC Address".ljust(21)+"SSID".ljust(36)+"Security".ljust(18)+"Cipher".ljust(21)+"Power (dBm)".ljust(13))
    for wifi in filtered_list:
        print(wifi["id"].ljust(4)+ wifi["bssid"].ljust(21)+
            wifi["essid"].ljust(36)+ wifi["privacy"].ljust(18)+ 
            wifi["cipher"].ljust(21)+ wifi["power"].ljust(13)) 