#!/usr/bin/python3

import mysql.connector

def stream_users():
    """
    Generator that streams rows from the user_data table one by one.
    Yields:
        dict: A row from the user_data table as a dictionary.
    """
    # Connect to the database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username
        password='6979samZ.@',  # Replace with your MySQL password
        database='ALX_prodev'
    )
    cursor = connection.cursor(dictionary=True)  # Fetch rows as dictionaries

    try:
        # Execute the query
        cursor.execute("SELECT * FROM user_data")
        
        # Yield each row one by one
        for row in cursor:
            yield row
    finally:
        # Ensure resources are released
        cursor.close()
        connection.close()
