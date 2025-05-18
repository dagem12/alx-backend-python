# Python Generators Project

## Overview

This project introduces advanced usage of Python generators for efficient data processing, particularly in scenarios involving large datasets, batch processing, and lazy loading. It emphasizes memory-efficient computation using Python's `yield` keyword and demonstrates integration with SQL databases.

---

## Project Objectives

By completing this project, you will:

1. **Master Python Generators**  
   Learn how to create and utilize generators for iterative data processing to optimize memory usage.

2. **Handle Large Datasets**  
   Implement batch processing and lazy loading techniques to process extensive datasets efficiently.

3. **Simulate Real-world Scenarios**  
   Develop solutions for live data streaming and apply them to dynamic, real-time contexts.

4. **Optimize Performance**  
   Use generators to compute aggregate functions on large datasets without excessive memory consumption.

5. **Integrate with SQL**  
   Dynamically fetch data using SQL queries and integrate Python with MySQL/SQLite databases for robust data handling.

---

## Repository Structure

```
alx-backend-python/
├── python-generators-0x00/
│   ├── seed.py
│   ├── 0-main.py
│   ├── 0-stream_users.py
│   ├── 1-batch_processing.py
│   ├── 2-lazy_paginate.py
│   ├── 1-main.py
│   ├── 2-main.py
│   ├── 3-main.py
│   ├── README.md
```

---

## Project Requirements

- Python 3.x proficiency.
- Familiarity with `yield` and Python's generator functions.
- Understanding of SQL database operations (MySQL/SQLite).
- Basic knowledge of schema design and data seeding.
- Git and GitHub for version control and submission.

---

## Tasks

### 0. **Getting Started with Python Generators**
**Objective:** Create a generator to stream rows from an SQL database.

1. **Setup:**
   - Use `seed.py` to create the `ALX_prodev` database and the `user_data` table.
   - Populate the table with sample data from `user_data.csv`.

2. **Functions to Implement:**
   - `connect_db()`: Connect to the MySQL server.
   - `create_database(connection)`: Create `ALX_prodev` if it doesn't exist.
   - `connect_to_prodev()`: Connect to the `ALX_prodev` database.
   - `create_table(connection)`: Create the `user_data` table.
   - `insert_data(connection, data)`: Seed the table with data.

3. **Validation:**
   - Use `0-main.py` to test the implementation.

---

### 1. **Streaming Data with Generators**
**Objective:** Implement a generator that streams rows one by one.

- Write `0-stream_users.py`:
  - Function `stream_users()` should yield rows one by one from the `user_data` table.
- Validate using `1-main.py`.

---

### 2. **Batch Processing Large Data**
**Objective:** Create a generator for batch processing.

- Write `1-batch_processing.py`:
  - `stream_users_in_batches(batch_size)`: Fetch rows in batches.
  - `batch_processing(batch_size)`: Filter users over age 25 from batches.

- Validate using `2-main.py`.

---

### 3. **Lazy Loading Paginated Data**
**Objective:** Implement lazy loading for paginated data.

- Write `2-lazy_paginate.py`:
  - `lazy_paginate(page_size)`: Load paginated data lazily using `paginate_users(page_size, offset)`.

- Validate using `3-main.py`.

---

## Running the Project

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/alx-backend-python.git
   ```
2. Navigate to the project directory:
   ```bash
   cd alx-backend-python/python-generators-0x00
   ```
3. Install necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute the tasks:
   - Run individual task scripts (e.g., `python3 0-main.py`).

---

## Learning Outcomes

- Effective use of Python generators for iterative data access.
- Handling and processing large datasets without memory overflow.
- Integrating Python with SQL databases to fetch and process data dynamically.
- Applying lazy loading and batch processing techniques in real-world contexts.

---
