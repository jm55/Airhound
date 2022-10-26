'''
NSSECU2 - Hacking Tool Project
===============================================
Members: Escalona, Fadrigo, Fortiz, Manzano, Sy
Topic: WiFi Hacking Tool
Description: The objective of this project is to create a packaged tool that will be able to do Wi-Fi scanning, cracking, and admin control access.
Objective Functionalities:
    1. WiFi Scanning
    2. WiFi Cracking
    3. WAP/Router Admin Control Access
'''

from utils.utils import Utils as utils

def main():
    utils.titlebar()
    if linux_check():
        print("You are running Linux")
    elif win_check():
        print("You are running Windows")
        print("The program will run with limited features.")
    else:
        print("OS not supported, exiting...")
        

if __name__ == "__main__":
    main()