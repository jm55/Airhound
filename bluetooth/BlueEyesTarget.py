import subprocess
import re
import math

class BlueEyesTarget:
    def __init__(self, name, addr):
        self.name = name
        self.addr = addr
        self.majorClasses = {
            "00000": "Miscellaneous",
            "00001": "Computer (Desktop, Notebook, PDA, Organizer)",
            "00010": "Phone (Cellular, Cordless, Pay Phone, Modem)",
            "00011": "LAN/Network Access Point",
            "00100": "Audio/Video (Headset, Speaker, Stereo, Video Display, VCR)",
            "00101": "Peripheral (Mouse, Joystick, Keyboard)",
            "00110": "Imaging (Printer, Scanner, Camera, Display)",
            "00111": "Wearable",
            "01000": "Toy",
            "01001": "Health",
            "11111": "Uncategorized"
        }
    
    def getName(self):
        return self.name
    
    def getAddr(self):
        return self.addr
    
    def setName(self, name):
        self.name = name 
    
    def setAddr(self, addr):
        self.addr = addr

    def clearAll(self):
        self.name = ""
        self.addr = ""
    
    def ping(self):
        address = self.getAddr()
        ping_command = "sudo l2ping -c 5 " + address

        p = subprocess.Popen(ping_command, stdout=subprocess.PIPE, shell=True)
        output = p.communicate()
        
        output_str = output[0].decode()
        print(output_str)

    def findClass(self, classID):
        IDBin = "{0:023b}".format(int(classID, 16))
        majorDevClassBits = IDBin[-13:-8]
        deviceClass = self.majorClasses[majorDevClassBits]

        return deviceClass
        
    def scanForClockAndClass(self):

        address = self.getAddr()
        addrFound = False
        i = 0

        p = subprocess.Popen("hcitool inq", stdout=subprocess.PIPE, shell=True)
        output = p.communicate()
        output_str = output[0].decode()
        devices = re.split(r'\n\t', output_str)
        devices.remove("Inquiring ...")
 
        while(not addrFound):
            if(address in devices[i]):
                inquiryResult = devices[i]
                addrFound = True
            i += 1

        if(not addrFound):
            print("ERROR: Cannot obtain the clock offset and class of target.")
        else:
            device_info = re.split(r'\t|\n', inquiryResult)
            classID = device_info[2].replace("class: ", "")
            deviceClass = self.findClass(classID)

            print("==========================================================")
            print("Clock offset and Device Class of " + device_info[0] + "\n")
            print("==========================================================")
            print(device_info[1])
            print(device_info[2] + " --" + deviceClass)

            print("\n")

            print("What is a clock offset?")
            print("""   ** The clock offset is the difference between the time a master (the one who initiates a connection) sends a packet and the time a slave (the one who listens for connections) receives it.
            This information is used by the slave to know when to change frequency to stay connected to the master.""")
            print("What is a class?")
            print("""   ** Each Bluetooth device has at most 24 bits for representing the 'Class of Device'. This is a binary value segemented into four areas: 
            Major Service Class (bits 24-13), Major Device Class (bits 12-8), Minor Device Class (bits 7-2), and a reserved header (bits 1-0).
            The class displayed here is the 'Major Device Class'""")

    def scanForServices(self):

        address = self.getAddr()
        ping_command = "sdptool browse " + address

        p = subprocess.Popen(ping_command, stdout=subprocess.PIPE, shell=True)
        output = p.communicate()
        output_str = output[0].decode()
        services_unfiltered = re.split(r'\n\n', output_str)
        services_filtered = []

        browsing_str = "Browsing " + address + " ..."

        for i in range(len(services_unfiltered)):

            if("Service Name: " in services_unfiltered[i]):
                record = services_unfiltered[i]
                if(browsing_str in record and "Service Search failed: Invalid argument" in record):
                    no_browsing = record.replace(browsing_str, "")
                    no_invalid = no_browsing.replace("Service Search failed: Invalid argument", "")
                    services_filtered.append(no_invalid)
                else:
                    services_filtered.append(record)

        print("==========================================================")
        print("SERVICES     |" + str(len(services_filtered)) + " found in " + address)
        print("==========================================================")
        for i in services_filtered:
            print(i)
            print("\n\n")
        
        print("What is Service Name?")
        print("""   ** The registered name of the service""")
        print("What is Service RecHandle?")
        print("""   ** A unique 32-bit value that identifies a service. """)
        print("What is Service Class ID List?")
        print("""   ** A list of all service classes that the service conforms to.""")
        print("What is Protocol Descriptor List?")
        print("""   ** A list of the communications protocol stacks that the service uses to function. The 'channel' displayed here
        refers which of the 79 channels (1MHz bandwidth each) Bluetooth uses to transmit packets.""")
        print("What is Profile Descriptor List?")
        print("""   ** A list of profile descriptors providing further information about the Bluetooth profile used by the service.
        The version number is also displayed here.""")
