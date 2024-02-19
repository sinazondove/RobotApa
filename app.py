    

# Sample data
import datetime
import time
from flask import Flask, jsonify, make_response, render_template, request
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import logging
from database import add_survivor
import psycopg2
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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


# Define SQLAlchemy database connection
# Replace 'your_postgres_username', 'your_postgres_password', 'your_postgres_host', and 'your_postgres_database' with your PostgreSQL credentials
DATABASE_URL = 'postgresql://postgres:postgres@localhost/robotApocalypse'
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Define SQLAlchemy models
class Survivor(Base):
    __tablename__ = 'survivors'
    survivor_id = Column(Integer, primary_key=True)
    name = Column(String)
    infection_status = Column(Boolean, default=False)

class InfectionReport(Base):
    __tablename__ = 'infection_reports'
    survivor_id = Column(Integer, primary_key=True)
    survivor_id = Column(Integer, nullable=False)

# Define endpoint to update infection status and add infection report
@app.route('/update_infection_status/<int:survivor_id>', methods=['POST'])
def update_infection_status(survivor_id):
    # Check if survivor exists
    survivor = session.query(Survivor).filter_by(id=survivor_id).first()
    if not survivor:
        return jsonify({'error': 'Survivor not found'}), 404
    
    # Get number of infection reports for the survivor
    num_reports = session.query(InfectionReport).filter_by(survivor_id=survivor_id).count()
    
    # Update infection status and add infection report if necessary
    if num_reports >= 3:
        survivor.infection_status = True
        session.add(InfectionReport(survivor_id=survivor_id))
        session.commit()
        return jsonify({'message': 'Infection status updated and infection report added'}), 200
    else:
        return jsonify({'message': 'Infection status not updated'}), 200

# Run Flask application
if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(debug=True)
