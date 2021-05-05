import psycopg2
from datetime import datetime
import json
import os
from flask import Flask
import sendFile

#retrieving data from database
def fromDatabase(farmid,tunnelid,startdate,enddate):
    connection = psycopg2.connect( #connecting to the database with given parameters
        user = "storage",
        host = "localhost",
        dbname = "farm",
        port = "5432",
        password = "password"
        )
    cursor = connection.cursor()

    #making an array to put into the sql command
    inputarray = [farmid, tunnelid, str(startdate), str(enddate)]

    #sql language to be sent to database
    farmsql = """
    SELECT * from crops where farmid = %s and tunnelid = %s and date between %s and %s;
    """

    #database output
    #farm data
    cursor.execute(farmsql,(inputarray[0], inputarray[1], inputarray[2], inputarray[3]))
    farmsql_result = cursor.fetchall() #outputs a list in the form of [(dataid, farmid, tunnelid, sensorid, time, date, temp_c, humidity), (next batch)]
    
    return farmsql_result

#convert farm postgres data to desired JSON format
def FarmtoJSON(data):
    dict = {
        "farm_id" : data[0][1],
        "tunnel_id" : {
            data[0][2] : []
            }
        }
    #appending the sensor data
    for batch in data:
    	dict["tunnel_id"][1].append({
            "sensor_id" : batch[3],
            "time" : batch[4].strftime('%H:%M:%S'),
            "date" : batch[5].strftime('%d/%m/%Y'),
            "Temp_C" : batch[6],
            "Humidity" : batch[7]
            })
    #formatting the data into JSON format
    json_dict = json.dumps(dict, indent=2)
    return json_dict

#driver code
def main():
    #receiving API request
    app=Flask(__name__)
    app.run(debug = True)

    @app.route('/log', methods=['GET'])
    parameters = [] #parameters sent by the GUI, in the order of [farmid, tunnelid, startdate, enddate]
    with open("send_to_arno", "r") as file:
        line = file.read().split(',') #each parameter is split by a ,
        parameters.append(line)

    try:
        farmdata = fromDatabase(parameters[0], parameters[1], parameters[2], parameters[3])
        global farmjson
        farmjson = FarmtoJSON(farmdata)

    except TypeError:
        print("Not enough parameters given", end='\n')
    
    #writing the farm json data to a file
    with open("APIRequest.json", "w+") as file:
        file.write("Farm Data \n")
        file.write(farmjson)
        sendFile.send_file(file)

if __name__ == '__main__':
    main()