import os
import subprocess
import json

def scan():
    #With help from https://stackoverflow.com/a/50303518
    lshw = subprocess.Popen("sudo lshw -class network -quiet -json", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lshw.wait()
    data, err = lshw.communicate()
    if lshw.returncode == 0:
        return data.decode("utf-8")
    else:  
        print("Error: " + err)

def cls():
    os.system('cls')

devices = json.loads(scan())
print("Scanning devices...")
print("Network devices: " + str(len(devices)))
ctr = 1
for d in devices:
    print(str(ctr) + ": " + d["logicalname"] + ", " + d["serial"] + ", " + d["configuration"]["driver"])
    ctr += 1