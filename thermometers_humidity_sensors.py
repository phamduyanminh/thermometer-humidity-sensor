import math

class Sensor:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.datas = []
    
    def set_datas(self, value):
        self.datas.append(value)
        

def calculate_mean(datas):
    if not datas:
        return 0.0
    return sum(datas)/len(datas)

def calculate_std(datas, mean):
    if not datas:
        return 0.0
    variance = sum([(data - mean) ** 2 for data in datas]) / len(datas)
    return math.sqrt(variance)

def thermometer_humidity_sensors(log_file):
    lines = open(log_file, "r").readlines()
    
    # Check if log is empty or not
    if not lines:
        print("Log is empty")
        return
    
    sensor_map: dict[Sensor] = {}
    sensor_order: list[str] = []
    sensor_result_output: list[str] = []
    
    reference_line = lines[0].split()
    reference_thermometer = float(reference_line[1])
    reference_humidity = float(reference_line[2])
    
    for line in lines[1:]:
        line_data = line.strip()
        data_section = line_data.split()
        
        if data_section[0] == "thermometer" or data_section[0] == "humidity":
            sensor_type = data_section[0]
            sensor_name = data_section[1]
            
            if sensor_name not in sensor_map:
                sensor_map[sensor_name] = Sensor(sensor_name, sensor_type)
                sensor_order.append(sensor_name)
        else:
            sensor_name = data_section[1]
            sensor_value = float(data_section[2])
            if sensor_name in sensor_map:
                sensor_object = sensor_map[sensor_name]
                sensor_object.set_datas(sensor_value)
                

log_file = "log.txt"
thermometer_humidity_sensors(log_file)