'''
LIST AND ALLOW USER TO SELECT INTERFACE TO USE
'''
import utils.utils as utils
import subprocess
import json

def __scan():
    #With help from https://stackoverflow.com/a/50303518
    lshw = subprocess.Popen("sudo lshw -class network -quiet -json", shell=True, stdout=subprocess.PIPE)
    lshw.wait()
    data, err = lshw.communicate()
    if lshw.returncode == 0:
        return json.loads(data.decode("utf-8"))
    else:  
        print("Error: " + err)
        return None

def __print_interface(devices):
    print("Network devices: " + str(len(devices)))
    ctr = 1
    for d in devices:
        print(str(ctr) + ": " + d["logicalname"] + ", " + d["serial"] + ", " + d["configuration"]["driver"])
        ctr += 1
    return ctr

def get_interface():
    devices = __scan()
    if devices != None:
        invalid = True
        while invalid:
            utils.cls()
            utils.titlebar()
            devices = __scan()
            __print_interface(devices)
            utils.bar()
            choices = [1,len(devices), len(devices)+1, 0]
            print("Menu\nSelect Devices: 1-" + str(choices[1])+ "\nRefresh: " + str(choices[2]) + "\nExit: 0")
            utils.bar()
            choice = int(input("Enter choice: "))
            if choice >= choices[0] and choice <= choices[1]: #Choose devices 
                return devices[choice-1]
            elif choice == choices[3]: #Exit
                return None
            #The else is considered as a refresh
    else:
        print("devices None!")