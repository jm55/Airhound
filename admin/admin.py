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

WAP ADMIN CREDENTIAL ATTACK MODULE
'''

def scrape_credentials():
    credentials = None

    ip_addr = ""
    while True:
        utils.header("")
        ip_addr = input("Enter target IP address: ")
        if valid_ip(ip_addr):
            break

    '''
    DO HYDRA STUFF HERE
    '''

    return credentials

#IMPLEMENT OTHER METHODS HERE