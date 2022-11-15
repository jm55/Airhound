import re

def valid_mac(mac_address:str): #https://stackoverflow.com/a/7629690
    match = re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac_address.lower())
    if match != None:
        return True
    return False

mac_list = ["a","abc","123","10:63:C8:5F:57:11","", "98:B0:8B:33:8D:78"]

for m in mac_list:
    print(m, valid_mac(m))