import threading
import os
import json
import time



#finds the mac address and the associated id, if not found, append to host_id
def find_mac(mac):
    line_number =0
    with open ("host_id", "a+") as f:       #put file on append mode
        f.seek(0)
        for line in f:
            line_number += 1
            if mac in line:
                return line_number
        mac_id = line_number + 1        #the next line number will be the new mac's id
        f.write(mac + " " + str(mac_id) + "\n")        #add new MAC and id
        f.truncate()
    return mac_id


def sort_tunnel_json(json_struc):
    tunnel_json = json.loads(json_struc)    #change the data to json format
    return tunnel_json


def repeat():
    tunnel_json_list = []
    with open("aggr_env_in.json", "r") as f:
        while (True):
            s = f.readline()
            
            if not s:
                if (len(tunnel_json_list) > 0): #check if the list contains any data
                    final_json = {"farm_id": 1, "tunnel_id" : tunnel_json_list}     #json structure required
                    with open("sensordata.json", "w") as fd:        #create new file
                        json.dump(final_json, fd, indent=4)         
                        os.system("python3 tcp_client.py sensordata.json &")        #send data off to processor
                    
                    tunnel_json_list.clear()
                    #os.system("echo '' > /tmp/temp.json") #can clear out file
                time.sleep(10)
            if len(s) > 25:
                mac = s[:17]        #gets the macaddress
                rest_of_json = s[18:-1]    #gets the json sent
                mac_id = find_mac(mac)      #get the id associated to the mac address
                rest_json = sort_tunnel_json(rest_of_json)  #turn the rest of the string into json structure
                tunnel_json = {mac_id : rest_json}      #desired json structure
                tunnel_json_list.append(tunnel_json)       #add to list

repeat()