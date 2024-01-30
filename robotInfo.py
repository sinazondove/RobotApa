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
def process_robot_information(robot_data):
    if robot_data:
        flying_robots = []
        land_robots = []

        for robot in robot_data:
            category = robot["category"]

            if category == "Flying":
                flying_robots.append(robot)
            elif category == "Land":
                land_robots.append(robot)

        # Sort the lists of robots based on their manufacturedDate
        flying_robots.sort(key=lambda x: x["manufacturedDate"])
        land_robots.sort(key=lambda x: x["manufacturedDate"])

        return flying_robots, land_robots
    else:
        return None, None
