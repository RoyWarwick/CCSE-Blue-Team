import time
import os
import sys

#When a sensor is activated it will send a random integer to the topic "agr/env"
#When the Aggregator reads that command it will begin a python process subscribed to a new topic "agr/env_sensor_<integer>"
#post the random integer followed by the name of the topic subcribed to by the new python script in the topic "agr/env_response"
#The assigned integer will be incremented for each assigned connection and will act as the sensor ID

#The sensors will read the messages published in agr/env_response and upon recognising their random integer will connect to the associated topic.

#The sensor will publish a message (MAC address), encrypted by the pre-shared ipsec key to the topic assigned to them as well as a secondary different random number.

#upon the unlikely scenario that two sensors choose the same random number and are directed to the same topic the aggregator will read in the random numbers sent to the new topic from sensors that also have a valid ipsec encrypted message and will publish one of them back, the channel will then be dedicated to the sensor that posted that random number and all others will disconnect and return to the "agr/env" topic to re-try a connection.



try:
	null = sys.argv[1] #read the value after the program name from the commandline argument
	#print("This has loaded for: " + null)
except: #Not enough arguments have been provided to indicate connection type
	exit("Not a valid usage, to call the program use: \n'python3 establish_connection.py <value>' \nWhere <value> is either 'env' or 'phys'")


if(sys.argv[1] == "env"): #indicates negotiation for the environmental data sensors
	type_connect = "env"
elif(sys.argv[1] == "phys"): #indicates negotiation for the physical data sensors
	type_connect = "phys"
else: #The program has been given additional arguments that do not indicate connection type
	exit("Not a valid usage, to call the program use: \n'python3 establish_connection.py <value>' \nWhere <value> is either 'env' or 'phys'")



incoming = open("./tmp/" + type_connect + "_incoming", 'r') #open the file that the mosquitto topic is publishing to, as defined in startup.sh

next_sensor_id = 1 #The ID of the next sensor to add

i=0
while(i==0): #For a general system this will run indefinitely checking for new connections, for the current test build it will run a finite number of times
	current = incoming.readline() #read the next line of the file
	#print(current)
	if(current != ""): #assuming that the readline function has been able to retrieve information from the file
		#print("This thing is not blank")
		try:
			#print(int(current)) #The expected value should be a random integer from the sensor
			
			#Start a mosquitto topic and file, each associated with the next_sensor_id, will be of form (mosquitto_sub -p 1883 -t 'agr/env_sensor_1' > ./tmp/env_sensor_1 &)
			os.system("mosquitto_sub -p 1883 -t 'agr/" + type_connect + "_sensor_" + str(next_sensor_id) + "' > ./tmp/" + type_connect + "_sensor_" + str(next_sensor_id) + " &")
			
			#publish to the response topic associating a random number with the topic so that sensors who published said number can connect to it.
			os.system("mosquitto_pub -p 1883 -t 'agr/" + type_connect + "_response' -m \"" + current[:-1] + " agr/" + type_connect + "_sensor_" + str(next_sensor_id) + "\"")
			
			#The parsing program is responsible for the mosquitto topic, including ensuring only one sensor is connected.
			
			
			#begin the parser to be responsible for the newly established sensor topic
			os.system("python3 " + type_connect + "_parser.py " + str(next_sensor_id) + " &")
			
			#increment the sensor id
			next_sensor_id+=1			
		except: #if the value read in isn't an int it is not valid
			#print("except triggered: not int")
			j=0 #deal with indentation errors
	else:
		time.sleep(1) #wait for more connections if there hasn't been one discovered in the present cycle
	#i+=1 #incremention of the indicator for the while loop, related to test build
	
incoming.close() #close the file that data is being read from


