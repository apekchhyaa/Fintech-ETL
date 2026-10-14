from pathlib import Path
import pandas as pd

data_folder = Path("data")

customers = pd.read_csv(data_folder / "customers.csv")
merchants = pd.read_csv(data_folder / "merchants.csv")
transactions = pd.read_csv(data_folder / "transactions_raw.csv")

print("Customers:")
print(customers.head())

print("\nMerchants:")
print(merchants.head())

print("\nTransactions:")
print(transactions.head())

print("\nCustomers shape:")
print(customers.shape)

print("\nMerchants shape:")
print(merchants.shape)

print("\nTransactions shape:")
print(transactions.shape)


print("\nMissing values in customers:")
print(customers.isna().sum())

print("\nMissing values in merchants:")
print(merchants.isna().sum())

print("\nMissing values in transactions:")
print(transactions.isna().sum())

print("\nDuplicate customer rows:")
print(customers.duplicated().sum())

print("\nDuplicate merchant rows:")
print(merchants.duplicated().sum())

print("\nDuplicate transaction rows:")
print(transactions.duplicated().sum())

print("\nDuplicate transaction IDs:")
print(transactions["txn_id"].duplicated().sum())

print("\nTransaction channels:")
print(transactions["channel"].value_counts())

print("\nTransaction statuses:")
print(transactions["status"].value_counts())

print("\nFraud labels:")
print(transactions["is_fraud"].value_counts())

print(
    "Negative amounts:",
    (transactions["amount"] < 0).sum()
)
