import threading
import os
import time


l = []

def concat_json():
    #threading.Timer(3.0, concat_json).start()
    with open ("temp.json", "r") as f:
        while (True):
            s = f.readline()        #read file line
            if not s:
                time.sleep(3)
            #Now we get the MAC address and replace with our own id
            with open ("host_id", "a+") as f2: #open file to read and append
                f2.seek(0)
                host_file = f2.read()
                if s[:17] in host_file:
                    new_s = s[18:]
                    output_json = {"farm_id" : 1, tunnel_id : {} }
                else:
                    f2.write(s[:17])
                    f2.write("\n")
                f2.truncate()
           

    
         

concat_json()

#use readline 
