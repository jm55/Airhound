'''
==============================
NSSECU2 - Hacking Tool Project
==============================
Members: Escalona, Fadrigo, Fortiz, Manzano, Sy
Topic: WiFi Hacking Tool

Some part of the code was 
referenced from David Bombal's 
YT Tutorial (https://www.youtube.com/watch?v=SzYKzAHsdMg)

windows.py module
'''

import utils.utils as utils
import subprocess


def run():
    utils.cls()
    utils.titlebar()
    print("You are running Windows")
    print(utils.getOS())
    print("The program will run with limited features.")
    utils.bar()
    extract_wifi()

def extract_wifi():
