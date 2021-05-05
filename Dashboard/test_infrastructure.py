import dataHandler


def test_number_of_sensors():
    sensor_array = []
    assumed_sensor = 38
    JSON_FILE = dataHandler.getData()
    tunnels = JSON_FILE["tunnel_id"]
    for key, value in tunnels.items():
        for sensor in value:
            sensor_array.append(sensor)
    running_total = len(sensor_array)
    assert running_total == assumed_sensor, f"There are {running_total} sensors active"


def test_number_of_tunnels():
    JSON_FILE = dataHandler.getData()
    tunnels = JSON_FILE["tunnel_id"]
    number_of_tunnels = len(tunnels.items())
    assumed_tunnels = 2
    assert number_of_tunnels == assumed_tunnels, f"Your assumption is incorrect there are {number_of_tunnels} of tunnels"

def test_physical_access_attempt():
    JSON_FILE = dataHandler.getPhysicalSecurityData()
    Attempts = len(JSON_FILE)
    assert 5 == Attempts, f"The website stores up to a maximum of 5 attempts, however currently it has only received {Attempts}"






