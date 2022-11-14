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

WINDOWS SUBDRIVER MODULE
'''

import utils.utils as utils
import subprocess
import re

#Saves collected WiFi credentials as .csv
def saveAsCSV(filename, wifi_list):
    if ".csv" not in filename:
        filename += ".csv"
    try:
        file = open(filename, 'w')
        file.write("SSID,Password,Security\n")
        for wifi in wifi_list:
            file.write(str(wifi["ssid"]) + "," + str(wifi["password"]) + "," + str(wifi["authentication"]+' '+wifi["cipher"]) + "\n")
        file.close()
        return filename
    except:
        return None

#Saves collected WiFi credentials as .txt
def saveAsTXT(filename, wifi_list):
    if ".txt" not in filename:
        filename += ".txt"
    try:
        file = open(filename, 'w')
        for wifi in wifi_list:
            file.write("SSID: " + str(wifi["ssid"]) + "\n")
            file.write("Password: " + str(wifi["password"]) + "\n")
            file.write("Security: " + str(wifi["authentication"]+' '+wifi["cipher"]) + "\n")
            file.write("\n")
        file.close()
        return filename
    except:
        return None

#Driver for Windows-based function; Serves as home menu
def run():
    utils.confirm(utils.running_OS())
    invalid = True
    while invalid:
        utils.header("Windows Easter Egg", "Extract Stored WiFi Credentials")
        print("Searching stored WiFi credentials...")
        wifi_list = extract_wifi()
        utils.header("Windows WiFi Credentials", "Extract Stored WiFi Credentials")
        print_wifi(wifi_list)
        int_choices = ["1","2","0"]
        str_choices = [ "Save as .csv",
                        "Save as .txt",
                        "Exit"]
        choice = utils.menu(int_choices, str_choices)
        if utils.valid_choice(choice, int_choices):
            if choice >= int_choices[0] and choice <= int_choices[1]:
                filename = input("Enter filename: ")
                if choice == int_choices[0]:
                    csv = saveAsCSV(filename, wifi_list)
                    print_wifi(wifi_list)
                    if csv != None:
                        print("File saving success!\nSaved as " + csv)
                    else:
                        print("Error occured while saving " + csv)
                elif choice == int_choices[1]:
                    txt = saveAsTXT(filename, wifi_list)
                    print_wifi(wifi_list)
                    if txt != None:
                        print("File saving success!\nSaved as " + txt)
                    else:
                        print("Error occured while saving " + txt)
                input("Press any key to continue...")
            elif choice == int_choices[2]:
                exit(0)

#Extract saved WiFi credentials from Windows using netsh command.
def extract_wifi():
    netsh = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()
    profiles = re.findall("All User Profile     : (.*)\r", netsh)
    wifi_list = []
    if len(profiles) != 0:
        for name in profiles:
            wifi = {}
            profile = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
            if re.search("Security key           : Absent", profile):
                continue
            else:
                wifi["ssid"] = name
                raw = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
                password = re.search("Key Content            : (.*)\r", raw)
                authentication = re.search("Authentication         : (.*)\r", raw)
                cipher = re.search("Cipher                 : (.*)\r", raw)
                if password == None:
                    wifi["password"] = None
                else:
                    wifi["password"] = password[1]
                if authentication == None:
                    wifi["authentication"] = None
                else:
                    wifi["authentication"] = authentication[1]
                if cipher == None:
                    wifi["cipher"] = None
                else:
                    wifi["cipher"] = cipher[1]
                wifi_list.append(wifi)
    return wifi_list

#Find longest value from dict
def longest(list, key):
    length = 0
    for l in list:
        if len(l[key]) > length:
            length = len(l[key])
    return length

#Find longest SSID from list
def longest_ssid(list):
    return longest(list, "ssid")

#Find longest password from list
def longest_password(list):
    return longest(list, "password")

#Find longest security config from list
def longest_secu(list):
    length = 0
    for l in list:
        if (len(l["authentication"])+len(l["cipher"])) > length:
            length = len(l["authentication"] + " " + l["cipher"])
    return length

#Print list of WiFi information
def print_wifi(list):
    if len(list) == 0 or list == None:
        print("WiFi list empty")
    else:
        long_ssid = longest_ssid(list) + 4
        long_pass = longest_password(list) + 4
        long_auth = longest_secu(list) + 4
        utils.header("Windows WiFi Credentials", "Extract Stored WiFi Credentials")
        utils.print_bar(long_ssid + long_pass + long_auth)
        print("SSID".ljust(long_ssid) + "Password".ljust(long_pass) + "Security")
        for wifi in list:
            print(str(wifi["ssid"]).ljust(long_ssid) + str(wifi["password"]).ljust(long_pass) + (wifi["authentication"]+' '+wifi["cipher"]))
        utils.print_bar(long_ssid + long_pass + long_auth)