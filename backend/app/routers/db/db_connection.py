# db_connection.py

import mysql.connector

# Database configuration
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'adminesan',
    'password': 'passw0rd@1',
    'database': 'esandb'
}

# Function to establish database connection
def connect_to_database():
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()
        print("Database connection established successfully")
        return connection, cursor
    except mysql.connector.Error as error:
        print("Error connecting to database:", error)
        return None, None
