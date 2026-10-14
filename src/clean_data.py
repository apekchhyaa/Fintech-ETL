from pathlib import Path
import pandas as pd


data_folder = Path("data")
output_folder = Path("output")
output_folder.mkdir(exist_ok=True)

customers = pd.read_csv(data_folder / "customers.csv")
merchants = pd.read_csv(data_folder / "merchants.csv")
transactions = pd.read_csv(data_folder / "transactions_raw.csv")

# Fill missing transaction cities
transactions["city"] = transactions["city"].fillna("Unknown")

print("Missing cities after cleaning:")
print(transactions["city"].isna().sum())

print("\nExample city values:")
print(transactions["city"].head(10))


# Clean identifier columns
transactions["txn_id"] = (
    transactions["txn_id"]
    .astype("string")
    .str.strip()
)

transactions["customer_id"] = (
    transactions["customer_id"]
    .astype("string")
    .str.strip()
)

transactions["merchant_id"] = (
    transactions["merchant_id"]
    .astype("string")
    .str.strip()
)

transactions["device_id"] = (
    transactions["device_id"]
    .astype("string")
    .str.strip()
)

# Standardize payment channels
transactions["channel"] = (
    transactions["channel"]
    .astype("string")
    .str.strip()
    .str.upper()
)

# Standardize transaction statuses
transactions["status"] = (
    transactions["status"]
    .astype("string")
    .str.strip()
    .str.lower()
)

transactions["timestamp"] = pd.to_datetime(
    transactions["timestamp"],
    errors="coerce",
    format="mixed"
)

# Convert amount to numeric
transactions["amount"] = pd.to_numeric(
    transactions["amount"],
    errors="coerce"
)

transactions = transactions.dropna(
    subset=[
        "txn_id",
        "customer_id",
        "merchant_id",
        "timestamp",
        "amount",
        "channel",
        "status",
        "is_fraud",
    ]
)

print(
    "Negative amounts:",
    (transactions["amount"] < 0).sum()
)

# Remove negative transaction amounts
transactions = transactions[transactions["amount"] >= 0]

# Keep only one row for each transaction ID
transactions = transactions.drop_duplicates(
    subset=["txn_id"],
    keep="first"
)

# Create a separate date column
transactions["transaction_date"] = (
    transactions["timestamp"].dt.date
)


# Save cleaned files
customers.to_csv(
    output_folder / "customers_clean.csv",
    index=False
)

merchants.to_csv(
    output_folder / "merchants_clean.csv",
    index=False
)

transactions.to_csv(
    output_folder / "transactions_clean.csv",
    index=False
)

print("Cleaning complete.")
print("Customers:", len(customers))
print("Merchants:", len(merchants))
print("Transactions after cleaning:", len(transactions))

print("\nCleaned channels:")
print(transactions["channel"].value_counts())

print("\nCleaned statuses:")
print(transactions["status"].value_counts())

print("\nMissing transaction values:")
print(transactions.isna().sum())