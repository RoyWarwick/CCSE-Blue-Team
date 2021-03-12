import time
import sys
import os
import random
import string
from datetime import datetime


#There will be an open mosquitto subscriber for the topic associated with the sensor id (agr/phys_sensor_<sensor_id>)
#this subscriber will output to the file ./tmp/phys_sensor_<sensor_id>

sensor_id = int(sys.argv[1]) #read in the id for this sensor from the command line
file_name = "./tmp/phys_sensor_"+str(sensor_id) #use this id to specify the file to look for data

data_in = open(file_name, "r") #open the file ready for reading
nextline = "" #set aside variable for data to be written into
incoming = [] #set aside varible for incoming second-stage random numbers to be written into
legacyline = "" #set aside variable for keeping data when transitioning from establishing a connection to reading data


while(nextline == ""): #while there is no data available within the file (the sensors have not yet connected) 
	nextline = data_in.readline() #read in the next line of data
	time.sleep(1) #wait for connections
	

incoming.append(nextline) #add the first input to the array

while(nextline == ""): #while there is still data to be read from the sensors within the file
	nextline = data_in.readline() #read the next line in the file
	#data_in.truncate(0) 
	try:
		thing = int(nextline) #attempt to convert the value to an integer type
		incoming.append(nextline) #Add the input to an array
	except: #if the conversion to integer fails
		if(nextline != "" and nextline[:3] == "res"): #if the nextline has text and appears to be a reserve call normally sent by the aggregator then store it and exit while, otherwise ignore and continue
			legacyline = nextline
			nextline = ""
			
chosen = incoming[random.randint(0,len(incoming)-1)] #choose one of the integers read in from the file

print(incoming)
print(chosen)
print("legacyline = " +legacyline)

if(legacyline[:3] == "res"): #This needs to be altered before being placed on the live test system to read == not !=
	exit("the legacyline is a reserve command from an aggregator so something has gone wrong, the system may be using files that were not properly cleared in the previous run")

print("printing to topic?")
os.system("mosquitto_pub -p 1883 -t 'agr/phys_sensor_" + str(sensor_id) + "' -m \"res " + chosen[:-1] + "\"") #publish back to the topic the chosen random number
	
	
nextline = data_in.readline() #This should be the res which was sent by the aggregator (this is commented out to allow the aggregator to work with static files for testing purposes)
 
	
i=0
while(i==0): #Run for limited iterations for testing purposes
	nextline = data_in.readline() #read in next data value
	print(nextline)
	if(nextline[:1] != ""): #if there is data available
		#data format is:
		#1613832190 A
		#1613832196 1478*F
		#1613832203 123A*T
		data = nextline[:-1].split(" ") #split the data into a list format
			
		#https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date - Converting unix time to dd/mm/yyyy hh:mm:ss
			
		date_time = datetime.fromtimestamp(int(data[0])) #convert the unix time to a datetime object
		date_time_str = date_time.strftime('%d/%m/%Y %H:%M:%S').split(" ") #convert the datetime object to a string and then split the date/time into two indipendant list values
			
			
		if(data[1] == "A"): #if an alarm was triggered
			writefile = open("json_struct_phys_" + str(sensor_id) + ".txt", "a") #As the notifications are made available, they are converted to json and pushed to this file, ready to be read from
		
			writefile.write("{\"farm_id\" : 1, \"tunnel_id\": 1, \"sensor_id\": " + str(sensor_id) + ", \"time\": \"" + date_time_str[1] + "\", \"date\": \"" + date_time_str[0] + "\", \"Alarm_sounding\": \"T\", \"Pin_entered\": \"NULL\", \"Access_Granted\": \"INVALID\"} \n")
				
			writefile.close()
		else:
			print("Pin entered")
			
			print(data[1][:4])
			print(data[1][4])
			print(data[1][5])
				
			if(data[1][5] == "T"):
				if(data[1][4] == "*"):
					granted = "IN"
				elif(data[1][4] == "#"):
					granted = "OUT"
			elif(data[1][5] == "F"):
				granted = "INVALID"
				
			writefile = open("json_struct_phys_" + str(sensor_id) + ".txt", "a") #As the notifications are made available, they are converted to json and pushed to this file, ready to be read from
			
			writefile.write("{\"farm_id\" : 1, \"tunnel_id\": 1, \"sensor_id\": " + str(sensor_id) + ", \"time\": \"" + date_time_str[1] + "\", \"date\": \"" + date_time_str[0] + "\", \"Alarm_sounding\": \"F\", \"Pin_entered\": \"" + data[1][:4] + "\", \"Access_Granted\": \"" + granted + "\"}, \n")
			
			writefile.close()
			
	time.sleep(1)
	#i+=1
			

	
	
	
	
	
	
	
