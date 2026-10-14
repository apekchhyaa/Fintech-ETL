from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


output_folder = Path("output")
charts_folder = output_folder / "charts"

charts_folder.mkdir(exist_ok=True)

transactions = pd.read_csv(
    output_folder / "transactions_enriched.csv"
)

transactions["timestamp"] = pd.to_datetime(
    transactions["timestamp"]
)

transactions["amount"] = pd.to_numeric(
    transactions["amount"]
)

# 1. Daily transaction count
daily_summary = (
    transactions
    .groupby("transaction_date")
    .agg(
        transaction_count=("txn_id", "count"),
        total_amount=("amount", "sum")
    )
    .reset_index()
)

plt.figure(figsize=(12, 6))
plt.plot(
    daily_summary["transaction_date"],
    daily_summary["transaction_count"]
)

plt.title("Daily Transaction Count")
plt.xlabel("Date")
plt.ylabel("Number of Transactions")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(charts_folder / "daily_transaction_count.png")
plt.close()

# 2. Total amount by payment channel
channel_summary = (
    transactions
    .groupby("channel")
    .agg(total_amount=("amount", "sum"))
    .reset_index()
    .sort_values("total_amount", ascending=False)
)

plt.figure(figsize=(8, 5))
plt.bar(
    channel_summary["channel"],
    channel_summary["total_amount"]
)

plt.title("Total Transaction Amount by Channel")
plt.xlabel("Payment Channel")
plt.ylabel("Total Amount")
plt.tight_layout()
plt.savefig(charts_folder / "amount_by_channel.png")
plt.close()

# 3. Total amount by merchant category
category_summary = (
    transactions
    .groupby("category")
    .agg(total_amount=("amount", "sum"))
    .reset_index()
    .sort_values("total_amount", ascending=False)
)

plt.figure(figsize=(10, 6))
plt.bar(
    category_summary["category"],
    category_summary["total_amount"]
)

plt.title("Total Transaction Amount by Merchant Category")
plt.xlabel("Merchant Category")
plt.ylabel("Total Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(charts_folder / "amount_by_category.png")
plt.close()

# 4. Fraud rate by payment channel
fraud_summary = (
    transactions
    .groupby("channel")
    .agg(
        total_transactions=("txn_id", "count"),
        fraud_transactions=("is_fraud", "sum")
    )
    .reset_index()
)

fraud_summary["fraud_rate"] = (
    fraud_summary["fraud_transactions"]
    / fraud_summary["total_transactions"]
    * 100
)

plt.figure(figsize=(8, 5))
plt.bar(
    fraud_summary["channel"],
    fraud_summary["fraud_rate"]
)

plt.title("Fraud Rate by Payment Channel")
plt.xlabel("Payment Channel")
plt.ylabel("Fraud Rate (%)")
plt.tight_layout()
plt.savefig(charts_folder / "fraud_rate_by_channel.png")
plt.close()

print("Charts created successfully.")
print(f"Charts saved in: {charts_folder}")