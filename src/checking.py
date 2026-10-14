import pandas as pd

raw_transactions = pd.read_csv(
    "data/transactions_raw.csv"
)

parsed_timestamps = pd.to_datetime(
    raw_transactions["timestamp"],
    errors="coerce",
    format="mixed"
)

invalid_rows = raw_transactions[
    parsed_timestamps.isna()
]

print("Invalid timestamp count:", len(invalid_rows))
print(invalid_rows["timestamp"].value_counts(dropna=False).head(20))