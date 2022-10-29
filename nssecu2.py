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
'''

import utils.utils as utils
import subdrivers.linux as lin
import subdrivers.windows as win

#Main Function
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

#T&C essentially.
def oath():
    invalid = True
    while invalid:
        oath = "I do solemnly swear that I am up to GOOD"
        return utils.yesNo("Oath",oath,"Do you agree to the terms?",True)

#Delegates Linux execution
def linux():
    if utils.root_check():
        lin.run()
    else:
        utils.header("SUDO REQUIRED","Application must run in root!")
        utils.getch("Press enter to exit...")
        exit(0)

#Delegates Windows execution
def windows():
    win.run()
    
if __name__ == "__main__":
    main()