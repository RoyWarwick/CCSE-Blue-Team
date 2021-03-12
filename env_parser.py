import time
import sys
import os
import random
import string

#There will be an open mosquitto subscriber for the topic associated with the sensor id (agr/env_sensor_<sensor_id>)
#this subscriber will output to the file ./tmp/env_sensor_<sensor_id>

sensor_id = int(sys.argv[1]) #read in the id for this sensor from the command line
file_name = "./tmp/env_sensor_"+str(sensor_id) #use this id to specify the file to look for data in

data_in = open(file_name, "r") #open the file ready for reading
nextline = "" #set aside variable for data to be written into
incoming = [] #set aside varible for incoming second-stage random numbers to be written into
legacyline = "" #set aside variable for keeping data when transitioning from establishing a connection to reading data

while(nextline == ""): #while there is no data available within the file (the sensors have not yet connected) 
	nextline = data_in.readline() #read in the next line of data
	time.sleep(1) #wait for connections
	
incoming.append(nextline) #add the first input to the array

while(nextline != ""): #while there is still data to be read from the sensors within the file
	nextline = data_in.readline() #read the next line in the file
	try:
		thing = int(nextline) #attempt to convert the value to an integer type
		incoming.append(nextline) #Add the input to an array
	except: #if the conversion to integer fails
		if(nextline != "" and nextline[:3] == "res"): #if the nextline has text and appears to be a reserve call normally sent by the aggregator then store it and exit while, otherwise ignore and continue
			legacyline = nextline
			nextline = ""
			
chosen = incoming[random.randint(0,len(incoming)-1)] #choose one of the integers read in from the file

#print("I gots this far")
#print(incoming)
#print(chosen)

if(legacyline[:3] == "red"): #This needs to be altered before being placed on the live test system to read == not !=
	exit("the legacyline is a reserve command from an aggregator so something has gone wrong, the system may be using files that were not properly cleared in the previous run")

#print("I have printed the res command")
os.system("mosquitto_pub -p 1883 -t 'agr/env_sensor_" + str(sensor_id) + "' -m \"res " + chosen[:-1] + "\"") #publish back to the topic the chosen random number
#print("okay, no more res")


time.sleep(1) #
	
nextline = data_in.readline() #This should be the res which was sent by the aggregator (this is commented out to allow the aggregator to work with static files for testing purposes)
#print("nextline here is: "+nextline)	

i = 0
while(i==0): #as with establish_connect.py this is for testing purposes to have a finite loop and 
	nextline = data_in.readline() #This should be the first data value
	#print("The next line is: " + nextline[:-1])
		
	#if the next line is not blank (a blank line indicating that the sensor has not yet sent data)
	if(nextline[:-1] != ""): 
		#print("Nextline is not blank")
		data = nextline[:-1].split(" ") #divide the line of data into a list format
		#Data form ['03/03/2021', '16:02:28', 'T=23.9', 'H=47.1']
		try:
			data[2] = data[2][2:] #remove the 'T='
			data[3] = data[3][2:] #remove the 'H='
			
			writefile = open("json_struct_sensor_" + str(sensor_id) + ".txt", "a")
			
			writefile.write("{\"sensor_id\":"+str(sensor_id)+ ", \"time\": \""+data[1]+ "\", \"date\": \""+data[0]+ "\", \"Temp_C\":"+data[2]+ ", \"Humidity\":"+data[3]+ "}, \n") #write the json structure to the file
			
			writefile.close()
		except:
			time.sleep(0.1)
	time.sleep(3)
	#i+=1 
	
writefile.close() #close the file the json structure is being saved to
	






	
	
