import threading
import os
import json
import time

#this file are identical to env_in_json.py except for some file names, more code comments are on that file

def find_mac(mac):
    line_number =0
    with open ("host_id", "a+") as f:
        f.seek(0)
        for line in f:
            line_number += 1
            if mac in line:
                return line_number
        mac_id = line_number + 1
        f.write(mac + " " + str(mac_id) + "\n")        #add new MAC and id
        f.truncate()
    return mac_id


def sort_tunnel_json(json_struc):
    tunnel_json = json.loads(json_struc)
    return tunnel_json


def repeat():
    tunnel_json_list = []
    with open("aggr_phys_in.json", "r") as f:
        while (True):
            s = f.readline()
            
            if not s:
                if (len(tunnel_json_list) > 0):
                    final_json = {"farm_id": 1, "tunnel_id" : tunnel_json_list}
                    with open("alarmdata.json", "w") as fd:
                        json.dump(final_json, fd, indent=4)
                        os.system("python3 tcp_client.py alarmdata.json &")
                    
                    tunnel_json_list.clear()
                    #os.system("echo '' > /tmp/temp.json")
                
                time.sleep(10)
            if len(s) > 25:
                mac = s[:17]
                rest_of_json = s[18:-1]    
                mac_id = find_mac(mac)
                rest_json = sort_tunnel_json(rest_of_json)
                tunnel_json = {mac_id : rest_json}
                tunnel_json_list.append(tunnel_json)

repeat()