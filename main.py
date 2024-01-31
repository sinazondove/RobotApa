import psycopg2
from database import add_survivor, add_survivor_resources, add_survivor_status, update_survivor_location
from robotInfo import get_robot_information, find_robot_location

def main():
    try:
        conn = psycopg2.connect(
            dbname="robotApocalypse",
            user="postgres",
            password="postgres",
            host="127.0.0.1",
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
            print("List of Infected Survivors:")
            # Add code to display list of infected survivors here

    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL database:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
