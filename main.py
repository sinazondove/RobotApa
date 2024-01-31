import psycopg2
from database import add_survivor, add_survivor_resources, add_survivor_status, get_infected_survivors, update_survivor_location
from robotInfo import get_robot_information
from flask import Flask, jsonify, render_template, request

def main():
    try:
        conn = psycopg2.connect(
            dbname="robotApocalypse",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        
        print("Are you an existing user? (yes/no):")
        existing_user = input().lower() == "yes"

        if existing_user:
            print("Enter your ID number:")
            sa_id_number = input()

            print("Do you want to update your location? (yes/no):")
            update_location = input().lower() == "yes"

            if update_location:
                print("Enter your new latitude and longitude:")
                latitude = float(input("Latitude: "))
                longitude = float(input("Longitude: "))

                # Update survivor location
                update_survivor_location(conn, sa_id_number, latitude, longitude)
                print("Survivor location updated successfully.")

            print("Do you want to update your infection status? (yes/no):")
            update_infection_status = input().lower() == "yes"

            if update_infection_status:
                print("Are you infected? (yes/no):")
                infected = input().lower() == "yes"

                # Update survivor infection status
                add_survivor_status(conn, sa_id_number, infected)
                print("Survivor infection status updated successfully.")

        else:
            print("Displaying Robot Information:")
            robot_data = get_robot_information()
            if robot_data:
                for robot in robot_data:
                    print(f"Model: {robot['model']}, Serial Number: {robot['serialNumber']}")
            else:
                print("No robot information available.")

            print("\nWould you like to Add yourself as a survivor?:")
            name = input("Name: ")
            age = int(input("Age: "))
            gender = input("Gender: ")
            sa_id_number = input("SA ID number (13 digits): ")
            latitude = float(input("Latitude: "))
            longitude = float(input("Longitude: "))

            # Add survivor to Survivors table
            survivor_id = add_survivor(conn, name, age, gender, sa_id_number, latitude, longitude)

            # Prompt user to enter survivor resources
            water = int(input("Water: "))
            food = int(input("Food: "))
            medication = int(input("Medication: "))
            ammunition = int(input("Ammunition: "))

            # Add survivor resources to Survivor_Resources table
            add_survivor_resources(conn, survivor_id, water, food, medication, ammunition)

            print("Survivor added successfully with ID:", survivor_id)
            print("Survivor resources added successfully.")

        print("\nWould you like to continue? (yes/no):")
        continue_option = input().lower() == "yes"

        if continue_option:
            main()  # Recursively call main function to continue
        else:
            # Display list of infected survivors
           
            # Add code to display list of infected survivors here
            conn = psycopg2.connect(
            dbname="robotApocalypse",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        
        print("Are you an existing user? (yes/no):")
        existing_user = input().lower() == "yes"

        if existing_user:
            # Check if survivor already exists
            cur = conn.cursor()
            cur.execute("SELECT * FROM Survivors WHERE sa_id_number = %s", (sa_id_number,))
            existing_survivor = cur.fetchone()
            

            if existing_survivor:
                # Update survivor location
                sql = "UPDATE Survivors SET latitude = %s, longitude = %s WHERE sa_id_number = %s"
                cur.execute(sql, (latitude, longitude, sa_id_number))
                print("Survivor location updated successfully.")
        else:
            # Displaying Robot Information logic here...




          print("\nWould you like to continue? (yes/no):")
        continue_option = input().lower() == "yes"

        if continue_option:
            main()  # Recursively call main function to continue
    finally:
        conn.close()    

# Sample data
app=Flask(__name__)
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
# API endpoints
@app.route('/add_survivor', methods=['POST'])
def add_survivor_endpoint():
    conn = psycopg2.connect()
    if conn:
        try:
            data = request.json
            name = data['name']
            age = data['age']
            gender = data['gender']
            sa_id_number = data['sa_id_number']
            latitude = data['latitude']
            longitude = data['longitude']

            survivor_id = add_survivor(conn, name, age, gender, sa_id_number, latitude, longitude)
            if survivor_id:
                return jsonify({'message': 'Survivor added successfully', 'survivor_id': survivor_id}), 200
            else:
                return jsonify({'message': 'Failed to add survivor'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 400
        finally:
            conn.close()
    else:
        return jsonify({'message': 'Failed to connect to the database'}), 500


if __name__ == "__main__":
    main()
