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

BLUETOOTH MODULE
'''

import utils.utils as utils
import subprocess
import re
import bluetooth.BlueEyesAllTargets as BlueEyesAllTargets
import bluetooth.BlueEyesTarget as BlueEyesTarget
import sys

def printBanner():
    utils.cls()
    print("===========================================")
    print('\033[0;34m' + "  ____  _            ______                ")
    print(" |  _ \| |          |  ____|               ")
    print(" | |_) | |_   _  ___| |__  _   _  ___  ___ ")
    print(" |  _ <| | | | |/ _ \  __|| | | |/ _ \/ __|")
    print(" | | ) | | |_| |  __/ |___| |_| |  __/\__ |")
    print(" |____/|_|\__,_|\___|______\__, |\___||___/")
    print("                            __/ |          ")
    print("                           |___/           " + '\033[0m')
    print("===========================================") 
    print(" 0 - Basics of Bluetooth Technology      -- learn the fundamentals of Bluetooth technology before you get started")
    print(" 1 - Check Bluetooth Service Status      -- check if Bluetooth is currently running in Kali")
    print(" 2 - Start Bluetooth Service             -- activate Bluetooth in Kali; needed for your adapter to be recognized")
    print(" 3 - Check My Bluetooth Device           -- display information about your Kali's active Bluetooth adapter")
    print(" 4 - Check All Bluetooth Devices         -- display information about all Bluetooth adapters in your machine, whether virtual or not")
    print(" 5 - Start BlueEyes                      -- access the main BlueEyes features")
    print(" 6 - Exit                                -- does this really need to be explained?")

def printBTBasics():
    print("** All information was paraphrased from hackers-arise.com**")
    print("**READ MORE: https://www.hackers-arise.com/post/bluetooth-hacking-part-1-getting-started-with-bluetooth **")
    print("Bluetooth Basics")
    print("""       Bluetooth is a universal protocl that operates at 2.4 - 2.485 GHz. It works at a minimum of 10 meters with theoretically no limit (range is device-dependent).
    Two Bluetooth-capable devices connect by pairing with each other. When pairing, the devices exchange names, classes, lists of services, and other technical information.
    Additionally, they exchange a pre-shared key to be able to identify each other in the future. Every Bluetooth device can be identified with its MAC address, which is
    is comprised of 48-bits worth of hexadecimal values (a portion of which is tied to a manufacturer name).""")

def checkBTService():
    p = subprocess.Popen('service --status-all | grep bluetooth', stdout=subprocess.PIPE, shell=True)
    output = p.communicate()
    output_str = output[0].decode()

    if(output_str.find("+") == -1):
        print("Bluetooth service is INACTIVE. Enter '2' to start the Bluetooth service.")
        return False
    else:
        print("Bluetooth service is ACTIVE.")
        return True

def startBTService():
    endLoop = False

    p = subprocess.Popen('service --status-all | grep bluetooth', stdout=subprocess.PIPE, shell=True)
    output = p.communicate()
    output_str = output[0].decode()

    if(output_str.find("+") == -1):
        print("** If you are not a root user, you need to enter your password to start the Bluetooth service.")
        print("** And by the way, you're never going to see your password as you type it on the terminal. Sorry, it's a Linux thing")

        while(not endLoop):
            p = subprocess.Popen("sudo service bluetooth start", stdout=subprocess.PIPE, shell=True)
            output = p.communicate()
            
            if(output[0].decode() == ''):
                endLoop = True
    
        p = subprocess.Popen('service --status-all | grep bluetooth', stdout=subprocess.PIPE, shell=True)
        output = p.communicate()

        print('Bluetooth service has been started.')
        print("\nCurrent Bluetooth Status: ")
        print("--------------------------")
        print(output[0].decode() + " ** having a [ + ] means that the service is up and running")
    else:
        print('Bluetooth service is already running,  no need to restart the service.')

def checkMyBT():
    p = subprocess.Popen("hcitool dev", stdout=subprocess.PIPE, shell=True)
    output = p.communicate()
    output_str = output[0].decode()

    if(output_str == ''):
        print("No Bluetooth devices connected. Connect a (compatible) Bluetooth adapter to your Kali machine to get started.")
        print("     ** If you are using a virtual Kali machine, ensure that the adapter is connected to the VM and not your main machine.")
        print("     ** After connecting your Bluetooth adapter, enter '2' to activate the Bluetooth service if you have not done so already.")
        return False
    else:
        my_interface = re.split(r'\n\t|\t|\n', output_str)
        print("Currently Used Bluetooth Interface: " + my_interface[1])
        print("     MAC Address: " + my_interface[2])
        return True

def checkBTDevices():
    p = subprocess.Popen("hciconfig", stdout=subprocess.PIPE, shell=True)
    output = p.communicate()
    output_str = output[0].decode()

    if(output_str == ''):
        print("No Bluetooth devices connected. Connect a (compatible) Bluetooth adapter to your Kali machine to get started.")
        print("     ** If you are using a virtual Kali machine, ensure that the adapter is connected to the VM and not your main machine.")
        print("     ** After connecting your Bluetooth adapter, enter '2' to activate the Bluetooth service if you have not done so already.")
    else:
        interfaces = output_str.split("\n\n")
        for i in range(0, len(interfaces)-1):
            interface_str = interfaces[i]
            interface_info = interface_str.split("\n\t")
            print("Interface Name: " + (interface_info[0])[0:4])
            print("     MAC Address: " + (interface_info[1])[12:(interface_info[1]).find("ACL")])
            print("     Status: " + interface_info[2])

def scanForDevices():
    p = subprocess.Popen("hcitool scan", stdout=subprocess.PIPE, shell=True)

    output = p.communicate()
    output_str = output[0].decode()
    
    if(output_str == "Scanning ...\n"):
        devices_list = []
    else:
        devices_list = output_str.split("\n\t")
        devices_list.remove("Scanning ...")

    return devices_list


def createTargetDict(scanned_devices):

    targetDict = {}

    for i in range(len(scanned_devices)):    
        device_info = re.split(r'\t|\n', scanned_devices[i])
        device_info_dict = dict(id = str(i), macAddr = device_info[0], name = device_info[1])
        targetDict[str(i)] = device_info_dict
    
    return targetDict

def commands(devices_list):

    endLoop = False

    targetDict = createTargetDict(devices_list)
    targets = BlueEyesAllTargets.BlueEyesAllTargets(targetDict)

    print("\nTarget List: ")
    targets.showTargets()

    print("\n")

    print("Commands: ")
    print("     ** set TARGET <id>      -- select the Bluetooth device you want to scan and enumerate via its assigned ID number")
    print("             i.e., set TARGET 0, set target 1")
    print("     ** unset TARGET         -- unselect the current target")
    print("     ** show ALL             -- show the target list")
    print("     ** show TARGET          -- show the currently selected target")
    print("     ** ping                 -- ping the currently selected target to see if they are in reach")
    print("     ** scan                 -- begin the scanning process; scans for clock offset, device class, and services")
    print("     ** scan -o <filename>   -- same as 'scan' but saves the results in a textfile with a filename of your choice. No need to append '.txt'.")
    print("             i.e., scan -o scan_results")
    print("     ** exit                 -- close the scanner and go back to the main menu\n")
    print("Note: the commands are NOT case-sensitive but you must strictly follow the syntax\n")
        
    target = BlueEyesTarget.BlueEyesTarget("", "")

    while(not endLoop):
        command = input('\033[0;34m' + 'BlueEyes/startBlueEyes >> ' + '\033[0m')
        command_lower = command.lower()
        command_words = (command_lower.strip()).split(" ")

        if(command_words[0] == "set" and command_words[1] == "target"):
            if(len(command_words) < 3 or len(command_words) > 4):
                print("ERROR: Incorrect syntax for 'set target <id>' command.")
            else:
                ID = command_words[2]
                validity = targets.checkIfEntryExists(ID)
                if(validity):
                    target.setName(targets.getName(ID))
                    target.setAddr(targets.getAddr(ID))
                    print("Target set to " + ID)
                    print("     Name: " + target.getName())
                    print("     MAC Address: " + target.getAddr())
                else:
                    print("ERROR: ID does not exist in the target list.")

        elif(command_words[0] == "unset" and command_words[1] == "target"):

            target_name = target.getName()
            target_addr = target.getAddr()
            if(target_name == "" and target_addr == ""):
                print("ERROR: No target has been selected yet.")
            else:
                target.clearAll()
                print("Current target has been deselcted. You may now set a new one.")

        elif(command_words[0] == "show" and command_words[1] == "all"):

            targets.showTargets()

        elif(command_words[0] == "show" and command_words[1] == "target"):

            target_name = target.getName()
            target_addr = target.getAddr()
            if(target_name == "" and target_addr == ""):
                print("ERROR: No target has been selected yet.")
            else:
                print("Current target: ")
                print("     Name: " + target_name)
                print("     MAC Address: " + target_addr)

        elif(command_words[0] == "ping"):

            target_name = target.getName()
            target_addr = target.getAddr()
            if(target_name == "" and target_addr == ""):
                print("ERROR: No target has been selected yet.")
            else:
                target.ping()
        
        elif(command_words[0] == "scan"):

            target_name = target.getName()
            target_addr = target.getAddr()

            if(target_name == "" and target_addr == ""):
                print("ERROR: No target has been selected yet.")
            else:
                if(len(command_words) == 3):
                    if(command_words[1] == "-o"):
                        file_name = command_words[2] + ".txt"
                        print("Scanning ...")
                        restore_IO = sys.stdout
                        sys.stdout = open(file_name, "w")
                        target.scanForClockAndClass()
                        target.scanForServices()
                        sys.stdout = restore_IO
                        print("Scan completed! Saved results can be viewed in " + file_name + ".txt")
                    else:
                        print("ERROR: Incorrect syntax for 'scan -o <filename>' command.")
                elif(len(command_words) == 2):
                    if(command_words[1] == "-o"):
                        print("ERROR: No filename has been inputted.")
                    else:
                        print("ERROR: Incorrect syntax for 'scan -o <filename>' command.")
                elif(len(command_words) == 1):
                    print("Scanning ...")
                    target.scanForClockAndClass()
                    target.scanForServices()
                    print("Scan completed!")
                else:
                    print("ERROR: Invalid input.")

        elif(command_words[0] == "exit"):
            printBanner()
            endLoop = True
        else:
            print("ERROR: Invalid input.")

def startBlueEyes():

    print("Starting BlueEyes ...")
    adapterConnected = checkMyBT()
    serviceOn = checkBTService()

    if(adapterConnected):
        if(serviceOn):
            devices_list = scanForDevices()
            if(len(devices_list) == 0):
                print("No Bluetooth devices have been detected within range.")
            else:
                
                commands(devices_list)
        else:
            print("---")
    else:
        print("---")

def bt_driver():
    #test() REMOVE THIS ONCE bt_driver() HAS OFFICIAL CODE
    #Execute/Call functions here
    printBanner()
    endLoop = False

    try:
        while(not endLoop):
            choice = input('\033[0;34m' + 'BlueEyes >> ' + '\033[0m')
            if(choice == '0'):
                printBTBasics()
            elif(choice == '1'):
                checkBTService()
            elif(choice == '2'):
                startBTService()
            elif(choice == '3'):
                checkMyBT()
            elif(choice == '4'):
                checkBTDevices()
            elif(choice == '5'):
                startBlueEyes()
            elif(choice == '6'):
                print("Exiting ...")
                return None
            else:
                print("ERROR: Invalid input.")
    except KeyboardInterrupt:
        print("Exiting ...")
        return None
    
def test():
    utils.header("Bluetooth Module")
    utils.getch()