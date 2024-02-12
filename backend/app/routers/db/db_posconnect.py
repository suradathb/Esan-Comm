import mysql.connector

# Database configuration
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'adminesan',
    'password': 'passw0rd@1',
    'database': 'esanposdb'
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

# def connect_to_database():
#     # Database configuration
#     db_config = {
#         'host': 'localhost',
#         'port': 3306,
#         'user': 'adminesan',
#         'password': 'passw0rd@1',
#         'database': 'esanposdb'
#     }

#     try:
#         # Establish a connection to the database
#         connection = mysql.connector.connect(**db_config)

#         # Create a cursor object to execute SQL queries
#         cursor = connection.cursor()

#         # Return both the connection and cursor objects
#         return connection, cursor

#     except mysql.connector.Error as error:
#         print("Error connecting to the database: ", error)
#         # You might want to handle the error appropriately,
#         # such as logging it or raising an exception.
#         raise