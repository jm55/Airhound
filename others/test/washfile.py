def parseWashOutput(filename):
    wps_list = []
    ctr = 0
    with open(filename) as file:
        while (line := file.readline().rstrip()):
            print(line.split())
            if ctr != 1:
                wps_list.append(line.split())
            ctr += 1
    return wps_list
    
output = parseWashOutput("wash.txt")
print(output)