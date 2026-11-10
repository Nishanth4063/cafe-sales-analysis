# Cafe Sales Data Cleaning & Dashboard

![Dashboard Preview](dashboard/dashboard_preview.png)

## Overview
This is a data analysis portfolio project based on the [Dirty Cafe Sales dataset from Kaggle](https://www.kaggle.com/). It demonstrates how to clean unstructured data in Python, validate the results using SQL, and build a Power BI dashboard to analyze revenue and transaction volume. 

The core focus of this project is data integrity. Instead of fabricating data through statistical mode/median imputation, missing or erroneous values are deduced mathematically where possible, labeled strictly as "Unknown", or dropped if unrecoverable.

## Tech Stack
* **Data Cleaning:** Python (Pandas, NumPy)
* **Validation:** SQL Server
* **Visualization:** Power BI

## Project Structure
```text
cafe-sales-analysis/
│
├── data/
│   ├── dirty_cafe_sales.csv            # Raw dataset (10,000 rows)
│   └── cafe_sales_cleaned.xlsx         # Cleaned output dataset (9,974 valid rows)
│
├── python/
│   └── cafe_cleaning.py                # Python data cleaning script
│
├── Sql/
│   └── data_validation.sql             # SQL queries for basic integrity checks
│
├── dashboard/
│   └── dashboard_preview.png           # Dashboard screenshot
│
├── PowerBI/
│   └── Cafe_Sales_Analysis_Dashboard.pbix
│
└── README.md
```

## Data Cleaning Methodology
The raw dataset contained missing fields, invalid string formats (`ERROR`, `UNKNOWN`), and broken dates. The `cafe_cleaning.py` script enforces strict data governance:
1. **Categorical Standardization:** Replaced text errors and blanks with a distinct `Unknown` label. Mode imputation was intentionally avoided to prevent skewing business metrics.
2. **Strict Item Mapping:** Mapped missing items based on price *only* when a price corresponded to exactly one item on the menu. 
3. **Mathematical Deduction:** 
   * Calculated missing `Quantity` using `Total Spent / Price Per Unit`.
   * Calculated missing `Price Per Unit` using `Total Spent / Quantity`.
4. **Business Rule Enforcement:** Nullified mathematically deduced quantities that exceeded the store maximum (5 per transaction). 
5. **Honest Dates:** Coerced invalid dates to nulls rather than fabricating timelines via forward-filling.

## Dashboard Insights
The Power BI dashboard visualizes the 9,974 rigorously cleaned records, tracking $89.04K in valid revenue. By preserving `Unknown` categorizations, the dashboard provides a highly accurate, auditable view of payment methods and location distributions without artificial inflation.

## How to Run
1. **Run the Data Pipeline:** 
   Navigate to the `python/` directory and execute the script.
   ```bash
   cd python
   python cafe_cleaning.py
   ```
2. **View the Dashboard:**
   Open `PowerBI/Cafe_Sales_Analysis_Dashboard.pbix` in Power BI Desktop and interact with the latest cleaned data.