#!/usr/bin/python3

import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that streams rows from the user_data table in batches.
    
    Args:
        batch_size (int): The number of rows to fetch in each batch.

    Yields:
        list[dict]: A batch of rows from the user_data table as dictionaries.
    """
    # Connect to the database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='6979samZ.@',
        database='ALX_prodev'
    )
    cursor = connection.cursor(dictionary=True)

    try:
        # Execute the query
        cursor.execute("SELECT * FROM user_data")
        
        while True:
            # Fetch a batch of rows
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break  # Stop when no more rows are available
            yield batch
    finally:
        # Ensure resources are released
        cursor.close()
        connection.close()


def batch_processing(batch_size):
    """
    Processes batches of users to filter those over the age of 25.
    
    Args:
        batch_size (int): The number of rows to fetch in each batch.
    """
    for batch in stream_users_in_batches(batch_size):
        # Filter users over the age of 25
        processed_batch = [user for user in batch if user['age'] > 25]
        for user in processed_batch:
            print(user)
