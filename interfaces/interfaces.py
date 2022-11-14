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

WLAN INTERFACE SEARCH MODULE
'''

import utils.utils as utils
import subprocess
import json

'''
Get list of wlan devices on machines and allow user to select 
lshw subprocess formatted as JSON, example are as follows:
[
    {
        "id": "network",
        "class": "network",
        ...
        "description": "Wireless interface",
        "product": "QCA9377 802.11ac Wireless Network Adapter",
        "vendor": "Qualcomm Atheros",
        ...
        "logicalname": "wlan0",
        ...
        "configuration": {
            "broadcast": "yes",
            "driver": "ath10k_pci",
            ...
        },
        "capabilities": {
            ...
        }
    }
]
'''

def refresh(device):
    if device == None:
        return None

    curr_logicalname = get_logicalname(device)
    if "mon" in curr_logicalname: #removing mon prefix for disabling process; should work regardless
        print(a[0:len(a)-3])
    '''
        Check if device logicalname changed after iwconfig subprocess to one with 'mon' suffix and update accordingly

        Process similar to scan

        But instead, do command: [sudo lshw -class network -quiet -json | grep <device_prefix>] 
        E.G. 
        Command: sudo lshw -class network -quiet -json | grep
        Output: "logicalname" : "wlan1",

        Trim the output however you want as long as it will extract the format 'wlan#mon' or 'wlan#' (depending on outcome)

        If result of command equals or contains the device prefix the update logicalname by doing: 
        device["logicalname"] = <some function/variable that trims the output cmd>
        
        Return device whether updated or not
    '''
    return device

#Retrieves network devices using lshw shell command.
def scan():
    #With help from https://stackoverflow.com/a/50303518
    lshw = subprocess.Popen("sudo lshw -class network -quiet -json", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lshw.wait()
    data, err = lshw.communicate()
    if lshw.returncode == 0:
        return json.loads(data.decode("utf-8"))
    else:  
        print("Error: " + str(err))
        return None

#Prints WLAN devices specified in devices parameter
def print_interfaces(devices):
    print("WLAN Device Count: " + str(len(devices)))
    print("")
    longest = 0
    ctr = 1
    print("ID".ljust(8) + "Logical Name".ljust(16) + "MAC Address".ljust(20) + "Chipset/Driver".ljust(10))     
    for d in devices:
        if(d["logicalname"].ljust(16)[0:4] == "wlan"): 
            content = str(ctr).ljust(8) + d["logicalname"].ljust(16) + d["serial"].ljust(20) + d["configuration"]["driver"].ljust(10)
            print(content)
            if len(content) > longest:
                longest = len(content)
            ctr += 1
    return longest

#Ask user for interface selection
#Returns JSON formatted choice of WLAN or None if none was selected (i.e., Exit)
def get_interface():
    requirement()
    utils.header("WLAN Device Selection","Scanning WLAN devices...")
    wifi_devices = scan()
    if wifi_devices != None:
        invalid = True
        while invalid: #Assume user inputs as invalid
            try:
                choices = ["1",str(len(wifi_devices)),str(len(wifi_devices)+1),"0"]
                utils.header("WLAN Device Selection", "Select WLAN Device")
                print_interfaces(wifi_devices)
                print("")
                print("Menu: ")
                print(choices[0] + " to " + choices[1] + " - Device ID")
                print(choices[2] + " - Refresh")
                print(choices[3] + " - Exit")
                choice = input("Enter choice: ")
                if choice == "":
                    print()
                elif choice == "0":
                    return None
                elif int(choice) >= 1 and int(choice) <= len(wifi_devices):
                    selected_device = wifi_devices[int(choice)-1]
                    utils.header("WARNING", "Please disconnect " + get_logicalname(selected_device) + " from its current network.")
                    utils.getch()
                    #To replace with something that checks if the device is really disconnected
                    #Command to check: ifconfig $wlan_device | grep ip
                    #If result is empty, then it is disconnected
                    #Otherwise, it is still connected!
                    return selected_device
                elif choice == choices[2]:
                    utils.header("Scanning WLAN devices...")
                    wifi_devices = scan()
            except ValueError:
                invalid = True
    else:
        utils.header("WLAN Device Selection", "No WLAN devices detected!")
        utils.getch()

#Return value from device using specified key
def get_key(device, key):
    if device != None:
        return device[key]
    return None

#Returns logical name of the device. Example: wlan0, wlan1, etc.
def get_logicalname(device):
    return str(get_key(device, "logicalname"))

#Returns MAC Address of the device.
def get_macaddress(device):
    return get_key(device,"serial")

#Returns the driver/chipset of the device.
def get_driver(device):
    if device != None:
        return get_key(device,"configuration")["driver"]
    return None
    
#Returns summary of the device given in [logicalname, macaddress, driver/chipset] format.
def get_device_summary(device):
    return [get_logicalname(device), get_macaddress(device), get_driver(device)]

#Prints the summary of the device given. Example below:
#WLAN Device Details
#WLAN Logicalname:   wlan1
#WLAN MAC Address:   c6:d7:e8:7e:c6:f1
#WLAN Driver:        mt7601u
def print_device_summary(device):
    print("WLAN Device Details")
    summary = get_device_summary(device)
    print("WLAN Logicalname: ".ljust(20) + summary[0])
    print("WLAN MAC Address: ".ljust(20) + summary[1])
    print("WLAN Driver: ".ljust(20) + summary[2])

#End possible interfering processes to WLAN device
def terminate_services():
    end_services = subprocess.Popen("sudo airmon-ng check kill", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    end_services.wait()
    res, err = end_services.communicate()
    if end_services.returncode == 0:
        return False #Service disabled successfully
    else:
        return True #Service not/partially disabled

#Restart (possible) terminated services from terminate_services()
def restart_services():
    commands =  [
                    "sudo systemctl start wpa_supplicant.service",
                    "sudo systemctl start NetworkManager.service"
                ]
    for c in commands:
        p = subprocess.Popen(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
        res, err = p.communicate()
        if p.returncode != 0:
            return False
    return True

#Enable monitor mode for specified device
def enable_monitor(device, channel=""):
    orig_logicalname = get_logicalname(device)
    if orig_logicalname == "":
        return False
    
    steps = ["ifconfig " + orig_logicalname + " down"]
    if channel != "":
        steps.append("iwconfig " + orig_logicalname + " mode monitor channel " + channel)
    else:
        steps.append("iwconfig " + orig_logicalname + " mode monitor")

    revised_device = refresh(device)
    if revised_device != None:
        device = revised_device

    steps.append("ifconfig " + orig_logicalname + " up")
    for s in steps:
        process = subprocess.Popen(s, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        process.wait()
        res, err = process.communicate()
        if process.returncode != 0:
            return False
     
    return True, device #Return updated device

#Disable monitor for specified device
def disable_monitor(device):
    logicalname = get_logicalname(device)
    if logicalname == "":
        return False

    steps = [
                "ifconfig " + logicalname + " down",
                "iwconfig " + logicalname + " mode managed"
                
            ]

    steps.append("ifconfig " + logicalname + " up")
    
    ''' DON'T OPEN JUST YET
    revised_device = refresh(device)
    if revised_device != None:
        device = revised_device
    '''

    for s in steps:
        process = subprocess.Popen(s, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        process.wait()
        res, err = process.communicate()
        if process.returncode != 0:
            return False

    return True, device #Return updated device

#Check if previous connections are restored
def check_connection():
    check = subprocess.Popen("ifconfig | grep wlan", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    check.wait()
    res, err = check.communicate()
    if res.decode("utf-8") == "":
        return False
    return True

def requirement():
    descs = [   "==== HARDWARE CAPABILITY REQUIREMENT ====",
                "\n",
                "The tool assumes and requires that you have the ",
                "certain WLAN chipsets in order to work.",
                "\n",
                "The WLAN devices you have must support monitoring/injection mode in order to work."
                "\n",
                "Refer to this link for more details: ",
                "https://deviwiki.com/wiki/List_of_Wireless_Adapters_That_Support_Monitor_Mode_and_Packet_Injection"
            ]
    utils.header("WLAN Device Selection", descs)
    utils.getch()