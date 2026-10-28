import pandas as pd

# Load the raw dataset
df = pd.read_csv("data/raw_data.csv")

print("Original rows:", len(df))
print("Original columns:", len(df.columns))

# Check missing values
print("\nMissing values before cleaning:")
print(df.isnull().sum())

# Check duplicate rows
print("\nDuplicate rows before cleaning:", df.duplicated().sum())

# Check category values before cleaning
print("\nCategory values before cleaning:")
print(df["Category"].unique())


# -------------------------------
# DATA CLEANING
# -------------------------------

# 1. Remove duplicate rows
df = df.drop_duplicates()

# 2. Clean category names
df["Category"] = df["Category"].str.strip().str.title()

# 3. Fill missing customer names
df["Customer_Name"] = df["Customer_Name"].fillna("Unknown")

# 4. Fill missing cities
df["City"] = df["City"].fillna("Unknown")

# 5. Fill missing ages with the average age
df["Age"] = df["Age"].fillna(df["Age"].mean())


# -------------------------------
# SAVE CLEANED DATA
# -------------------------------

df.to_csv("data/cleaned_data.csv", index=False)

print("\nCleaning completed!")
print("Rows after cleaning:", len(df))

print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nDuplicate rows after cleaning:", df.duplicated().sum())

print("\nCategory values after cleaning:")
print(df["Category"].unique())

print("\nCleaned dataset saved as cleaned_data.csv")