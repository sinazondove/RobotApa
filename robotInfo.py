
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


def display_robot_list(robot_data):
    print("List of Robots:")
    for robot in robot_data:
        print(f"Model: {robot['model']}, Serial Number: {robot['serialNumber']}")
