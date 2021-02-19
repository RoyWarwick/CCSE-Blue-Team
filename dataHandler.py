import json


def getData():
    global JSON_FILE
    with open('jsonData.json') as json_data:
        JSON_FILE = json.load(json_data)

    return JSON_FILE


getData()


def getSensorInfo():
    sensor_array = []
    tunnels = JSON_FILE["tunnel_id"]
    for key, value in tunnels.items():
        for sensor in value:
            sensor_array.append(sensor)
            """
            for k, v in sensor.items():
                print(f"{k}: {v}")
            """
    return sensor_array


getSensorInfo()


def getExtremeData():
    extreme_data_array = []
    tunnels = JSON_FILE["tunnel_id"]
    for key, value in tunnels.items():
        print(key)
        for sensor in value:
            if sensor['Temp_C'] > 50 and sensor['Humidity'] > 50:
                temp_array = []  # Temp Array to store information to append to the multidimensional array
                temp_array[0] = key  # Tunnel_id
                temp_array[1] = sensor.id  # Sensor ID
                temp_array[2] = sensor.Temp_C  # Sensor Temperature
                temp_array[3] = sensor.Humidity  # Sensor Humidity
                extreme_data_array.append(temp_array)
    return extreme_data_array

    # for k, v in sensor.items():
    # print(f"{k}: {v}")


getExtremeData()


def getTooHotSensors():  # returns array of hot sensors
    sensor_info = getSensorInfo()
    extreme_temperature = []
    for x in sensor_info:
        if x['Temp_C'] > 50:
            extreme_temperature.append(x)
    return extreme_temperature


def getTooHumidSensors():
    sensor_info = getSensorInfo()
    extreme_humidity = []
    for x in sensor_info:
        if x['Humidity'] > 50:
            extreme_humidity.append(x)
    return extreme_humidity


def getFarmData():
    return None


def getTunnelData():
    return None
