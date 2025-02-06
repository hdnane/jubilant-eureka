import pyodbc

class Customer:
    def __init__(self, customer_id, first_name):
        self.customer_id = customer_id
        self.first_name = first_name

def create_table(connection):
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

def customer_exists(connection, customer_id):
    select_sql = "SELECT COUNT(*) FROM Customer WHERE CustomerId = ?"
    cursor = connection.cursor()
    cursor.execute(select_sql, (customer_id,))
    exists = cursor.fetchone()[0] > 0
    cursor.close()
    return exists

def find_by_customer_id(connection, customer_id):
    select_sql = "SELECT CustomerId, FirstName FROM Customer WHERE CustomerId = ?"
    cursor = connection.cursor()
    cursor.execute(select_sql, (customer_id,))
    row = cursor.fetchone()
    customer = Customer(row.CustomerId, row.FirstName) if row else None
    cursor.close()
    return customer

def update_customer(connection, customer_id, first_name):
    update_sql = "UPDATE Customer SET FirstName = ? WHERE CustomerId = ?"
    cursor = connection.cursor()
    cursor.execute(update_sql, (first_name, customer_id))
    connection.commit()
    print("Customer updated successfully.")
    cursor.close()

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

    # Create the Customer table (if not exists)
    create_table(connection)

    # Insert data into the Customer table
    insert_customer(connection, 1, "John Doe")
    insert_customer(connection, 2, "Jane Doe")

    # Update data in the Customer table
    update_customer(connection, 1, "Johnathan Doe")

    # Retrieve and print customer data
    customer = find_by_customer_id(connection, 1)
    if customer:
        print(f"Customer ID: {customer.customer_id}")
        print(f"First Name: {customer.first_name}")

    # Close the connection
    connection.close()

if __name__ == "__main__":
    main()
