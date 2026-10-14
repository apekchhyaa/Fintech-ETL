from pathlib import Path
import pandas as pd


output_folder = Path("output")

customers = pd.read_csv(
    output_folder / "customers_clean.csv"
)

merchants = pd.read_csv(
    output_folder / "merchants_clean.csv"
)

transactions = pd.read_csv(
    output_folder / "transactions_clean.csv"
)

# Join customer information
enriched_transactions = transactions.merge(
    customers,
    on="customer_id",
    how="left",
    suffixes=("", "_customer")
)

# Join merchant information
enriched_transactions = enriched_transactions.merge(
    merchants,
    on="merchant_id",
    how="left",
    suffixes=("", "_merchant")
)

print("Enriched transactions shape:")
print(enriched_transactions.shape)

print("\nMissing values after joins:")
print(enriched_transactions.isna().sum())

enriched_transactions.to_csv(
    output_folder / "transactions_enriched.csv",
    index=False
)

print("\nSaved:")
print("output/transactions_enriched.csv")