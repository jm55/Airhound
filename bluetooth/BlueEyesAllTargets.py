class BlueEyesAllTargets:

    def __init__(self, dict):
        self.targetDict = dict

    def showTargets(self):
        print("ID   MAC Address         Name")
        print("==   ===========         ====")
        for i in range(len(self.targetDict)):
            device = self.targetDict[str(i)]
            print(device["id"] + "    " + device["macAddr"] + "   " + device["name"])
    
    def checkIfEntryExists(self, key):
        try:
            entry = self.targetDict[key]
            if(entry is not None):
                return True
        except KeyError:
            return False
    
    def getID(self, key):
        entry = self.targetDict[key]
        return entry["id"]
    
    def getName(self, key):
        entry = self.targetDict[key]
        return entry["name"]
    
    def getAddr(self, key):
        entry = self.targetDict[key]
        return entry["macAddr"]

    