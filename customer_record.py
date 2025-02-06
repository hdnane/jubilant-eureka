import csv
import random
import string

# Function to generate a random name
def generate_random_name(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

# Generate a larger dataset for the Customer table
large_data = [{"CustomerId": i, "FirstName": generate_random_name(10)} for i in range(1, 1001)]

# CSV file name
csv_file = "large_customers.csv"

# Write data to CSV file
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["CustomerId", "FirstName"])
    writer.writeheader()
    for row in large_data:
        writer.writerow(row)

print(f"Data written to {csv_file} successfully.")
