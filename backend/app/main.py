from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector 
import json


app = FastAPI()

# Database configuration
DATABASE_CONFIG = {
    'host': 'localhost',
    'port':3306,
    'user': 'adminesan',
    'password': 'passw0rd@1',
    'database': 'esandb'
}
connection = mysql.connector.connect(**DATABASE_CONFIG)
cursor = connection.cursor()

# Test database connection
def test_db_connection():
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        if connection.is_connected():
            connection.close()  # Close the connection after checking
            return True
    except Exception as e:
        print("Error:", e)
        return False

    return False  # Return False if connection is not successful

@app.get("/test-db-connection")
async def test_database_connection():
    if test_db_connection():
        sql_command = "SELECT * FROM test;"
        cursor.execute(sql_command)
        rows = cursor.fetchall()
        for row in rows:
            json_data = json.dumps(rows)
            return json_data
        cursor.close()
        connection.close()
    else:
        return {"error": "Failed to connect to database"}