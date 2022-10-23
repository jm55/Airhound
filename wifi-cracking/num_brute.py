import os

print("====PIN Brute====")
start = int(input("Enter start: "))
end = int(input("Enter end: "))
filename = input("Enter filename (include .txt): ")

def banner(progress):
	print("====PIN Brute====")
	print("Current " + str(start))
	print("End: " + str(end))
	print("Filename: " + str(filename))
	print("Progress: " + str(progress) + "%")

f = open(filename, "a")
while start <= end:
	os.system("clear")
	banner((start/end)*100)
	f.write(str(start)+ '\n')
	start += 1

print("Completed!")
