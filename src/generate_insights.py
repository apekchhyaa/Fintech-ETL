from pathlib import Path
import pandas as pd


output_folder = Path("output")

transactions = pd.read_csv(
    output_folder / "transactions_enriched.csv"
)

transactions["timestamp"] = pd.to_datetime(
    transactions["timestamp"]
)

transactions["amount"] = pd.to_numeric(
    transactions["amount"]
)

# Create a daily summary
daily_summary = (
    transactions
    .groupby("transaction_date")
    .agg(
        transaction_count=("txn_id", "count"),
        total_amount=("amount", "sum"),
        average_amount=("amount", "mean")
    )
    .reset_index()
)

# Create a channel summary
channel_summary = (
    transactions
    .groupby("channel")
    .agg(
        transaction_count=("txn_id", "count"),
        total_amount=("amount", "sum"),
        average_amount=("amount", "mean"),
        fraud_count=("is_fraud", "sum")
    )
    .reset_index()
)

# Create a customer summary
customer_summary = (
    transactions
    .groupby("customer_id")
    .agg(
        transaction_count=("txn_id", "count"),
        total_amount=("amount", "sum"),
        average_amount=("amount", "mean"),
        fraud_count=("is_fraud", "sum")
    )
    .reset_index()
    .sort_values("total_amount", ascending=False)
)

# Create a merchant-category summary
category_summary = (
    transactions
    .groupby("category")
    .agg(
        transaction_count=("txn_id", "count"),
        total_amount=("amount", "sum"),
        average_amount=("amount", "mean"),
        fraud_count=("is_fraud", "sum")
    )
    .reset_index()
    .sort_values("total_amount", ascending=False)
)

# Create a status summary
status_summary = (
    transactions
    .groupby("status")
    .agg(
        transaction_count=("txn_id", "count"),
        total_amount=("amount", "sum"),
        average_amount=("amount", "mean")
    )
    .reset_index()
)

# Create a fraud summary
fraud_summary = (
    transactions
    .groupby("is_fraud")
    .agg(
        transaction_count=("txn_id", "count"),
        total_amount=("amount", "sum"),
        average_amount=("amount", "mean")
    )
    .reset_index()
)

# Save reports
daily_summary.to_csv(
    output_folder / "daily_summary.csv",
    index=False
)

channel_summary.to_csv(
    output_folder / "channel_summary.csv",
    index=False
)

customer_summary.to_csv(
    output_folder / "customer_summary.csv",
    index=False
)

category_summary.to_csv(
    output_folder / "category_summary.csv",
    index=False
)

status_summary.to_csv(
    output_folder / "status_summary.csv",
    index=False
)

fraud_summary.to_csv(
    output_folder / "fraud_summary.csv",
    index=False
)

print("Insight reports created successfully.")