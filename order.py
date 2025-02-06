import csv
import random
import string
from datetime import datetime, timedelta

class Order:
    def __init__(self, order_id, customer_id, order_date, amount):
        self.order_id = order_id
        self.customer_id = customer_id
        self.order_date = order_date
        self.amount = amount

def create_order_table(connection):
    create_table_sql = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Order' and xtype='U')
    CREATE TABLE [Order] (
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
    print("Order table created successfully (if it did not already exist).")
    cursor.close()
    

# Function to generate random order date
def generate_random_date(start_date, end_date):
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

# Generate a larger dataset for the Order table
order_data = []
start_date = datetime(2020, 1, 1)
end_date = datetime(2023, 12, 31)
for i in range(1, 1001):
    customer_id = random.randint(1, 1000)  # assuming there are 1000 customers
    order_date = generate_random_date(start_date, end_date)
    amount = round(random.uniform(10.0, 1000.0), 2)
    order_data.append({"OrderId": i, "CustomerId": customer_id, "OrderDate": order_date, "Amount": amount})

# CSV file name for orders
csv_file = "large_orders.csv"

# Write data to CSV file
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["OrderId", "CustomerId", "OrderDate", "Amount"])
    writer.writeheader()
    for row in order_data:
        writer.writerow(row)

print(f"Order data written to {csv_file} successfully.")
