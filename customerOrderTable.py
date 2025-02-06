import csv
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

# Function to generate a random name
def generate_random_name(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

# Function to generate random order date
def generate_random_date(start_date, end_date):
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

# Generate data for the Customer table
customers = [{"CustomerId": i, "FirstName": generate_random_name(10)} for i in range(1, 1001)]

# Generate data for the Order table
orders = []
start_date = datetime(2020, 1, 1)
end_date = datetime(2023, 12, 31)
order_id_counter = 1
for customer in customers:
    num_orders = random.randint(1, 5)  # Each customer can have 1 to 5 orders
    for _ in range(num_orders):
        order_date = generate_random_date(start_date, end_date)
        amount = round(random.uniform(10.0, 1000.0), 2)
        orders.append({"OrderId": order_id_counter, "CustomerId": customer["CustomerId"], "OrderDate": order_date, "Amount": amount})
        order_id_counter += 1

# Write combined data to CSV files
customers_csv_file = "combined_customers.csv"
orders_csv_file = "combined_orders.csv"

# Write Customer data to CSV file
with open(customers_csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["CustomerId", "FirstName"])
    writer.writeheader()
    for row in customers:
        writer.writerow(row)

# Write Order data to CSV file
with open(orders_csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["OrderId", "CustomerId", "OrderDate", "Amount"])
    writer.writeheader()
    for row in orders:
        writer.writerow(row)

print(f"Customer data written to {customers_csv_file} successfully.")
print(f"Order data written to {orders_csv_file} successfully.")
