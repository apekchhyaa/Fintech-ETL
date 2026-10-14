from pathlib import Path
import pandas as pd


output_folder = Path("output")
docs_folder = Path("docs")

# Create the docs folder automatically if it does not exist
docs_folder.mkdir(exist_ok=True)

# Read generated reports
daily = pd.read_csv(output_folder / "daily_summary.csv")
channels = pd.read_csv(output_folder / "channel_summary.csv")
customers = pd.read_csv(output_folder / "customer_summary.csv")
categories = pd.read_csv(output_folder / "category_summary.csv")
statuses = pd.read_csv(output_folder / "status_summary.csv")
fraud = pd.read_csv(output_folder / "fraud_summary.csv")

# Find important results
busiest_day = daily.loc[
    daily["transaction_count"].idxmax()
]

top_channel_by_count = channels.loc[
    channels["transaction_count"].idxmax()
]

top_channel_by_amount = channels.loc[
    channels["total_amount"].idxmax()
]

top_category = categories.loc[
    categories["total_amount"].idxmax()
]

top_customer = customers.loc[
    customers["total_amount"].idxmax()
]

top_status = statuses.loc[
    statuses["transaction_count"].idxmax()
]

# Find fraud totals
non_fraud_row = fraud[fraud["is_fraud"] == 0].iloc[0]
fraud_row = fraud[fraud["is_fraud"] == 1].iloc[0]

total_transactions = fraud["transaction_count"].sum()
fraud_transactions = fraud_row["transaction_count"]
fraud_rate = (fraud_transactions / total_transactions) * 100

# Create the document
findings = f"""# Fintech Transaction Insights

## Dataset summary

The cleaned dataset contains:

- {total_transactions:,.0f} transactions
- 5,000 customers
- 300 merchants

## Daily activity

The busiest transaction date was **{busiest_day["transaction_date"]}**,
with **{busiest_day["transaction_count"]:,.0f} transactions** and a total
amount of **{busiest_day["total_amount"]:,.2f}**.

## Payment channels

The most frequently used payment channel was **{top_channel_by_count["channel"]}**,
with **{top_channel_by_count["transaction_count"]:,.0f} transactions**.

The channel with the highest total transaction value was
**{top_channel_by_amount["channel"]}**, with a total amount of
**{top_channel_by_amount["total_amount"]:,.2f}**.

## Merchant categories

The merchant category with the highest transaction value was
**{top_category["category"]}**, with a total amount of
**{top_category["total_amount"]:,.2f}**.

## Customer activity

The customer with the highest total transaction value was
**{top_customer["customer_id"]}**, with a total amount of
**{top_customer["total_amount"]:,.2f}**.

## Transaction statuses

The most common transaction status was **{top_status["status"]}**,
with **{top_status["transaction_count"]:,.0f} transactions**.

## Fraud

There were **{fraud_transactions:,.0f} fraud-labelled transactions** and
**{non_fraud_row["transaction_count"]:,.0f} non-fraud transactions**.

The overall fraud rate was approximately **{fraud_rate:.2f}%**.

## Conclusion

The ETL pipeline cleaned and combined customer, merchant, and transaction
data. It produced insights about daily activity, payment channels,
customers, merchant categories, transaction statuses, and
fraud-labelled transactions.

The data is synthetic, so these findings demonstrate an analysis workflow
rather than real-world banking behavior.
"""

# Save the document
findings_file = docs_folder / "findings.md"
findings_file.write_text(findings, encoding="utf-8")

print(f"Findings document created: {findings_file}")