import os
import time
import json
import threading


def find(file_name, mac):
    line_number = 0
    # Open the file in read only mode
    with open(file_name, "a+") as f:
        f.seek(0) #make sure file read starts from top of file
        # Read all lines in the file one by one
        for line in f:
            # For each line, check if line contains the string
            line_number += 1
            if mac in line:
                return line_number

        newline= line_number + 1
        f.write(mac + " " + str(newline) + "\n")        #add new MAC and id
        f.truncate()
    return newline


def sort_json():
    tunnel_json_list = []
    threading.Timer(3.0, sort_json).start()
    with open ("/tmp/temp.json", "r") as f:
        while (True):
            s = f.readline()
            if not s:
                break       #if s is empty then escape while loop
            mac = s[:17]    
            rest_of_json = json.loads(s[18:-1])
            mac_id = find("host_id", mac)
            #get the json in correct format
            tunnel_json = {mac_id: rest_of_json}    #gets (from) tunnel to right json structure
            tunnel_json_list.append(tunnel_json)    #append to a list ready for final json structure
    final_json = {"farm_id": 1, "tunnel_id" : tunnel_json_list}
    print(final_json)       
    tunnel_json_list.clear()
    final_json.clear()
    os.system("echo '' > /tmp/temp.json")


sort_json()