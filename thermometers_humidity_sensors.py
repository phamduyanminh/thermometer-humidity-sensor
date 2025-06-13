import math

class Sensor:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.datas = []
        #TODO:
        # WAY TOO MUCH HARDCODE -> CONST TYPE (NEED TO BE CAPITALIZED | INDEX VALUE)
    
    def set_datas(self, value):
        self.datas.append(value)
        
    def get_datas(self):
        return self.datas
    
    def get_type(self):
        return self.type

    def validate_sensor(self, reference_thermometer, reference_humidity):
        pass

###########################################################################################
# Class Thermometer    
class Thermometor(Sensor):
    def __init__(self, name):
        super().__init__(name, "thermometer")
        
    def validate_sensor(self, reference_thermometer, reference_humidity):
        result = "N/A"
        
        if not self.datas:
            return result 
        
        mean = calculate_mean(self.datas)
        std = calculate_std(self.datas, mean)
        mean_difference = abs(mean - reference_thermometer)
        
        if mean_difference <= 0.5:
            if std < 3:
                result = "ultra precise"
            elif std < 5:
                result = "very precise"
            else:
                result = "precise"
        else:
            result = "precise"

###########################################################################################
# Class Humidity        
class Humidity(Sensor):
    def __init__(self, name):
        super().__init__(name, "humidity")
    
    def validate_sensor(self, reference_thermometer, reference_humidity):
        result = "N/A"
        
        if not self.datas:
                result = "discard"
        else:
            humidity_lower_range = reference_humidity - (0.01 * reference_humidity)
            humidity_upper_range = reference_humidity + (0.01 * reference_humidity)

            all_datas_are_in_range = True
            for data_point in self.datas:
                if not (humidity_lower_range <= data_point <= humidity_upper_range):
                    all_datas_are_in_range = False
                    break
            
            if all_datas_are_in_range:
                result = "OK"
            else:
                result = "discard"
        
        return result

###########################################################################################
# Class Sensor Factory
class SensorFactory:
    def sensor_factory(name, sensor_type):
        if sensor_type == "thermometer":
            return Thermometor(name)
        elif sensor_type == "humidity":
            return Humidity(name)
        else:
            print('Invalid sensor type!')
            return None

###########################################################################################
# Function calculate mean
def calculate_mean(datas):
    if not datas:
        return 0.0
    return sum(datas)/len(datas)

# Function calculate std
def calculate_std(datas, mean):
    if not datas:
        return 0.0
    variance = sum([(data - mean) ** 2 for data in datas]) / len(datas)
    return math.sqrt(variance)

###########################################################################################
# Main function 
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
        
        if len(data_section) < 2 or len(data_section) > 3:
            print(f'Data is invalid!')  
            continue          
        
        if data_section[0] == "thermometer" or data_section[0] == "humidity":
            sensor_type = data_section[0]
            sensor_name = data_section[1]
            
            if sensor_name not in sensor_map:
                sensor_object = SensorFactory.sensor_factory(sensor_name, sensor_type)
                if sensor_object:
                    sensor_map[sensor_name] = sensor_object
            else:
                print(f'{sensor_name} is already in the record!')
     
        else:
            sensor_name = data_section[1]
            sensor_value = float(data_section[2])
            if sensor_name in sensor_map:
                sensor_object = sensor_map[sensor_name]
                sensor_object.set_datas(sensor_value)
            else:
                print(f'{sensor_name} is not available in record yet!')
    
    for sensor_name in sensor_map:
        sensor_object = sensor_map[sensor_name]    
        result = sensor_object.validate_sensor(reference_thermometer, reference_humidity)
        sensor_result_output.append(f"{sensor_name}: {result}")
    
    for final_result in sensor_result_output:
        print(final_result)


log_file = "log.txt"
thermometer_humidity_sensors(log_file)