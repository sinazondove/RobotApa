    

# Sample data
from flask import Flask, jsonify, render_template, request
import psycopg2

from database import add_survivor


app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'




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

# API endpoints
@app.route('/add_survivor', methods=['POST'])
def add_survivor_endpoint():
    conn = psycopg2.connect(
        dbname="robotApocalypse",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
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
            infected = data['infected']

            survivor_id = add_survivor(conn, name, age, gender, sa_id_number, latitude, longitude, infected)
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

if __name__ == '__main__':
    # Explicitly set the port to 5000
    app.run(debug=True, port=5000)    