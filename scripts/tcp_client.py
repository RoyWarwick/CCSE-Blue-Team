import socket

#tcp server for sending client real time data

#setting up network for file transfer
def networkconfig():
    #server ip address and port
    s = socket.socket() #create socket object
    ipaddr = "192.168.255.254 " #local ip address
    host = socket.gethostname() #get local machine name
    port = 22 #using port number 22 to send data
    s.bind((host, port)) #binding hostname to port
    return s

#send file to GUI through TCP socket
def sendfile(file, s): #the function takes in two parameters: file = the file to be sent, s = tcp socket
    #get filesize
    filesize = os.path.getsize(file)
    s.listen(5) #wait for client connection
    while True:
        conn, addr = socket.accept() #accept client connection
        print('Received connection from ', addr, end='\n')
        print('Sending...', end='\n')
        l = file.read(1024)
        #the program will send the JSON data in 1024 byte chunks
        while (l):
            print('Sending...', end='\n')
            s.send(l)
            l = file.read(1024)
        f.close() #close file since all is transferred
        print('File transfer complete', end='\n') #Protocol for when the file transfer is complete
        s.shutdown(s.SHUT_WR) #Notify client that file transfer is done
        print(s.recv(1024), end = '\n')
        s.close() #close socket when done

#driver code
def main():
    s = networkconfig() #setup tcp socket
    try:
        sensorfile = open("sensordata.json", "r")
        sendfile(sensorfile, s)
    except IOError: #in the case where the file cannot be opened
        print("File does not exist or cannot be opened", end="\n")

    try:
        alarmfile = open("alarmdata.json", "r")
        sendfile(alarmfile, s)
    except IOError:
        print("File does not exist or cannot be opened", end="\n")

if (__name__ == __main__):
    main()