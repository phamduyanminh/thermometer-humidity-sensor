def thermometer_humidity_sensors(log_file):
    lines = open(log_file, "r").readlines()
    
    # Check if log is empty or not
    if not lines:
        print("Log is empty")
        return
    else:
        print(lines)
                

log_file = "log.txt"
thermometer_humidity_sensors(log_file)