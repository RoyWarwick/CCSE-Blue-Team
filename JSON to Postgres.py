import json
import psycopg2

#sending received JSON data to the Postgres Database

#creating data tables in the database if it doesn't already exist, however, if the table already exists, the sql command will not create a replacement
def createtable():
    connection = psycopg2.connect(
        user = 'storage', #connecting to database as database owner
        host = 'localhost',
        port = '5432', #port 5432 is for connection to a PostgreSQL database
        database = 'farm', #tables inside the 'farm' database are 'crops' and 'alarms'
        password = 'password' #passphrase to gain access as database owner
        )
    #enabling the ability to make insert SQL commands into Postgres database
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    #for sensor data table
    tablecreation = ["""create table if not exists crops (
    dataid bigserial primary key,
    farmid smallint NOT NULL,
    tunnelid smallint NOT NULL,
    sensorid smallint NOT NULL,
    time time NOT NULL,
    date date NOT NULL,
    temp_C real NOT NULL,
    humidity real NOT NULL
    );""",
    #for alarm data table
    """create table if not exists alarms (
    dataID bigserial primary key,
    farmID smallint NOT NULL,
    tunnelID smallint NOT NULL,
    sensorID smallint NOT NULL,
    time time NOT NULL,
    date date NOT NULL,
    alarmSound char(1) NOT NULL,
    PINEntry text,
    access text
    );"""]

    for command in tablecreation:
        cursor.execute(command)
    #commit changes
    connection.commit()

    #closing connection
    connection.close()

#Parsing JSON data coming from sensors, reporting data on temperature in celsius, humidity, time and date

def getsensordata(): 
    #parsing the sensor data from json file
    global sensor_data_json
    with open('sensordata.json') as json_data:
        sensor_data_json = json.load(json_data)
    return sensor_data_json

def getsensorID():
    #retrieving tunnel/sensor id
    global IDArray
    IDArray = []
    tempArray = []
    tunnelID = sensor_data_json["tunnel_id"]
    for key, value in tunnelID.items():
        tempArray = [key] #tunnel id
        for sensor in value:
            tempArray = [key, sensor]
            IDArray.append(tempArray) # [tunnelID, otherdata]
    return IDArray

def getSensorReports():
    #retrieving specific data inside sensor ids to be transferred to the database
    global sensorTransferData
    sensorTransferData = [] #array for the data to be sent to the database
    tempArray = []
    tunnelID = sensor_data_json['tunnel_id']
    for key, value in tunnelID.items():
        for sensor in value:
            #extracting data to be sent
            tempArray = [
                key,
                str(sensor.get('sensor_id')), #psycopg2 requires string format to upload data to the postgres database
                str(sensor.get('time')),
                str(sensor.get('date')),
                str(sensor.get('Temp_C')),
                str(sensor.get('Humidity'))
                ]
            tempArray.insert(0, str(sensor_data_json['farm_id'])) #insert farmID at the start of the array
            sensorTransferData.append(tempArray) #tempArray = [farm_id, tunnel_id, sensorID, time, date, temperature, humidity]
    return sensorTransferData

def sendSensorData():
    #Inserting sensor data into the Postgres Database
    connection = psycopg2.connect(
        user = 'storage', #connecting to database as database owner
        host = 'localhost',
        port = '5432', #port 5432 is for connection to a PostgreSQL database
        database = 'farm', #tables inside the 'farm' database are 'crops' and 'alarms'
        password = 'password' #passphrase to gain access as database owner
        )
    
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    
    #uploading the data into the postgres database, in the crops table
    try:
        #SQL command for inserting data into database
        SQL = """
        insert into crops(farmid, tunnelid, sensorid, time, date, temp_c, humidity) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        for data in sensorTransferData:
            cursor.execute(SQL, (data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
        connection.commit()
        connection.close()
        print("\nDatabase Insert Completed", end='\n')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()

#Parsing and sending alarm data to the Postgres database
def getalarmdata():
    global alarmdict
    with open('alarmdata.json') as json_data:
        alarm_json_data = json.load(json_data) #parsing json data on alarms
    tempdict = []
    alarmdict = []
    for data in alarm_json_data:
    	tempdict=([
    	data.get('farm_id'),
    	data.get('tunnel_id'),
    	data.get('sensor_id'),
    	data.get('time'),
    	data.get('date'),
    	data.get('Alarm_sounding'),
    	data.get('Pin_entered'),
    	data.get('Access_Granted')
    	])
    	alarmdict.append(tempdict)
    return alarmdict


def sendAlarmData():
    connection = psycopg2.connect(
        user = 'storage', #connecting to database as database owner
        host = 'localhost',
        port = '5432', #port 5432 is for connection to a PostgreSQL database
        dbname = 'farm', #tables inside the 'farm' database are 'crops' and 'alarms'
        password = 'password' #passphrase to gain access as database owner
        )
    cursor = connection.cursor()
    for data in alarmdict:
        cursor.execute("insert into alarms(farmid, tunnelid, sensorid, time, date, alarmsound, pinentry, access) values (%s, %s, %s, %s, %s, %s, %s, %s);", (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]))
    connection.commit()
    connection.close()

#driver code
def main():
    #creating tables in Postgres database
    createtable()

    #retrieving and sending data
    try:
        getsensordata()
        getsensorID()
        getSensorReports()
        sendSensorData()
    except FileNotFoundError:
        pass
    try:
        getalarmdata()
        sendAlarmData()
    except FileNotFoundError:
        pass

if __name__ == '__main__':
    main()
