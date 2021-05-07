import socket
import tqdm
import os

#tcp server for receiving client real time data

#send file to GUI through TCP socket
def sendfile(filename): #the function takes in two parameters: file = the file to be sent, s = tcp socket
    separator = "<separator>"
    buffer_size = 1024 #the program will send the JSON data in 1024 byte chunks
    
    #setting up network for file transfer
    #client ip address and port
    host = "192.165.255.2"
    port = 22

    #get filesize, for printing progress
    filesize = os.path.getsize(filename)
    
    s = socket.socket() #create client socket
    s.connect((host, port)) #connecting to socket
    
    #sending the filename and filesize
    s.send(f"{filename}{separator}{filesize}".encode())

    #sending the file
    progress = tdqm.tdqm(range(filesize), f"Sending {filename}", unit = "B", unit_scale = "True", unit_divisor = 1024) #showing progress
    with open(filename, "rb") as file:
        while True:
            #read bytes from file
            read_bytes = f.read(buffer_size)
            if not read_bytes:
                #when file transmission is done
                print("File Transfer Complete", end = "\n")
                break
            #sending bytes
            s.sendall(read_bytes)
            #update progress bar
            progress.update(len(read_bytes))
    
    #close socket
    s.shutdown(s.SHUT_WR) #notify server that transfer is complete
    s.close()

#driver code
def main():
    try:
        filename = "sensordata.json"
        file = open(filename, "r")
        file.close()
        sendfile(filename)
        os.remove("sensordata.json")
        
    except IOError: #in the case where the file cannot be opened
        print("File does not exist or cannot be opened", end="\n")

    try:
        filename = "alarmdata.json"
        file = open(filename, "r")
        file.close()
        sendfile(filename)
        os.remove("alarmdata.json")
    except IOError:
        print("File does not exist or cannot be opened", end="\n")

if (__name__ == __main__):
    main()