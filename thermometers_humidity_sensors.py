def thermometer_humidity_sensors(log_file):
    lines = open(log_file, "r").readlines()
    
    # Check if log is empty or not
    if not lines:
        print("Log is empty")
        return
    
    
    reference_temperature = None
    reference_humidity = None
    sensor_data = {}
    sensor_data_order = []
    result_output = []
    
    reference_line = lines[0].split()
    reference_temperature = float(reference_line[1])
    reference_humidity = float(reference_line[2])
    
    for line in lines[1:]:
        data = line.strip()
        data_section = data.split()
        
        if data_section[0] == "thermometer" or data_section[0] == "humidity":
            sensor_type = data_section[0]
            sensor_name = data_section[1]

            if sensor_name not in sensor_data:
                sensor_data[sensor_name] = {"type": sensor_type, "datas": []}
                sensor_data_order.append(sensor_name)
        else:
            sensor_name = data_section[1]
            sensor_value = float(data_section[2])
            
            if sensor_name in sensor_data:
                sensor_data[sensor_name]["datas"].append(sensor_value)
                

log_file = "log.txt"
thermometer_humidity_sensors(log_file)