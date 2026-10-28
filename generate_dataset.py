import pandas as pd 
import random
from datetime import datetime,timedelta

number_of_records=5000
print("creating ",number_of_records,"E-commerce-records")

name=["ranju","himesa","teju","amu","hitha","jaanu","pathru","dhanvith"]
gender=["female","male"]
cities=["bengaluru","mysuru","hosur","agara"]
categories=["clothing","mobile","watches","fridge"]
payment_methods=["upi","credit card","debit card","cash"]
order_status=["delivered","cancelled","returned"]

print("basic data list created succesfullu !")


data = []


for i in range(1, number_of_records + 1):

    quantity = random.randint(1, 5)
    unit_price = random.randint(200, 50000)
    discount = random.choice([0, 0.05, 0.10, 0.15, 0.20])

    sales = quantity * unit_price * (1 - discount)
    cost = quantity * unit_price * random.uniform(0.50, 0.80)
    profit = sales - cost

    row = {
        "Order_ID": f"ORD{i:05d}",
        "Customer_ID": f"CUST{random.randint(1, 1500):04d}",
        "Customer_Name": random.choice(name),
        "Age": random.randint(18, 60),
        "Gender": random.choice(gender),
        "City": random.choice(cities),
        "Category": random.choice(categories),
        "Quantity": quantity,
        "Unit_Price": unit_price,
        "Discount": discount,
        "Sales": round(sales, 2),
        "Cost": round(cost, 2),
        "Profit": round(profit, 2),
        "Payment_Method": random.choice(payment_methods),
        "Order_Status": random.choice(order_status)
    }

    data.append(row)

print("Transactions generated:", len(data))


df = pd.DataFrame(data)

df.loc[10, "Customer_Name"] = None
df.loc[25, "City"] = None
df.loc[40, "Age"] = None

duplicate_rows = df.iloc[[100, 200, 300]]

df = pd.concat([df, duplicate_rows], ignore_index=True)


df.loc[50, "Category"] = "electronics"
df.loc[60, "Category"] = "ELECTRONICS"
df.loc[70, "Category"] = " electronics "



df.to_csv("data/raw_data.csv", index=False)

print("Dataset saved successfully!")
print("Rows:", len(df))
print("Columns:", len(df.columns))

print(df.loc[50, "Category"])
print(df.loc[60, "Category"])
print(df.loc[70, "Category"])
