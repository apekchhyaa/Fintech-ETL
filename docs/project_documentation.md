# Fintech ETL Pipeline Project Documentation

## 1. Project overview

This project builds a local, sequential batch ETL pipeline for synthetic fintech data. It reads customer, merchant, and transaction CSV files, cleans the records, enriches transactions with customer and merchant information, generates insight reports, and produces a written findings document.

The data is synthetic. The results demonstrate an analytics workflow and should not be interpreted as real customer or banking activity.

## 2. Source data and objective

The input files are `customers.csv`, `merchants.csv`, and `transactions_raw.csv`. The project answers questions about daily activity, payment channels, customer spending, merchant categories, transaction statuses, and fraud-labelled activity.

The relationships are:

```text
transactions.customer_id -> customers.customer_id
transactions.merchant_id  -> merchants.merchant_id
```

## 3. Project structure

```text
fintech-project/
├── data/
│   ├── customers.csv
│   ├── merchants.csv
│   └── transactions_raw.csv
├── src/
│   ├── inspect_data.py
│   ├── clean_data.py
│   ├── enrich_data.py
│   ├── generate_insights.py
│   ├── generate_finding.py
│   └── run_pipeline.py
├── output/
├── docs/
└── .venv/
```

## 4. Initial inspection

`inspect_data.py` loads each CSV and reports sample rows, shapes, missing values, duplicate rows, duplicate IDs, channels, statuses, and fraud labels.

Original sizes:

```text
Customers: 5,000 rows and 5 columns
Merchants: 300 rows and 3 columns
Transactions: 202,000 rows and 10 columns
```

Initial findings:

- Customers had no missing values.
- Merchants had no missing values.
- Transactions had 3,954 missing city values.
- There were 2,000 duplicate transaction rows and IDs.
- Channel names had inconsistent capitalization and whitespace.
- Statuses were `success`, `failed`, and `reversed`.
- Original fraud labels were 199,854 non-fraud and 2,146 fraud-labelled transactions.

## 5. Issues encountered and fixes

### Missing city values

The 3,954 missing cities were replaced with `Unknown` because the transaction records remained useful.

### Duplicate transactions

Duplicate transaction IDs were removed by keeping the first row for each `txn_id`.

### Inconsistent text fields

Identifier whitespace was removed. Channels were trimmed and converted to uppercase. Statuses were trimmed and converted to lowercase.

### Timestamp parsing

Initial strict parsing created apparent missing timestamps. Parsing with `format="mixed"` successfully converted all timestamps, so the final timestamp and transaction-date missing counts were zero.

### Negative amounts

There were 982 negative transaction amounts. They were reported before filtering and then removed because amounts should be non-negative for this analysis.

## 6. Cleaning process

`clean_data.py` loads the raw files, fills missing cities, cleans identifiers, standardizes text fields, converts timestamps and amounts, removes incomplete records, removes negative amounts, removes duplicate transaction IDs, creates `transaction_date`, and saves cleaned files.

Final cleaning result:

```text
Customers: 5,000
Merchants: 300
Transactions: 199,033
Missing values in final transaction data: 0
```

Outputs:

```text
output/customers_clean.csv
output/merchants_clean.csv
output/transactions_clean.csv
```

## 7. Enrichment process

`enrich_data.py` performs left joins from transactions to customers using `customer_id`, and from transactions to merchants using `merchant_id`.

The result was:

```text
199,033 rows and 17 columns
```

All customer and merchant joins matched successfully, with zero missing values after the joins.

Output:

```text
output/transactions_enriched.csv
```

## 8. Insight generation

`generate_insights.py` creates:

```text
output/daily_summary.csv
output/channel_summary.csv
output/customer_summary.csv
output/category_summary.csv
output/status_summary.csv
output/fraud_summary.csv
```

These reports describe daily activity, channel performance, customer activity, merchant-category performance, status distribution, and fraud-labelled activity.

## 9. Pipeline

The pipeline runs the stages in order:

```text
inspect_data.py
    ↓
clean_data.py
    ↓
enrich_data.py
    ↓
generate_insights.py
    ↓
generate_finding.py
```

It is a local sequential batch ETL pipeline: it processes files on one computer, one stage at a time. It is suitable for this project but is not a production system with cloud storage, scheduling, monitoring, or alerting.

Run it with:

```bash
source .venv/bin/activate
python src/run_pipeline.py
```

## 11. Limitations

- The data is synthetic.
- It does not represent real customers or financial institutions.
- Fraud labels are simulated.
- The analysis identifies patterns but does not prove fraud.
- IDs are anonymized.
- The pipeline is a local prototype, not a production banking system.

## 12. Conclusion

The project implements a reproducible fintech ETL workflow. It extracts customer, merchant, and transaction records, validates and cleans the data, enriches transactions through relational joins, generates analytical reports, and produces written findings about transaction activity, payment channels, customer behavior, merchant categories, transaction status, and fraud-labelled activity.
