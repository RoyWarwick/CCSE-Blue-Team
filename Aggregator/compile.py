import os
import time
from uuid import _ip_getnode as getmac

mac_raw = getmac()
mac_hex = str(hex(mac_raw))[2:]

while(len(mac_hex) < 12):
	mac_hex = '0' + mac_hex

mac_pos = 0
mac = ""

while(mac_pos < 12):
	if (mac_pos % 2 == 0):
		mac += mac_hex[mac_pos]
	else:
		mac+= mac_hex[mac_pos] + ':'
	mac_pos += 1

mac = mac[:-1]


os.system("mosquitto_sub -p 8883 --cafile ca.crt --cert server.crt --key server.key -h 192.168.0.2 -t 'agr/env_json' > tmp/all_env_json.txt &")

time.sleep(0.5)

alldata = open("tmp/all_env_json.txt", "r")

json_data = "["
id_list = []


while(True):
	nextline = alldata.readline()
	
	
	if (nextline == ""):
		#print("Nextline is blank")
		if(json_data != "["):
			os.system("mosquitto_pub -p 8883 -h 192.168.0.254 --cafile ca.crt --cert server.crt --key server.key -t 'fwd/aggr_env_in' -m \"" +mac + " " + json_data[:-2] + "]\"")
			#print(mac + " " + json_data[:-2] + "]")
			
			writefile = open("json_struct_sensor_" + str(sensor_id) + ".txt", "a")
			writefile.write(mac + " " + json_data[:-2] + "]") #write the json structure to the file
			writefile.close()
			
			
			
			id_list = []
			json_data = "["
		
		time.sleep(5)
	else:
		#print(nextline)
		sensor_id = ""
		pos = 0
		while (nextline[pos] != " "):
			sensor_id += nextline[pos]
			pos += 1
		
		if (sensor_id in id_list):
			os.system("mosquitto_pub -p 8883 -h 192.168.0.254 --cafile ca.crt --cert server.crt --key server.key -t 'fwd/aggr_env_in' -m \"" +mac + " " + json_data[:-2] + "]\"")
			#print(mac + " " + json_data[:-2] + "]")
			writefile = open("json_struct_sensor_" + str(sensor_id) + ".txt", "a")
			writefile.write(mac + " " + json_data[:-2] + "]") #write the json structure to the file
			writefile.close()
			
			id_list = []
			json_data = "[" + nextline[pos+1: -1] + ", "
		else:
			id_list.append(sensor_id)
			json_data += nextline[pos+1:-1] + ", "
			
alldata.close()
