import utils.utils as utils
import scanning.interfaces.interfaces as interfaces

def confirm():
    utils.cls()
    utils.titlebar()
    print("You are running Linux")
    print(utils.getOS())
    utils.bar()
    input("Press Enter to continue...")

def menu():
    invalid = True
    while invalid:
        utils.cls()
        utils.titlebar()
        utils.bar()
        print("          Menu")
        utils.bar()
        print("1 - WiFi Scan")
        print("2 - WiFi Cracking")
        print("3 - WAP Admin Attack")
        print("4 - Full Suite (1-3 in order)")
        print("0 - Exit")
        utils.bar()
        selection = int(input("Enter choice: "))
        if selection >= 0 and selection <= 4:
            return selection

def get_wifi_devices():
    interf = interfaces.get_interface()
    if interf == None:
        return None
    return interf 

def scan_wifi(interf):

def run():
    confirm()
    choice = menu()
    while choice != 0:
        if choice == 1:
            print("WiFi Scan")
        elif choice == 2:
            print("WiFi Cracking")
        elif choice == 3:
            print("WAP Admin Attack")
        elif choice == 4:
            print("Full Suite")
        choice = menu()
    exit(0)
