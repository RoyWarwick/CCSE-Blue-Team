import socket
import tqdm
import os

#tcp client for sending real time data

#send file to GUI through TCP socket
def receivefile(filename): #the function takes in two parameters: file = the file to be sent, s = tcp socket
    #server ip address and port
    host = "192.165.255.2"
    port = 22

    buffer_size = 1024 #receive 1024 bytes at a time
    separator = "<separator>"
    
    #create tcp socket
    s = socket.socket()
    s.bind((host,port))
    s.listen(5) #wait for client connection
    
    #accept client connection
    client_socket, addr = s.accept()
    print(f"[+] {addr} is connected.", end='\n')

    #receive file info
    received = client_socket.recv(buffer_size).decode()
    filename, filesize = received.split(separator)

    #remove file path if needed
    filename = os.path.basename(filename)
    filesize = int(filesize) #convert to integer

    #start receiving file from socket + write to file stream
    progress = tdqm.tdqm(range(filesize), f"Receiving {filename}", unit = "B", unit_scale = True, unit_divisor = 1024)
    with open(filename, "wb") as file:
        while True:
            #read bytes from socket
            read_bytes = client_socket.recv(buffer_size)
            if not read_bytes:
                #when file transfer is finished
                print("File Received!", end = '\n')
                break
            #write received bytes to file
            file.write(read_bytes)
            #update progress bar
            progress.update(len(read_bytes))
    
    #close socket
    s.shutdown(s.SHUT_WR) #notify server that transfer is complete
    s.close()

#driver code
def main():
    s = networkconfig() #setup tcp socket
    sensorfile = "sensordata.json"
    sendfile(sensorfile)
    alarmfile = "alarmdata.json"
    sendfile(alarmfile)

if (__name__ == __main__):
    main()