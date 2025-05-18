#!/usr/bin/python3
seed = __import__('seed')

def stream_user_ages():
    """
    Generator to stream user ages one by one from the database.
    
    Yields:
        int: The age of each user.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    
    for row in cursor:
        yield row['age']
    
    connection.close()

def calculate_average_age():
    """
    Calculate the average age using the stream_user_ages generator.
    
    Prints:
        The average age of users.
    """
    total_age = 0
    count = 0
    
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count == 0:
        print("No users in the dataset.")
    else:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")
