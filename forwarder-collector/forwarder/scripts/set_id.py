import glob, os

#first read if host exist in host file, append if not
with open ("host_id", "r") as f:
    temp = f.read()
    print(temp)
    os.chdir(".")
    for file in glob.glob("my_macaddress*"):
        with open (file, "r") as f1:
            temp1 = f1.read()
            if temp1 in temp:
                print("in")
                continue
            else:
                print(temp1)    
                print("hello")