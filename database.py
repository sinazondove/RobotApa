import psycopg2

def add_survivor(conn, name, age, gender, sa_id_number, latitude, longitude, infected):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Survivors (name, age, gender, sa_id_number, latitude, longitude, infection_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING survivor_id
    """, (name, age, gender, sa_id_number, latitude, longitude, infected))
    survivor_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return survivor_id

def add_survivor_resources(conn, survivor_id, water, food, medication, ammunition):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Survivor_Resources (survivor_id, water, food, medication, ammunition)
        VALUES (%s, %s, %s, %s, %s)
    """, (survivor_id, water, food, medication, ammunition))
    conn.commit()
    cur.close()

def update_survivor_location(conn, sa_id_number, latitude, longitude):
    cur = conn.cursor()
    cur.execute("""
        UPDATE Survivors
        SET latitude = %s, longitude = %s
        WHERE sa_id_number = %s
    """, (latitude, longitude, sa_id_number))
    conn.commit()
    cur.close()
    
def add_survivor_status(conn, sa_id_number, infected):
    cur = conn.cursor()

    # Check if the survivor already exists in the database
    cur.execute("SELECT * FROM Survivors WHERE sa_id_number = %s", (sa_id_number,))
    existing_survivor = cur.fetchone()

    if existing_survivor:
        # Update the infection status in the Survivors table
        cur.execute("UPDATE Survivors SET infection_status = %s WHERE sa_id_number = %s", (infected, sa_id_number))
        conn.commit()
        cur.close()
        return True

    cur.close()
    return False

def validate_sa_id(conn, sa_id_number):
    """
    Validate the SA ID number format.
    """
    if len(sa_id_number) != 13:
        return False

    # Check if SA ID number contains only digits
    if not sa_id_number.isdigit():
        return False
    # Check if SA ID number is 13 digits long
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM Survivors WHERE sa_id_number = %s", (sa_id_number,))
        count = cur.fetchone()[0]
        return count > 0
    except psycopg2.Error as e:
        print("Error validating SA ID number:", e)
        return False
    finally:
        cur.close()

def get_non_infected_survivors(conn):
    """
    Retrieve a list of survivors that are not infected from the survivor table.

    Args:
    - conn: psycopg2 connection object

    Returns:
    - A list of non-infected survivors (as dictionaries) if successful, or
    - None if an error occurs.
    """
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Survivors WHERE infection_status = false")
        non_infected_survivors = cur.fetchall()
        return non_infected_survivors
    except psycopg2.Error as e:
        print("Error fetching non-infected survivors:", e)
        return None
    finally:
        if cur:
            cur.close()

def get_infected_survivors(conn):
    """
    Retrieve a list of survivors who are infected from the survivor table.

    Args:
    - conn: psycopg2 connection object

    Returns:
    - A list of infected survivors (as dictionaries) if successful, or
    - None if an error occurs.  """
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Survivors WHERE infection_status = true")
        infected_survivors = cur.fetchall()
        return infected_survivors
    except psycopg2.Error as e:
        print("Error fetching infected survivors:", e)
        return None
    finally:
        if cur:
            cur.close()

def display_existing_survivors(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Survivors")
    existing_survivors = cur.fetchall()
    cur.close()

    if existing_survivors:
        for survivor in existing_survivors:
            print("ID:", survivor[0], "Name:", survivor[1], "Age:", survivor[2], "Gender:", survivor[3], "SA ID:", survivor[4])
    else:
        print("No existing survivors.")


def calculate_percentage(survivor_count, total_count):
    if total_count == 0:
        return 0
    return (survivor_count / total_count) * 100