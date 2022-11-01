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

WPA HANDSHAKE CAPTURE MODULE
'''

import subprocess
import utils.utils as utils
import interfaces.interfaces as interface
import deauth.deauth as deauth

global dos

def capture_handshake(device, bssid:str):
    utils.header("WPA Capture","Capture Handshake")
    
    #Use these device details however needed
    device_logicalname = interface.get_logicalname(device)
    device_macaddress = interface.get_macaddress(device)
    device_driver = interface.get_driver(device)
    '''
    =========================================================================
                                INSTRUCTIONS
    =========================================================================
    Do the airodump-ng command here where you capture the handshake 
    being transmitted over WiFi.

    You may also include a simultaneous deauth attack as you capture since
    capturing handshakes require hosts to do an attempt to connect to WiFi 
    but can be noticed by the victims as an anomaly during an attack, thus
    ask the user first before using deauth.

    After capture was done, save capture .pcap file and return filename/file.

    It is optional to turn it into a .hccapx file but .pcap file shall suffice
    '''

    return str(None)

#IMPLEMENT ANYTHING HERE ACCORDINGLY