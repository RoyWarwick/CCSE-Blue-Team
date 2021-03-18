import json


def getPhysicalSecurityData():
    global PHYSICAL_SECURITY_JSON
    with open('physical_security.json') as json_data:
        PHYSICAL_SECURITY_JSON = json.load(json_data)
    return PHYSICAL_SECURITY_JSON


getPhysicalSecurityData()


def getData():
    global JSON_FILE
    with open('jsonData.json') as json_data:
        JSON_FILE = json.load(json_data)

    return JSON_FILE


getData()


def getSecurityDate():
    global SECURITY_FILE
    with open('physical_security.json') as security_data:
        SECURITY_FILE = json.load(security_data)
    return SECURITY_FILE


getSecurityDate()


def getSensorInfo():
    sensor_array = []
    tmp_array = []
    tunnels = JSON_FILE["tunnel_id"]
    for key, value in tunnels.items():
        tmp_array = [key]  # Tunnel_id
        for sensor in value:
            tmp_array = [key,
                         sensor]  # ["tunnel_id", {'sensor_id': 1, 'time': '14:55:30', 'date': '03/02/2021', 'Temp_C': 22, 'Humidity': 12}],
            sensor_array.append(tmp_array)  # [[tunnel_id, sensor_dictionary],[tunnel_id, sensor_dictionary],....]
            """
            for k, v in sensor.items():
                print(f"{k}: {v}")
            """
    return sensor_array


getSensorInfo()


def getExtremeData():
    global EXTREME_DATA_ARRAY
    EXTREME_DATA_ARRAY = []
    tunnels = JSON_FILE["tunnel_id"]
    for key, value in tunnels.items():
        for sensor in value:
            if 23 <= sensor['Temp_C'] or sensor['Temp_C'] < 22 and 50 <= sensor['Humidity'] or sensor['Humidity'] < 49:
                temp_array = [  # Temp Array to store information to append to the multidimensional array
                    key,  # Tunnel_id
                    sensor.get('sensor_id'),  # sensor_id
                    sensor.get('Temp_C'),  # temperature of the current sensor
                    sensor.get('Humidity'),  # Humidity of current sensor
                    "ht"]
                EXTREME_DATA_ARRAY.append(
                    temp_array)  # temp_array[0]= tunnel_id temp_array[1]= temp_array[2]=Temperature temp_array[3]=Humidity
            elif 23 <= sensor['Temp_C'] or sensor['Temp_C'] < 22 and (50 > sensor['Humidity'] >= 49):
                temp_array = [  # Temp Array to store information to append to the multidimensional array
                    key,  # Tunnel_id
                    sensor.get('sensor_id'),  # sensor_id
                    sensor.get('Temp_C'),  # temperature of the current sensor
                    sensor.get('Humidity'),  # Humidity of current sensor
                    "t"]
                EXTREME_DATA_ARRAY.append(
                    temp_array)  # temp_array[0]= tunnel_id temp_array[1]= temp_array[2]=Temperature temp_array[3]=Humidity
            elif (23 > sensor['Temp_C'] >= 22) and 50 <= sensor['Humidity'] or sensor['Humidity'] < 49:
                temp_array = [  # Temp Array to store information to append to the multidimensional array
                    key,  # Tunnel_id
                    sensor.get('sensor_id'),  # sensor_id
                    sensor.get('Temp_C'),  # temperature of the current sensor
                    sensor.get('Humidity'),  # Humidity of current sensor
                    "h"]
                EXTREME_DATA_ARRAY.append(
                    temp_array)  # temp_array[0]= tunnel_id temp_array[1]= temp_array[2]=Temperature temp_array[3]=Humidity temp
    return EXTREME_DATA_ARRAY


getExtremeData()


def sortExtremeData():
    sorted_array = []
    t_array = []
    h_array = []
    for x in range(len(EXTREME_DATA_ARRAY)):
        if EXTREME_DATA_ARRAY[x][4] == "ht":
            sorted_array.append(EXTREME_DATA_ARRAY[x])
        elif EXTREME_DATA_ARRAY[x][4] == "t":
            t_array.append(EXTREME_DATA_ARRAY[x])
        elif EXTREME_DATA_ARRAY[x][4] == "h":
            h_array.append(EXTREME_DATA_ARRAY[x])

    if len(t_array) > len(h_array):
        for x in range(len(t_array)):
            try:
                sorted_array.append(t_array[x])
                sorted_array.append(h_array[x])
            except IndexError:
                None

    else:
        for x in range(len(h_array)):
            try:
                sorted_array.append(t_array[x])
                sorted_array.append(h_array[x])
            except IndexError:
                sorted_array.append(h_array[x])

    return sorted_array  # returns an array structure of sensors that are in the following format all the HT then T,H till exhaustion


def getTunnelData():
    status_indicator = []
    tunnels = JSON_FILE["tunnel_id"]
    for key, value in tunnels.items():
        flag = True
        for sensor in value:
            if 23 <= sensor['Temp_C'] or sensor['Temp_C'] < 22 or 50 <= sensor['Humidity'] or sensor['Humidity'] < 49:
                flag = False
                break
        temp_array = [key, flag]
        status_indicator.append(temp_array)
    return status_indicator


getTunnelData()
