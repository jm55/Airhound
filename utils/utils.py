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

UTILITIES MODULE
'''

from datetime import datetime as dt
import sys
import os
import platform
import subprocess
import json
import csv
import re
import time
import ipaddress

title = "NSSECU2 Hacking Tool"
test = ["1","2","3"]
about_content = [   "==============================================================", 
                    "                NSSECU2 - Hacking Tool Project", 
                    "==============================================================",
                    "      Members: Escalona, Fadrigo, Fortiz, Manzano, Sy".ljust(62),
                    "      Topic: WiFi Hacking Tool".ljust(62), 
                    "      Description: The objective of this project is to ".ljust(62),
                    "                   create a packaged tool that will be ".ljust(62),
                    "                   able to do Wi-Fi scanning, cracking, ".ljust(62),
                    "                   and admin control access.".ljust(62), 
                    "      Objective Functionalities:".ljust(62),
                    "         1. WPA Scanning & Handshake Capture".ljust(62),
                    "         2. WPA Cracking", 
                    "         3. WiFi DOS".ljust(62),
                    "         4. Other Tools".ljust(62),
                    "         5. Windows Saved WiFi Passwords (if on Windows)".ljust(62),
                    "=============================================================="
                ]

#Get a 'bar' of specified length
def bar(len:str):
    b = ""
    for l in range(len):
        b += "="
    return b

#Print bar of specified length
def print_bar(len:str):
    b = bar(int(len)+12)
    print(b)

#Get standard bar of length 20.
def get_bar():
    return bar(20)

#Get titlebar of specified length
def titlebar(length:int):
    print_bar(length)
    print(title.center(12+length))
    print_bar(length)

#Compile about list
def compile_about():
    return str("\n".join(map(str,about_content)))

#Print about page
def about():
    cls()
    print(compile_about())
    print("")
    getch()
    cls()

#Prints actual header with description
def print_header(module:str, desc, longest:int):
    titlebar(longest)
    print(module.center(longest+12))
    print("")
    if type(desc) == list:
        for d in desc:
            print(d.center(longest+12))
    else:
        print(desc.center(longest+12))
    print_bar(longest)

#Print header controller
def header(module:str, desc=None):
    cls()
    if module != None: #Module Name
        if desc != None: #Module Name & Description
            if type(desc) == list:
                longest = len(title)
                if longest < len(module):
                    longest = len(module)
                for d in desc:
                    if longest < len(d):
                        longest = len(d)
                print_header(module, desc, longest)
            else:
                if len(module) < len(desc):
                    print_header(module, desc, len(desc))
                elif len(title) < len(module) & len(module) > len(desc):
                    print_header(module, desc, len(module))
                else:
                    print_header(module, desc, len(title))
        else:
            if len(title) < len(module):
                titlebar(len(module))
                print(module.center(12+len(module)))
                print_bar(len(module))
            else:
                titlebar(len(title))
                print(module.center(12+len(title)))
                print_bar(len(title))
    else:
        titlebar(len(title))
    print("")

#Get running OS
def running_OS():
    return "You are running " + getOS()

#Check if OS matches specified OS
def os_check(os:str):
    if(sys.platform == os):
        return True
    return False

#Check if running Linux
def linux_check():
    return os_check("linux")

#Check if running Windows
def win_check():
    return os_check("win32") or os_check("cygwin") or os_check("msys")

#Show confirm message and ask for getch()
def confirm(message):
    header("CONFIRM", message)
    getch()

#Get OS in str format
def getOS():
    return platform.system() + " " + platform.release()

#Execute cls/clear command
def cls():
    if linux_check():
        os.system('clear')
    if win_check():
        os.system('cls')

#Decode terminal/cmd output to UTF-8
def utf8_decode(data):
    return data.decode("utf-8").strip()

#Check if running as root
def root_check():
    whoami = subprocess.Popen("whoami", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    cls()
    whoami.wait()
    data, err = whoami.communicate()
    if utf8_decode(data) != "root":
        return False
    return True

#Show 'Press Enter to continue"
#Add msg to specify message
def getch(msg=""):
    try:
        if msg == "":
            input("Press Enter to continue...")
        else:
            input(msg)
    except EOFError as e:
        print(e)

#Check menu selection alignement
def check_menu(int_choices:str, str_choices:list):
    if len(int_choices) == len(str_choices):
        return True
    return False

#Prints and asks user for choice based on choices
def menu(int_choices:str, str_choices:list):
    if not check_menu(int_choices, str_choices):
        print("Menu configuration mismatch! Exiting...")
        exit(1)
    ctr = 0
    for ctr in range(len(int_choices)):
        print(str(int_choices[ctr]) + " - " + str_choices[ctr])
    print("")
    choice = ""
    try:
        choice = input("Enter choice: ")
    except EOFError as e:
        print(e)
    return choice

#Checks if choice is valid from choices
def valid_choice(choice:str, choices:list):
    for c in choices:
        if choice == str(c):
            return True
    return False

#Find longest string from list
def longest_string(list):
    longest = ""
    for l in list:
        if len(longest) < l:
            longest = l
    return longest

#Find and return length of longest string from list
def longest_string_len(list:list):
    return longest_string(list)

#Ask a Yes or No question
#module: Same as module in header()
#desc: Same as desc in header()
#question: Question to ask
#explicit: Strict Yes only, considers anything as No; Set False if loop question, set True if non-loop strict question
def yesNo(module:str, desc:str, question:str, explicit:bool):   
    while True:
        cls()
        header(module, desc)
        ans = input(question + " (Y/N): ")
        if ans == 'Y' or ans == 'y':
            return True
        elif ans == 'N' or ans == 'n':
            return False
        if not explicit:
            return False

#Print JSON in a prettified manner.
def printJSON(src):
    print(json.dump(src,indent=4))

#Get raw now datetime
def getDT():
    return dt.now()

#Get formatted now datetime as yyyy-mm-dd-hh-mm-ss
def getFormattedDT():
    return str(getDT().strftime("%Y-%m-%d-%H-%M-%S"))

#CSV to 2D list; Generic, can be used on all csv to 2D list conversions
def csvToList(filepath:str):
    try:
        loc = filepath.rindex(".csv")
        if len(filepath)-loc != 4:
            return []
    except ValueError:
        filepath += ".csv"
    
    if not checkFile(filepath):
        return []

    f = open(filepath, "r")
    
    return list(csv.reader(f))

def checkFile(filepath:str):
    if os.path.exists(filepath):
        return True
    else:
        return False

def renameFile(src:str, dst:str):
    rn = subprocess.run("mv " + src + " " + dst, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def parseWashOutput(filename):
    wps_list = []
    ctr = 0
    with open(filename) as file:
        while (line := file.readline().rstrip()):
            if ctr != 1:
                wps_list.append(line.split())
            ctr += 1
    return wps_list

#Returns a slimmed down version of raw inputted wifi_list from post airodump WiFi Scan
def simplify_wifi_list(wifi_list: list, wps:False):
    filtered = []
    if wps:
        #Format: [['BSSID', 'Ch', 'dBm', 'WPS', 'Lck', 'Vendor', 'ESSID']]
        ctr = 1
        while ctr < len(wifi_list):
            wifi = wifi_list[ctr]
            # Important Cols:   0-BSSID, 1-Channel
            #                   2-Power, 6-ESSID
            if(len(wifi) == 0):
                break
            else:
                select = {
                    "id":str(ctr).strip(),
                    "bssid": wifi[0].strip(),
                    "essid": wifi[6].strip(),
                    "power": wifi[2].strip(),
                    "channel": wifi[1].strip()
                }
                filtered.append(select)
            ctr += 1
    else:
        ctr = 2
        print("ID".ljust(4)+"MAC Address".ljust(21)+"SSID".ljust(36)+"Security".ljust(18)+"Cipher".ljust(21)+"Power (dBm)".ljust(13))
        while ctr < len(wifi_list):
            wifi = wifi_list[ctr]
            # Important Cols:   0-BSSID, 3-Channel
            #                   5-Privacy, 6-Cipher
            #                   7-Authentication, 8-Power
            #                   13-ESSID
            if(len(wifi) == 0):
                break
            else:
                select = {
                    "id":str(ctr-1).strip(),
                    "bssid": wifi[0].strip(),
                    "essid": wifi[13].strip(),
                    "privacy": wifi[5].strip(),
                    "cipher": wifi[6].strip(),
                    "power": wifi[8].strip(),
                    "channel": wifi[3].strip()
                }
                filtered.append(select)
            ctr += 1
    return filtered

def valid_mac(mac_address:str): #https://stackoverflow.com/a/7629690
    match = re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac_address.lower())
    if match != None:
        return True
    return False

def valid_ip(ip_str):
    try:
        ipaddress.ip(ip_str)
        return True
    except ValueError:
        return False

def set_countdown(str_header, min, max):
    valid = False
    countdown = -1
    while not valid:
        header(str_header)
        try:
            entry = int(input("Enter time (sec) to scan (limited " + str(min) + "s to " + str(max) + "s): "))
            if entry >= min and entry < max:
                countdown = entry
                valid = True
            elif entry > max:
                header(str_header ,"Time entered exceeds max limit!","Time set to " + str(max) + " seconds.")
                countdown = max
                valid = True
            elif entry < min:
                header(str_header, "Invalid time, please try again!")
                getch()
        except ValueError:
            valid = False
    return countdown

def display_countdown(str_header, desc, countdown):
    while countdown:
        desc_list = []
        time_left = "Time left: " + str(countdown) + " second(s)"
        if type(desc) == list:
            desc_list = desc
            desc_list.append(time_left)
        else:
            desc_list = [desc, time_left]
        header(str_header, desc_list)
        time.sleep(1)
        countdown -= 1

def find_iterations(charset, min, max):
    iterations = 0
    if min == max:
        return pow(len(charset),min)
    while min <= max:
        iterations += pow(len(charset),min)
        min += 1
    return iterations

def dependency_list():
    return ["iwconfig", "ifconfig", "lshw", "aircrack-ng", "airodump-ng", "cowpatty", "crunch", "reaver", "wash"]

#@TODO Dependency Application Checking
def find_dependencies():
    '''
    Scan the Linux machine of the necessary applications that should be 
    installed prior to the launch of the tool. 
    This will be used on the startup part of the Linux subdriver.

    Create a function (with no parameters required) that will scan for installed tools on the system. 
    Refer to dependency_list() for the list of tools required.
    
    Simply return true if all the listed programs are found and return false if otherwise.
    '''
    # ls and grep command for checking packages in /usr/bin/
    ls_bin_cmd = "ls /usr/bin/" + " | " + "grep -E lshw\|aircrack-ng\|cowpatty\|crunch\|reaver\|wash"
    ls_bin_process = subprocess.Popen(ls_bin_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    res, err = ls_bin_process.communicate()
    bin_list = str(res.decode("utf-8")+"").split()

    # ls and grep command for checking packages in /usr/sbin/
    ls_sbin_cmd = "ls /usr/sbin/" + " | " + "grep -E " + "ifconfig\|iwconfig\|airodump-ng\|aireplay-ng"
    ls_sbin_process = subprocess.Popen(ls_sbin_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    res, err = ls_sbin_process.communicate()
    sbin_list = str(res.decode("utf-8")+"").split("\n")

    # combined list of existing packages
    exist_list = bin_list + sbin_list

    # generated list of required dependencies
    req_list = dependency_list()
    
    # list for missing dependencies
    miss_list = []

    for req in req_list:
        if req not in exist_list:
            miss_list.append(req)
    
    if len(miss_list) > 0:
        return miss_list

    return None #No missing dependencies