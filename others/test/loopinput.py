import os

def cls():
	os.system("clear")

start = 0
end = 0
start_valid = False
end_valid = False
print("WPA Cracking (Bruteforce Attack)","Configuration")

while not start_valid:
	try:
		cls()
		print("WPA Cracking (Bruteforce Attack)","Configuration")
		start = int(input("Enter minimum number of characters: "))
		start_valid = True
	except ValueError:
		cls()

while not end_valid:
	try:
    		cls()
	    	print("WPA Cracking (Bruteforce Attack)","Configuration")
	    	end = int(input("Enter maximum number of characters: "))
	    	end_valid = True
	except ValueError:
		cls()
