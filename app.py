    

# Sample data
from flask import Flask, jsonify, make_response, render_template, request
import psycopg2
import logging
from database import add_survivor
import psycopg2
from psycopg2 import Error


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

def add_survivor(conn, survivor_id, name, age, gender, sa_id_number, latitude, longitude, infection_status):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO survivors (survivor_id,name, age, gender, sa_id_number, latitude, longitude, infection_status) VALUES (%s,%s, %s, %s, %s, %s, %s, %s) RETURNING survivor_id",
                       (survivor_id,name, age, gender, sa_id_number, latitude, longitude, infection_status))
        survivor_id = cursor.fetchone()[0]
        conn.commit()
        return survivor_id
    except Exception as e:
        conn.rollback()
        raise e
@app.route('/add_survivors', methods=['POST'])
def add_survivor_endpoint():
    try:
        conn = psycopg2.connect(
            dbname="robotApocalypse",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        
        data = request.json
        survivor_id = data['survivor_id']
        name = data['name']
        age = data['age']
        gender = data['gender']
        sa_id_number = data['sa_id_number']
        latitude = data['latitude']
        longitude = data['longitude']
        infection_status= data['infected']

        survivor_id = add_survivor( conn,survivor_id, name, age, gender, sa_id_number, latitude, longitude, infection_status)
        conn.close()  # Close connection after successful database operation
        return make_response(jsonify({'message': 'Survivor added successfully', 'survivor_id': survivor_id}), 200)
    except Exception as e:
        if 'conn' in locals():  # Check if conn variable is defined
            conn.close()  # Close connection in case of exception
        return make_response(jsonify({'error': str(e)}), 400)

# Assume you have 

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def update_survivor_location(conn, survivor_id, new_latitude, new_longitude):
    try:
        # Create a cursor
        cursor = conn.cursor()

        # Update survivor's location
        if conn:
            # Log the SQL query before execution
            query = """
            UPDATE survivors
            SET latitude = %s, longitude = %s
            WHERE survivor_id = %s
            """
            logging.debug("Executing SQL query: %s", query)

            # Execute the query with parameters
            cursor.execute(query, (new_latitude, new_longitude, survivor_id))

            # Commit the transaction
            conn.commit()

            logging.info(f"Location updated successfully for survivor with ID {survivor_id}")
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error("Error while updating survivor's location:", error)

    # Close cursor
    cursor.close()

@app.route('/update_location/<int:survivor_id>', methods=['POST'])
def update_location_endpoint(survivor_id):
    try:
        # Parse request data and extract new latitude and longitude
        data = request.json
        new_latitude = data['latitude']
        new_longitude = data['longitude']
        
        # Update survivor's location in the database
        conn = psycopg2.connect(
            dbname="robotApocalypse",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        if conn:
            try:
                update_survivor_location(conn, survivor_id, new_latitude, new_longitude)
                return make_response(jsonify({'message': 'Survivor location updated successfully'}), 200)
            except Exception as e:
                return make_response(jsonify({'error': str(e)}), 400)
            finally:
                conn.close()
        else:
            return make_response(jsonify({'message': 'Failed to connect to the database'}), 500)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 400)
# Configure logging
logging.basicConfig(level=logging.DEBUG)

def flag_survivor_as_infected(conn, survivor_id):
    try:
        cursor = conn.cursor()
      

        # Check the number of times infection status reported for the survivor
        if conn:
            # Log the SQL query before execution
            query = ("""SELECT COUNT(*) FROM infection_reports
            WHERE survivor_id = %s AND infection_status = true
            """, (survivor_id,))
            logging.debug("Executing SQL query: %s", query)
        
        
            # Execute the query with parameters
            infection_reports_count = cursor.fetchone()[0]
            cursor.execute(query, (infection_reports_count,survivor_id))

            # Commit the transaction
            conn.commit()

            logging.info(f"Infection status updated successfully for survivor with ID {survivor_id}")
   
        if infection_reports_count >= 3:
            # Update survivor's status as infected in the survivors table
            cursor.execute("""
                UPDATE survivors
                SET infected = true
                WHERE survivor_id = %s
            """, (survivor_id,))

            # Insert a record into the infection_reports table
            cursor.execute("""
                INSERT INTO infection_reports (survivor_id, infection_status)
                VALUES (%s, true)
            """, (survivor_id,))

            conn.commit()

            logging.info(f"Survivor with ID {survivor_id} flagged as infected")
            return True  # Survivor flagged as infected
        else:
            logging.debug(f"Survivor with ID {survivor_id} not flagged as infected")
            return False  # Survivor not flagged as infected
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error("Error while updating survivor's infection status:", error)
        logging.debug(f"Infection reports count for survivor {survivor_id}: {infection_reports_count}")
        conn.rollback()
        logging.error(f"Error while flagging survivor {survivor_id} as infected: {error}")
        raise error
    finally:
        cursor.close()

@app.route('/flag_infected/<int:survivor_id>', methods=['POST'])
def flag_infected_endpoint(survivor_id):
    try:
        conn = psycopg2.connect(
            dbname="robotApocalypse",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        
        if flag_survivor_as_infected(conn, survivor_id):
            return make_response(jsonify({'message': 'Survivor not flagged as infected'}), 200)
        else:
            return make_response(jsonify({'message': 'Survivor flagged as infected'}), 201)
        
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)