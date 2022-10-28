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
            1. WiFi Scanning
            2. WiFi Cracking
            3. WAP/Router Admin Control Access
============================================================
'''

from operator import mod
import sys
import os
import platform
import subprocess

title = "NSSECU2 Hacking Tool"
test = ["1","2","3"]
about_content = [   "==============================================================", 
                    "                NSSECU2 - Hacking Tool Project", 
                    "==============================================================",
                    "        Members: Escalona, Fadrigo, Fortiz, Manzano, Sy",
                    "        Topic: WiFi Hacking Tool", "        Description: The objective of this project is to ",
                    "                     create a packaged tool that will be ",
                    "                     able to do Wi-Fi scanning, cracking, ",
                    "                     and admin control access.", 
                    "        Objective Functionalities:",
                    "            1. WiFi Scanning",
                    "            2. WiFi Cracking", 
                    "            3. WAP/Router Admin Control Access",
                    "            4. WiFi DOS",
                    "            5. Windows Saved Passwords (if on Windows)",
                    "=============================================================="
                ]

def bar(len:str):
    b = ""
    for l in range(len):
        b += "="
    return b

def print_bar(len:str):
    b = bar(int(len))
    print(b)

def get_bar():
    return bar(20)

def titlebar(length:int):
    print_bar(length)
    print(title.center(length))
    print_bar(length)

def compile_about():
    return str("\n".join(map(str,about_content)))

def about():
    cls()
    print(compile_about())
    getch()
    cls()

def header(module:str, desc=None):
    cls()
    if module != None: #Module Name
        if desc != None: #Module Name & Description
            if len(module) < len(desc):
                titlebar(len(desc))
                print(module.center(len(desc)))
                print("")
                print(desc)
                print_bar(len(desc))
            elif len(title) < len(module) & len(module) > len(desc):
                titlebar(len(module))
                print(module.center(len(module)))
                print("")
                print(desc.center(len(module)))
                print_bar(len(module))
            else:
                titlebar(len(title))
                print(module.center(len(title)))
                print("")
                print(desc.center(len(title)))
                print_bar(len(title))
        else:
            if len(title) < len(module):
                titlebar(len(module))
                print(module.center(len(module)))
                print_bar(len(module))
            else:
                titlebar(len(title))
                print(module.center(len(title)))
                print_bar(len(title))

    else:
        titlebar(len(title))

def running_OS():
    return "You are running " + getOS()

def os_check(os:str):
    if(sys.platform == os):
        return True
    return False

def linux_check():
    return os_check("linux")

def win_check():
    return os_check("win32") or os_check("cygwin") or os_check("msys")

def confirm(message):
    header("CONFIRM",message)
    input("Press enter to continue...")

def getOS():
    return platform.system() + " " + platform.release()

def cls():
    if linux_check():
        os.system('clear')
    if win_check():
        os.system('cls')

def utf8_decode(data):
    return data.decode("utf-8").strip()

def root_check():
    whoami = subprocess.Popen("whoami", shell=True, stdout=subprocess.PIPE)
    cls()
    whoami.wait()
    data, err = whoami.communicate()
    if utf8_decode(data) != "root":
        return False
    return True

def getch(msg=""):
    if msg == "":
        input("Press Enter to continue...")
    else:
        input(msg)

def check_menu(int_choices:str, str_choices:list):
    if len(int_choices) == len(str_choices):
        return True
    return False

def menu(int_choices:str, str_choices:list):
    if not check_menu(int_choices, str_choices):
        print("Menu configuration mismatch! Exiting...")
        exit(1)
    ctr = 0
    for ctr in range(len(int_choices)):
        print(str(int_choices[ctr]) + " - " + str_choices[ctr])
    return input("Enter choice: ")

def valid_choice(choice, choices):
    for c in choices:
        if choice == c:
            return True
    return False

def longest_string(list):
    longest = ""
    for l in list:
        if len(longest) < l:
            longest = l
    return longest

def longest_string_len(list:list):
    return longest_string(list)