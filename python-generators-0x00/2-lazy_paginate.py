#!/usr/bin/python3
seed = __import__('seed')

def paginate_users(page_size, offset):
    """
    Fetches a page of users from the database.
    
    Args:
        page_size (int): The number of rows to fetch.
        offset (int): The offset to start fetching rows.

    Returns:
        list[dict]: A list of user rows as dictionaries.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_paginate(page_size):
    """
    Lazily loads pages of users using a generator.
    
    Args:
        page_size (int): The number of rows per page.

    Yields:
        list[dict]: The next page of users.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break  # Stop if no more rows are available
        yield page
        offset += page_size
