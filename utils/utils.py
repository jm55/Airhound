import sys
import os
import platform
import subprocess

def bar():
    print("========================")

def titlebar():
        bar()
        print("  NSSECU2 Hacking Tool")
        bar()

def os_check(os):
    if(sys.platform == os):
        return True
    return False

def linux_check():
    return os_check("linux")

def win_check():
    return os_check("win32") or os_check("cygwin") or os_check("msys")

def getOS():
    return platform.system() + " " + platform.release()

def cls():
    if linux_check():
        os.system('clear')
    if win_check():
        os.system('cls')

def utf8_decode(data):
    return data.decode("utf-8").strip()

def root_check():
    whoami = subprocess.Popen("whoami", shell=True, stdout=subprocess.PIPE)
    cls()
    whoami.wait()
    data, err = whoami.communicate()
    if utf8_decode(data) != "root":
        return False
    return True