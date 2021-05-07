import threading
import glob, os
import json

l = []

def concat_json():
    threading.Timer(10.0, concat_json).start()
    os.chdir(".")
    for file in glob.glob("*.json"):
        with open (file, "r") as f:
            temp = json.load(f)
            l.append(temp)
    print(l)
    l.clear()
         

concat_json()

#use readline 
