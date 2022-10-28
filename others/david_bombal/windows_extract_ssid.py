#! py
######################################
#Copyright of David Bombal, 2021     #
#https://www.davidbombal.com         #
#https://www.youtube.com/davidbombal #
######################################

import subprocess 
import re

command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()

profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

wifi_list = []

if len(profile_names) != 0:
    for name in profile_names:
        wifi = {}
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            wifi["ssid"] = name
            raw = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
            password = re.search("Key Content            : (.*)\r", raw)
            authentication = re.search("Authentication            : (.*)\r", raw)
            cipher = re.search("Cipher            : (.*)\r", raw)
            if password == None:
                wifi["password"] = None
            else:
                wifi["password"] = password[1]
            if authentication == None:
                wifi['authentication'] = None
            else:
                wifi['authentication'] = authentication[1]
            if cipher == None:
                wifi['cipher'] = None
            else:
                wifi['cipher'] = cipher[1]
            wifi_list.append(wifi) 
        print(wifi)

for x in range(len(wifi_list)):
    print(wifi_list[x]) 