import pandas as pd
import matplotlib.pyplot as plt
import os

# Load cleaned dataset
df = pd.read_csv("data/cleaned_data.csv")

# Create charts folder
os.makedirs("charts", exist_ok=True)


# 1. Sales by Category
sales_by_category = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
sales_by_category.plot(kind="bar")
plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/sales_by_category.png")
plt.show()
plt.close()


# 2. Profit by Category
profit_by_category = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
profit_by_category.plot(kind="bar")
plt.title("Profit by Category")
plt.xlabel("Category")
plt.ylabel("Profit")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/profit_by_category.png")
plt.show()
plt.close()


# 3. Sales by City
sales_by_city = df.groupby("City")["Sales"].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
sales_by_city.plot(kind="bar")
plt.title("Sales by City")
plt.xlabel("City")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/sales_by_city.png")
plt.show()
plt.close()


# 4. Sales by Payment Method
payment_sales = df.groupby("Payment_Method")["Sales"].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
payment_sales.plot(kind="bar")
plt.title("Sales by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/sales_by_payment_method.png")
plt.show()
plt.close()


# 5. Discount vs Profit
discount_profit = df.groupby("Discount")["Profit"].sum()

plt.figure(figsize=(8, 5))
discount_profit.plot(kind="line", marker="o")
plt.title("Discount vs Profit")
plt.xlabel("Discount")
plt.ylabel("Profit")
plt.tight_layout()
plt.savefig("charts/discount_vs_profit.png")
plt.show()
plt.close()


print("All charts created and saved successfully!")
