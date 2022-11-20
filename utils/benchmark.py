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
============================================================

LINUX SUBDRIVER MODULE
'''

import utils.utils
import subprocess

def wpa_cracking_benchmark():
    score = "0"

    #INPUT
    while True:
        try:
            utils.header("WPA Cracking Benchmark (via Aircrack-ng CPU)","Allowed benchmark time: 15s to 300s")
            time = int(input("Enter benchmark time: "))
            break
        except ValueError:
            print()

    #PROCESS
    '''
    DO BENCHMARK HERE

    If time <15 set as 15
    If time >300 set as 300    

    Command: sudo aircrack-ng -S -Z <time>
    Output (Example): 4500 k/s
    
    Retrieve the last output via subprocess.communicate()
    '''
    if time < 15:
        time = 15
    elif time > 300:
        time = 300
    benchmark_process = subprocess.Popen("sudo aircrack-ng -S -Z " + str(time), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1) 
    benchmark_process.wait()
    res, err = benchmark_process.communicate()
    score_list = res.splitlines()
    score = score_list[-1].strip()
    #DISPLAY/OUTPUT
    utils.header("WPA Cracking Benchmark (via Aircrack-ng CPU)","Benchmark score: " + score)
    utils.getch()
    
    return score #not necessary, just here to mark end of method