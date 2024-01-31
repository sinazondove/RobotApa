import psycopg2

def add_survivor(conn, name, age, gender, sa_id_number, latitude, longitude):
    cur = conn.cursor()
    try:
        sql = "INSERT INTO Survivors (name, age, gender, sa_id_number, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s) RETURNING survivor_id"
        cur.execute(sql, (name, age, gender, sa_id_number, latitude, longitude))
        survivor_id = cur.fetchone()[0]
        conn.commit()
        print("Survivor added successfully with ID:", survivor_id)
        return survivor_id
    except psycopg2.Error as e:
        conn.rollback()
        print("Error inserting survivor:", e)
    finally:
        cur.close()
def update_survivor_location(conn, sa_id_number, latitude, longitude):
    cur = conn.cursor()
    try:
        # Check if survivor with given SA ID number exists
        cur.execute("SELECT * FROM Survivors WHERE sa_id_number = %s", (sa_id_number,))
        existing_survivor = cur.fetchone()

        if existing_survivor:
            # Update survivor location
            sql = "UPDATE Survivors SET latitude = %s, longitude = %s WHERE sa_id_number = %s"
            cur.execute(sql, (latitude, longitude, sa_id_number))
            conn.commit()
            print("Survivor location updated successfully.")
        else:
            print("Survivor with SA ID number {} not found.".format(sa_id_number))

    except psycopg2.Error as e:
        conn.rollback()
        print("Error updating survivor location:", e)
    finally:
        cur.close()


def add_survivor_resources(conn, survivor_id, water, food, medication, ammunition):
    cur = conn.cursor()
    try:
        sql = "INSERT INTO Survivor_Resources (survivor_id, water, food, medication, ammunition) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(sql, (survivor_id, water, food, medication, ammunition))
        conn.commit()
        print("Survivor resources added successfully.")
    except psycopg2.Error as e:
        conn.rollback()
        print("Error inserting survivor resources:", e)
    finally:
        cur.close()

def add_survivor_status(conn, survivor_id, infected):
    cur = conn.cursor()
    try:
        # Check if survivor status already exists
        cur.execute("SELECT * FROM Survivor_Status WHERE survivor_id = %s", (survivor_id,))
        existing_status = cur.fetchone()

        if existing_status:
            # Survivor status exists, update times_reported_infected
            times_reported_infected = existing_status[2] + 1 if infected else existing_status[2]
            cur.execute("UPDATE Survivor_Status SET times_reported_infected = %s WHERE survivor_id = %s", (times_reported_infected, survivor_id))
            print("Survivor status updated: Infected (times reported infected: {})".format(times_reported_infected))
            
            # Check if reported by more than 3 users and update status to "infected"
            if times_reported_infected >= 3:
                cur.execute("UPDATE Survivor_Status SET infected = TRUE WHERE survivor_id = %s", (survivor_id,))
                print("Survivor status updated to infected.")
            else:
                print("Survivor status remains unchanged.")
        else:
            # Survivor status does not exist, insert new record
            times_reported_infected = 1 if infected else 0
            cur.execute("INSERT INTO Survivor_Status (survivor_id, infected, times_reported_infected) VALUES (%s, %s, %s)", (survivor_id, infected, times_reported_infected))
            print("Survivor status added successfully.")

        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        print("Error inserting/updating survivor status:", e)
    finally:
        cur.close()

def get_infected_survivors(conn):
    """
    Retrieve the list of infected survivors from the database.
    
    Args:
    - conn: psycopg2 connection object
    
    Returns:
    - List of dictionaries representing infected survivors
    """
    infected_survivors = []
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name, sa_id_number FROM Survivors WHERE infected = true OR infection_reports > 3")
        rows = cursor.fetchall()
        
        for row in rows:
            survivor = {
                "name": row[0],
                "sa_id_number": row[1]
            }
            infected_survivors.append(survivor)
        
        return infected_survivors
    
    except psycopg2.Error as e:
        print("Error retrieving infected survivors:", e)
        return None
    
    finally:
        if cursor:
            cursor.close()