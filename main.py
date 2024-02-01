import psycopg2
from database import add_survivor, add_survivor_resources, add_survivor_status, calculate_percentage, get_infected_survivors, get_non_infected_survivors, update_survivor_location, validate_sa_id
from robotInfo import get_robot_information
from flask import Flask, jsonify, render_template, request

def main():
    conn = psycopg2.connect(
        dbname="robotApocalypse",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    while True:
        print("Are you an existing user? (yes/no):")
        existing_user = input().lower() == "yes"

        if existing_user:
            print("Enter your ID number:")
            sa_id_number = input()

            # Validate SA ID number against the database
            is_valid = validate_sa_id(conn, sa_id_number)
            if not is_valid:
                print("SA ID number does not exist in the database.")
                continue

            print("Do you want to update your location? (yes/no):")
            update_location = input().lower() == "yes"
            if update_location:
                print("Enter your new latitude and longitude:")
                latitude = float(input("Latitude: "))
                longitude = float(input("Longitude: "))
                update_survivor_location(conn, sa_id_number, latitude, longitude)
                print("Survivor location updated successfully.")

            print("Do you want to update your infection status? (yes/no):")
            update_infection_status = input().lower() == "yes"
            if update_infection_status:
                print("Are you infected? (yes/no):")
                infected = input().lower() == "yes"
                add_survivor_status(conn, sa_id_number, infected)
                print("Survivor infection status updated successfully.")

        else:
            print("\nWould you like to Add yourself as a survivor? (yes/no):")
            add_survivor_option = input().lower() == "yes"
            if add_survivor_option:
                name = input("Name: ")
                age = int(input("Age: "))
                gender = input("Gender: ")
                sa_id_number = input("SA ID number (13 digits): ")
                latitude = float(input("Latitude: "))
                longitude = float(input("Longitude: "))
                print("Are you infected? (yes/no):")
                infected = input().lower() == "yes"
                survivor_id = add_survivor(conn, name, age, gender, sa_id_number, latitude, longitude, infected)
                print("Survivor added successfully with ID:", survivor_id)

        print("\nDisplaying Robot Information:")
        robot_data = get_robot_information()
        if robot_data:
            for robot in robot_data:
                print(f"Model: {robot['model']}, Serial Number: {robot['serialNumber']}, Category: {robot['category']}")
        else:
            print("No robot information available.")

        print("\nList of Infected Survivors:")
        infected_survivors = get_infected_survivors(conn)
        if infected_survivors:
            for survivor in infected_survivors:
                print(survivor)  # Print each infected survivor's details
        else:
            print("No infected survivors.")

        print("\nList of Non-Infected Survivors:")
        non_infected_survivors = get_non_infected_survivors(conn)
        if non_infected_survivors:
            for survivor in non_infected_survivors:
                print(survivor)  # Print each non-infected survivor's details
        else:
            print("No non-infected survivors.")
            infected_survivors = get_infected_survivors(conn)
        non_infected_survivors = get_non_infected_survivors(conn)
        total_survivors = len(infected_survivors) + len(non_infected_survivors)

        infected_survivors_count = len(infected_survivors)
        non_infected_survivors_count = len(non_infected_survivors)

        percentage_infected = calculate_percentage(infected_survivors_count, total_survivors)
        percentage_non_infected = calculate_percentage(non_infected_survivors_count, total_survivors)

        print("Percentage of Infected Survivors:", percentage_infected)
        print("Percentage of Non-Infected Survivors:", percentage_non_infected)


        print("\nWould you like to continue? (yes/no):")
        continue_option = input().lower() == "yes"
        if not continue_option:
            break
        

    conn.close()
    

# Sample data
app = Flask(__name__)
robots = [
    {
        "model": "09FYU",
        "serialNumber": "Y0RIFQHMVBVTL50",
        "manufacturedDate": "2024-02-10T09:06:08.9862851+00:00",
        "category": "Land"
    },
    # Other robot objects...
]

@app.route('/')
def display_robots():
    formatted_robots = []
    for robot in robots:
        formatted_robot = {
            "Model": robot["model"],
            "Serial Number": robot["serialNumber"],
            "Manufactured Date": robot["manufacturedDate"],
            "Category": robot["category"]
        }
        formatted_robots.append(formatted_robot)

    # Check if the client accepts HTML
    if 'text/html' in request.headers['Accept']:
        return render_template('robots.html', robots=formatted_robots)
    else:
        return jsonify(formatted_robots)

if __name__ == "__main__":
    main()
