#!/usr/bin/python3
import mysql.connector
import csv
import os
from uuid import uuid4


def connect_db():
    """Connects to the MySQL database server."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your MySQL username
            password='6979samZ.@',  # Replace with your MySQL password
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None


def create_database(connection):
    """Creates the database ALX_prodev if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
        print("Database ALX_prodev created or already exists.")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")


def connect_to_prodev():
    """Connects to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your MySQL username
            password='6979samZ.@',  # Replace with your MySQL password
            database='ALX_prodev'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None


def create_table(connection):
    """Creates a table user_data if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(5,2) NOT NULL,
                INDEX (user_id)
            )
        """)
        cursor.close()
        print("Table user_data created or already exists.")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")


def insert_data(connection, file_path):
    """Inserts data into the user_data table from a CSV file."""
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    try:
        cursor = connection.cursor()
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        name=VALUES(name), email=VALUES(email), age=VALUES(age)
                """, (str(uuid4()), row['name'], row['email'], row['age']))
        connection.commit()
        cursor.close()
        print("Data inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")
