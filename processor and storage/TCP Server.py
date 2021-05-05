import socket
import tqdm
import os

#tcp client for sending real time data

#send file to GUI through TCP socket
def receivefile(filename): #the function takes in two parameters: file = the file to be received, s = tcp socket
    #server ip address and port
    host = "192.165.255.2"
    port = 432

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
    with open(filename, "w+") as file:
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

#checks whether the received file is sensor data or alarm data
def alarmorsensor(file):
    dict = []
    with open(file, "r"):
        dict = json.load(file)
    tester = dict[1]
    #creates renamed file for integration with other programs
    if len(tester) != 8:
        with open("sensordata.json", "w+") as file:
            json.dumps(dict, indent = 2)
            return file
    else:
        with open("alarmdata.json", "w+") as file:
            json.dumps(dict, indent = 2)
            return file
#driver code
def main():
    os.system("python3 'Postgres to JSON.py'")
    while True: #infinite loop
        datafile = "data.json"
        receivefile(datafile)
        alarmorsensor(datafile)
        os.system("python3 'JSON to Postgres.py'") #executes the json to postgres code
        os.system("python3 'TCP Client.py'") #sends the jsonfile to GUI
        os.remove("data.json")

if (__name__ == __main__):
    main()