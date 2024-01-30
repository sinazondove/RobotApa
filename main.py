import psycopg2
from database import add_survivor, add_survivor_resources, add_survivor_status, update_survivor_location

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
                print("Thank you for using the system.")
            
        print("Would you like to Add yourself as a survivor?:")
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

    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL database:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
