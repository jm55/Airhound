'''
==============================
NSSECU2 - Hacking Tool Project
==============================
Members: Escalona, Fadrigo, Fortiz, Manzano, Sy
Topic: WiFi Hacking Tool
Description: The objective of this project is to create a packaged tool that will be able to do Wi-Fi scanning, cracking, and admin control access.
Objective Functionalities:
    1. WiFi Scanning
    2. WiFi Cracking
    3. WAP/Router Admin Control Access
'''

import utils.utils as utils
import linux as lin
import windows as win

def main():
    if not oath():
        exit(0)

    utils.about()

    if utils.linux_check():
        linux()
    elif utils.win_check():
        windows()
    else:
        print("OS not supported, exiting...")
        exit(0)

def oath():
    invalid = True
    while invalid:
        oath = "I do solemnly swear that I am up to GOOD"
        utils.header("Oath", oath)
        ans = input("Do you agree to the terms? (Y/N): ")
        if ans == 'Y' or ans == 'y':
            return True
        if ans == 'N' or ans == 'n':
            return False
        utils.cls()

def linux():
    if utils.root_check():
        lin.run()
    else:
        utils.titlebar()
        print("Application must run in root!")
        exit(0)

def windows():
    win.run()
    
if __name__ == "__main__":
    main()