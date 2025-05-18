#!/usr/bin/python3
import mysql.connector
import csv
import os
from uuid import uuid4
from dotenv import load_dotenv

# Load .env file from the current script's directory
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

def connect_db():
    """Connects to the MySQL database server (no database selected yet)."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL server: {err}")
        return None

def create_database(connection):
    """Creates the ALX_prodev database if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        connection.commit()
        cursor.close()
        print("Database 'ALX_prodev' created or already exists.")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

def connect_to_prodev():
    """Connects directly to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to 'ALX_prodev': {err}")
        return None

def create_table(connection):
    """Creates the user_data table if it does not exist."""
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
        connection.commit()
        cursor.close()
        print("Table 'user_data' created or already exists.")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

def insert_data(connection, file_path):
    """Inserts data from a CSV file into the user_data table."""
    if not os.path.exists(file_path):
        print(f"File '{file_path}' does not exist.")
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
        print("Data inserted successfully from CSV.")
    except mysql.connector.Error as err:
        print(f" MySQL error while inserting data: {err}")
    except Exception as e:
        print(f"General error while inserting data: {e}")
