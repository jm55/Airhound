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
            4. WiFi DOS
            5. Windows Saved WiFi Passwords
============================================================
'''

from operator import mod
import sys
import os
import platform
import subprocess
import json

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
                    "            5. Windows Saved WiFi Passwords (if on Windows)",
                    "=============================================================="
                ]

#Get a 'bar' of specified length
def bar(len:str):
    b = ""
    for l in range(len):
        b += "="
    return b

#Print bar of specified length
def print_bar(len:str):
    b = bar(int(len)+4)
    print(b)

#Get standard bar of length 20.
def get_bar():
    return bar(20)

#Get titlebar of specified length
def titlebar(length:int):
    print_bar(length)
    print(title.center(4+length))
    print_bar(length)

#Compile about list
def compile_about():
    return str("\n".join(map(str,about_content)))

#Print about page
def about():
    cls()
    print(compile_about())
    print("")
    getch()
    cls()

#Print header data
def header(module:str, desc=None):
    cls()
    if module != None: #Module Name
        if desc != None: #Module Name & Description
            if len(module) < len(desc):
                titlebar(len(desc))
                print(module.center(4+len(desc)))
                print("")
                print(desc.center(4+len(desc)))
                print_bar(len(desc))
            elif len(title) < len(module) & len(module) > len(desc):
                titlebar(len(module))
                print(module.center(4+len(module)))
                print("")
                print(desc.center(4+len(module)))
                print_bar(len(module))
            else:
                titlebar(len(title))
                print(module.center(4+len(title)))
                print("")
                print(desc.center(4+len(title)))
                print_bar(len(title))
        else:
            if len(title) < len(module):
                titlebar(len(module))
                print(module.center(4+len(module)))
                print_bar(len(module))
            else:
                titlebar(len(title))
                print(module.center(4+len(title)))
                print_bar(len(title))

    else:
        titlebar(len(title))
    print("")

#Get running OS
def running_OS():
    return "You are running " + getOS()

#Check if OS matches specified OS
def os_check(os:str):
    if(sys.platform == os):
        return True
    return False

#Check if running Linux
def linux_check():
    return os_check("linux")

#Check if running Windows
def win_check():
    return os_check("win32") or os_check("cygwin") or os_check("msys")

#Show confirm message and ask for getch()
def confirm(message):
    header("CONFIRM",message)
    getch()

#Get OS in str format
def getOS():
    return platform.system() + " " + platform.release()

#Execute cls/clear command
def cls():
    if linux_check():
        os.system('clear')
    if win_check():
        os.system('cls')

#Decode terminal/cmd output to UTF-8
def utf8_decode(data):
    return data.decode("utf-8").strip()

#Check if running as root
def root_check():
    whoami = subprocess.Popen("whoami", shell=True, stdout=subprocess.PIPE)
    cls()
    whoami.wait()
    data, err = whoami.communicate()
    if utf8_decode(data) != "root":
        return False
    return True

#Show 'Press Enter to continue"
#Add msg to specify message
def getch(msg=""):
    if msg == "":
        input("Press Enter to continue...")
    else:
        input(msg)

#Check menu selection alignement
def check_menu(int_choices:str, str_choices:list):
    if len(int_choices) == len(str_choices):
        return True
    return False

#Prints and asks user for choice based on choices
def menu(int_choices:str, str_choices:list):
    if not check_menu(int_choices, str_choices):
        print("Menu configuration mismatch! Exiting...")
        exit(1)
    ctr = 0
    for ctr in range(len(int_choices)):
        print(str(int_choices[ctr]) + " - " + str_choices[ctr])
    return input("Enter choice: ")

#Checks if choice is valid from choices
def valid_choice(choice, choices):
    for c in choices:
        if choice == c:
            return True
    return False

#Find longest string from list
def longest_string(list):
    longest = ""
    for l in list:
        if len(longest) < l:
            longest = l
    return longest

#Find and return length of longest string from list
def longest_string_len(list:list):
    return longest_string(list)

#Ask a Yes or No question
#module: Same as module in header()
#desc: Same as desc in header()
#question: Question to ask
#explicit: Strict Yes only, considers anything as No; Set False if loop question, set True if non-loop strict question
def yesNo(module:str, desc:str, question:str, explicit:bool):   
    while True:
        cls()
        header(module, desc)
        ans = input(question + " (Y/N): ")
        if ans == 'Y' or ans == 'y':
            return True
        elif ans == 'N' or ans == 'n':
            return False
        if not explicit:
            return False

#Print JSON in a prettified manner.
def printJSON(src):
    print(json.dump(src,indent=4))