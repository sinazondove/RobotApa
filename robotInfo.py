# Function to retrieve robot information
import requests


def get_robot_information():
    try:
        url = "https://robotstakeover20210903110417.azurewebsites.net/robotcpu"
        response = requests.get(url, verify=False)  # Disable SSL certificate verification
        
        if response.status_code == 200:
            robot_data = response.json()
            return robot_data
        else:
            print("Failed to retrieve robot information. Status code:", response.status_code)
            return None
    except Exception as e:
        print("Error:", e)
        return None

# Function to find robot location based on model and serial number
def find_robot_location(model, serial_number):
    robot_data = get_robot_information()

    if robot_data:
        for robot in robot_data:
            if robot["model"] == model and robot["serialNumber"] == serial_number:
                # Extract latitude and longitude from the model and serial number
                latitude = float(model[:2] + '.' + model[2:4])
                longitude = float(serial_number[:2] + '.' + serial_number[2:4])
                return {"latitude": latitude, "longitude": longitude}
        
        # If the robot with the specified model and serial number is not found
        return "Robot not found"
    else:
        return "Failed to retrieve robot information"
def display_robot_list(robot_data):
    print("List of Robots:")
    for robot in robot_data:
        print(f"Model: {robot['model']}, Serial Number: {robot['serialNumber']}")
