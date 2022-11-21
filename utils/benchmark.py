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

import time
import utils.utils as utils
import subprocess

def wpa_cracking_benchmark():
    score = "0"

    #INPUT
    while True:
        try:
            utils.header("WPA Cracking Benchmark (via Aircrack-ng CPU)","Allowed benchmark time: 15s to 300s")
            benchmark_time = int(input("Enter benchmark time: "))
            break
        except ValueError:
            print()

    #PROCESS
    if benchmark_time < 15:
        benchmark_time = 15
    elif benchmark_time > 300:
        benchmark_time = 300
        
    benchmark_process = subprocess.Popen("sudo aircrack-ng -S -Z " + str(benchmark_time), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1) 
    
    time_left = benchmark_time
    while time_left > 0:
        utils.header("Benchmarking...", str(time_left)+"s remaining")
        time.sleep(1)
        time_left -= 1
    
    benchmark_process.wait()
    
    res, err = benchmark_process.communicate()
    score_list = res.splitlines()
    score = score_list[-1].strip()
    
    return score #not necessary, just here to mark end of method
