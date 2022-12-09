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
            6. Bluetooth Reconnaissance
============================================================
'''

import utils.utils as utils
import subdrivers.linux as lin
import subdrivers.windows as win

#Main Function
def main():
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
        if not oath():
            exit(0)
        lin.run()
    else:
        utils.header("SUDO REQUIRED","Application must run in root!")
        utils.getch("Press enter to exit...")
        exit(0)

#Delegates Windows execution
def windows():
    if not oath():
        exit(0)
    win.run()
    
if __name__ == "__main__":
    main()