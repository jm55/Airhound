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
                    "=============================================================="
                ]

def bar(len):
    b = ""
    for l in range(len):
        b += "="
    return b

def print_bar(len):
    b = bar(int(len))
    print(b)

def get_bar():
    return bar(20)

def titlebar(length):
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

def header(module, desc=""):
    cls()
    longest_desc = ""
    if type(desc) == isinstance(desc,list):
        for d in desc:
            if len(longest_desc) < d:
                longest_desc = d
    else:
        longest_desc = desc
    if module != None:
        if len(title) < len(module) or len(module) < len(longest_desc):
            if len(module) < len(longest_desc):
                titlebar(len(desc))
                print(module.center(len(longest_desc)))
                print("")
                print(desc)
                print_bar(len(longest_desc))
            else:
                titlebar(len(module))
                print(module.center(len(module)))
                print_bar(len(module))
        else:
            titlebar(len(title))
            print(module.center(len(title)))
            print_bar(len(title))
    else:
        titlebar()

def running_OS():
    return "You are running " + getOS()

def os_check(os):
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

def getch():
    input("Press Enter to continue...")