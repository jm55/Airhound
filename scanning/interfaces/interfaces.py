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
        "claimed": true,
        "handle": "PCI:0000:02:00.0",
        "description": "Wireless interface",
        "product": "QCA9377 802.11ac Wireless Network Adapter",
        "vendor": "Qualcomm Atheros",
        "physid": "0",
        "businfo": "pci@0000:02:00.0",
        "logicalname": "wlan0",
        "version": "31",
        "serial": "10:63:c8:5f:57:11",
        "width": 64,
        "clock": 33000000,
        "configuration": {
            "broadcast": "yes",
            "driver": "ath10k_pci",
            "driverversion": "5.19.0-kali2-amd64",
            "firmware": "WLAN.TF.2.1-00021-QCARMSWP-1",
            "ip": "192.168.2.252",
            "latency": "0",
            "link": "yes",
            "multicast": "yes",
            "wireless": "IEEE 802.11"
        },
        "capabilities": {
            "pm": "Power Management",
            "msi": "Message Signalled Interrupts",
            "pciexpress": "PCI Express",
            "bus_master": "bus mastering",
            "cap_list": "PCI capabilities listing",
            "ethernet": true,
            "physical": "Physical interface",
            "wireless": "Wireless-LAN"
        }
    }
]
'''

#Retrieves network devices using lshw shell command.
def scan():
    #With help from https://stackoverflow.com/a/50303518
    lshw = subprocess.Popen("sudo lshw -class network -quiet -json", shell=True, stdout=subprocess.PIPE)
    lshw.wait()
    data, err = lshw.communicate()
    if lshw.returncode == 0:
        return json.loads(data.decode("utf-8"))
    else:  
        print("Error: " + err)
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
    utils.header("Scanning WLAN devices...")
    wifi_devices = scan()
    if wifi_devices != None:
        invalid = True
        while invalid: #Assume user inputs as invalid
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
                utils.header("WARNING", "Please disconnect " + selected_device + "from its current network.")
                utils.getch()
                #To replace with something that checks if the device is really disconnected
                #Command to check: ifconfig $wlan_device | grep ip
                #If result is empty, then it is disconnected
                #Otherwise, it is still connected!
                return selected_device
            elif choice == choices[2]:
                utils.header("Scanning WLAN devices...")
                wifi_devices = scan()
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
    return get_key(device, "logicalname")

#Returns MAC Address of the device.
def get_macaddress(device):
    return get_key(device,"serial")

#Returns the driver/chipset of the device.
def get_driver(device):
    return get_key(device,"configuration")["driver"]

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