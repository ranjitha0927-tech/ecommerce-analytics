import pandas as pd

# ============================================================
# 1. LOAD CLEANED DATASET
# ============================================================

df = pd.read_csv("data/cleaned_data.csv")

print("=" * 60)
print("E-COMMERCE CUSTOMER, SALES & PROFITABILITY ANALYTICS")
print("=" * 60)


# ============================================================
# 2. BASIC DATASET INFORMATION
# ============================================================

print("\nFIRST 5 ROWS:")
print(df.head())

print("\nDATASET SHAPE:")
print(df.shape)

print("\nCOLUMN NAMES:")
print(df.columns.tolist())

print("\nDATASET INFORMATION:")
df.info()

print("\nSUMMARY STATISTICS:")
print(df.describe())


# ============================================================
# 3. KEY BUSINESS METRICS
# ============================================================

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order_ID"].nunique()
total_quantity = df["Quantity"].sum()
average_order_value = df["Sales"].mean()
average_discount = df["Discount"].mean()
profit_margin = (total_profit / total_sales) * 100

print("\n" + "=" * 60)
print("KEY BUSINESS METRICS")
print("=" * 60)

print(f"Total Sales: ₹{total_sales:,.2f}")
print(f"Total Profit: ₹{total_profit:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Total Quantity Sold: {total_quantity:,}")
print(f"Average Order Value: ₹{average_order_value:,.2f}")
print(f"Average Discount: {average_discount:.2%}")
print(f"Overall Profit Margin: {profit_margin:.2f}%")


# ============================================================
# 4. SALES BY CATEGORY
# ============================================================

print("\n" + "=" * 60)
print("SALES BY CATEGORY")
print("=" * 60)

sales_by_category = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(sales_by_category)


# ============================================================
# 5. PROFIT BY CATEGORY
# ============================================================

print("\n" + "=" * 60)
print("PROFIT BY CATEGORY")
print("=" * 60)

profit_by_category = (
    df.groupby("Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

print(profit_by_category)


# ============================================================
# 6. CATEGORY PERFORMANCE
# ============================================================

print("\n" + "=" * 60)
print("CATEGORY PERFORMANCE")
print("=" * 60)

category_performance = df.groupby("Category").agg(
    Orders=("Order_ID", "nunique"),
    Quantity=("Quantity", "sum"),
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
)

category_performance["Profit_Margin_%"] = (
    category_performance["Profit"]
    / category_performance["Sales"]
    * 100
)

category_performance = category_performance.sort_values(
    "Sales",
    ascending=False
)

print(category_performance)


# ============================================================
# 7. SALES BY CITY
# ============================================================

print("\n" + "=" * 60)
print("SALES BY CITY")
print("=" * 60)

sales_by_city = (
    df.groupby("City")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(sales_by_city)


# ============================================================
# 8. PROFIT BY CITY
# ============================================================

print("\n" + "=" * 60)
print("PROFIT BY CITY")
print("=" * 60)

profit_by_city = (
    df.groupby("City")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

print(profit_by_city)


# ============================================================
# 9. TOP 10 CUSTOMERS
# ============================================================

print("\n" + "=" * 60)
print("TOP 10 CUSTOMERS BY SALES")
print("=" * 60)

top_customers = (
    df.groupby(["Customer_ID", "Customer_Name"])["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(top_customers)


# ============================================================
# 10. ORDERS BY ORDER STATUS
# ============================================================

print("\n" + "=" * 60)
print("ORDERS BY ORDER STATUS")
print("=" * 60)

orders_by_status = df.groupby("Order_Status").agg(
    Orders=("Order_ID", "nunique"),
    Sales=("Sales", "sum")
)

print(orders_by_status)


# ============================================================
# 11. SALES BY PAYMENT METHOD
# ============================================================

print("\n" + "=" * 60)
print("SALES BY PAYMENT METHOD")
print("=" * 60)

payment_analysis = df.groupby("Payment_Method").agg(
    Orders=("Order_ID", "nunique"),
    Sales=("Sales", "sum")
)

payment_analysis = payment_analysis.sort_values(
    "Sales",
    ascending=False
)

print(payment_analysis)


# ============================================================
# 12. DISCOUNT VS PROFIT
# ============================================================

print("\n" + "=" * 60)
print("DISCOUNT VS PROFIT")
print("=" * 60)

discount_analysis = df.groupby("Discount").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
)

discount_analysis["Profit_Margin_%"] = (
    discount_analysis["Profit"]
    / discount_analysis["Sales"]
    * 100
)

print(discount_analysis)


# ============================================================
# 13. SALES BY GENDER
# ============================================================

print("\n" + "=" * 60)
print("SALES BY GENDER")
print("=" * 60)

sales_by_gender = (
    df.groupby("Gender")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(sales_by_gender)


# ============================================================
# 14. AGE GROUP ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("SALES BY AGE GROUP")
print("=" * 60)

df["Age_Group"] = pd.cut(
    df["Age"],
    bins=[17, 24, 34, 44, 54, 100],
    labels=["18-24", "25-34", "35-44", "45-54", "55+"]
)

age_group_sales = (
    df.groupby("Age_Group", observed=False)["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(age_group_sales)


# ============================================================
# 15. TOTAL QUANTITY BY CATEGORY
# ============================================================

print("\n" + "=" * 60)
print("QUANTITY SOLD BY CATEGORY")
print("=" * 60)

quantity_by_category = (
    df.groupby("Category")["Quantity"]
    .sum()
    .sort_values(ascending=False)
)

print(quantity_by_category)


# ============================================================
# 16. MOST PROFITABLE CATEGORY
# ============================================================

most_profitable_category = profit_by_category.idxmax()
highest_sales_category = sales_by_category.idxmax()
highest_margin_category = category_performance["Profit_Margin_%"].idxmax()
best_city = sales_by_city.idxmax()

print("\n" + "=" * 60)
print("KEY FINDINGS")
print("=" * 60)

print(f"Highest Sales Category: {highest_sales_category}")
print(f"Highest Profit Category: {most_profitable_category}")
print(f"Highest Profit Margin Category: {highest_margin_category}")
print(f"Best Performing City by Sales: {best_city}")

print("\nAnalysis completed successfully!")