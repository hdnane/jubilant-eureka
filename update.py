import pyodbc
import random
import string
from datetime import datetime, timedelta

class Customer:
    def __init__(self, customer_id, first_name):
        self.customer_id = customer_id
        self.first_name = first_name

class Order:
    def __init__(self, order_id, customer_id, order_date, amount):
        self.order_id = order_id
        self.customer_id = customer_id
        self.order_date = order_date
        self.amount = amount

def create_customer_table(connection):
    create_table_sql = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Customer' and xtype='U')
    CREATE TABLE Customer (
        CustomerId BIGINT PRIMARY KEY,
        FirstName VARCHAR(100) NOT NULL
    )
    """
    cursor = connection.cursor()
    cursor.execute(create_table_sql)
    connection.commit()
    print("Customer table created successfully (if it did not already exist).")
    cursor.close()

def create_order_table(connection):
    create_table_sql = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Orders' and xtype='U')
    CREATE TABLE Orders (
        OrderId BIGINT PRIMARY KEY,
        CustomerId BIGINT NOT NULL,
        OrderDate DATE NOT NULL,
        Amount DECIMAL(10, 2) NOT NULL,
        FOREIGN KEY (CustomerId) REFERENCES Customer(CustomerId)
    )
    """
    cursor = connection.cursor()
    cursor.execute(create_table_sql)
    connection.commit()
    print("Orders table created successfully (if it did not already exist).")
    cursor.close()

def insert_customer(connection, customer_id, first_name):
    if customer_exists(connection, customer_id):
        print(f"Customer with ID {customer_id} already exists. Skipping insertion.")
        return
    insert_sql = "INSERT INTO Customer (CustomerId, FirstName) VALUES (?, ?)"
    cursor = connection.cursor()
    cursor.execute(insert_sql, (customer_id, first_name))
    connection.commit()
    print("Customer inserted successfully.")
    cursor.close()

def insert_order(connection, order_id, customer_id, order_date, amount):
    if order_exists(connection, order_id):
        print(f"Order with ID {order_id} already exists. Skipping insertion.")
        return
    insert_sql = "INSERT INTO Orders (OrderId, CustomerId, OrderDate, Amount) VALUES (?, ?, ?, ?)"
    cursor = connection.cursor()
    cursor.execute(insert_sql, (order_id, customer_id, order_date, amount))
    connection.commit()
    print(f"Order {order_id} inserted successfully.")
    cursor.close()

def customer_exists(connection, customer_id):
    select_sql = "SELECT COUNT(*) FROM Customer WHERE CustomerId = ?"
    cursor = connection.cursor()
    cursor.execute(select_sql, (customer_id,))
    exists = cursor.fetchone()[0] > 0
    cursor.close()
    return exists

def order_exists(connection, order_id):
    select_sql = "SELECT COUNT(*) FROM Orders WHERE OrderId = ?"
    cursor = connection.cursor()
    cursor.execute(select_sql, (order_id,))
    exists = cursor.fetchone()[0] > 0
    cursor.close()
    return exists

def main():
    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=HospitalDB;"
        "Trusted_Connection=yes;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )
    connection = pyodbc.connect(connection_string)   
    print("Connection established successfully.")

    # Create the tables (if not exists)
    create_customer_table(connection)
    create_order_table(connection)

    # Generate data for the Customer table
    customers = [{"CustomerId": i, "FirstName": generate_random_name(10)} for i in range(1, 1001)]

    # Generate data for the Order table
    orders = []
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2023, 12, 31)
    order_id_counter = 1
    for customer in customers:
        # Insert customers into the Customer table
        insert_customer(connection, customer["CustomerId"], customer["FirstName"])
        
        num_orders = random.randint(1, 5)  # Each customer can have 1 to 5 orders
        for _ in range(num_orders):
            order_date = generate_random_date(start_date, end_date)
            amount = round(random.uniform(10.0, 1000.0), 2)
            # Insert orders into the Order table
            insert_order(connection, order_id_counter, customer["CustomerId"], order_date, amount)
            order_id_counter += 1

    # Close the connection
    connection.close()

    print("All data inserted successfully.")

def generate_random_name(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

def generate_random_date(start_date, end_date):
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

if __name__ == "__main__":
    main()
