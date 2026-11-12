# Cafe Sales Data Cleaning & Dashboard

Cleaning a messy cafe sales dataset with Python (pandas), checking it with SQL Server, and showing the results in Power BI.

![Dashboard Preview](dashboard/dashboard_preview.png)

## Data

- Source: [Cafe Sales - Dirty Data for Cleaning Training](https://www.kaggle.com/datasets/ahmedmohamed2003/cafe-sales-dirty-data-for-cleaning-training) (Kaggle)
- 10,000 transactions from 2023
- Problems in the raw data: `ERROR` and `UNKNOWN` text, blank cells, and wrong or missing Quantity, Price and Total Spent

## Cleaning rules

The main rule: **don't guess.** A missing value is filled only when the same row gives the answer.

| Problem | What I did |
|---|---|
| Missing Price | Taken from the Item (each item has one price), or from Total ÷ Quantity |
| Missing Item | Taken from the Price only if that price belongs to one item. Prices 3 and 4 match two items each, so those stay `Unknown` |
| Missing Quantity | Total ÷ Price, only if the result is a whole number from 1 to 5 |
| Missing Total | Quantity × Price |
| Missing Item / Payment Method / Location | Marked `Unknown` |
| Blank dates (460) | Left blank |
| Rows with no way to find Quantity or Total (26) | Dropped |

Result: **9,974 rows**, no duplicate IDs, Quantity always 1 to 5, and Quantity × Price = Total for every row. Where the raw file already had a Total, the script never changed it.

## What I learned

My first version filled missing Payment Method and Location with the most common value. This made Digital Wallet look like the top payment method (5,469 orders) and Takeaway the top location (6,983 orders).

In the raw data, the known values are almost equal. The fake trend came from the filling. So I changed the approach and kept `Unknown` instead.

## Results

- Total revenue: **89,042** (9,974 orders)
- Date range: 01 Jan 2023 to 31 Dec 2023

**Revenue by item**

| Item | Revenue |
|---|---|
| Salad | 19,095 |
| Sandwich | 13,716 |
| Smoothie | 13,344 |
| Juice | 10,515 |
| Cake | 10,404 |
| Coffee | 7,808 |
| Tea | 5,475 |
| Cookie | 3,598 |
| Unknown | 5,087 |

**Payment method (known orders only):** Digital Wallet 2,284, Credit Card 2,268, Cash 2,254. All three are almost equal, so there is no clear winner.

**Location (known orders only):** Takeaway 3,016, In-store 3,006. Also almost equal.

## Limits

- Unknown values are a big part of the data: Payment Method 31.8%, Location 39.6%, Item 4.8%. The payment and location results are based only on the known orders. The dashboard shows Unknown in grey.
- I assume the missing values are random. The data can't prove this.
- 26 rows were dropped, and 460 dates are blank, so date charts leave those out.

## Project structure

```
cafe-sales-analysis/
├── data/
│   ├── dirty_cafe_sales.csv        # raw data
│   └── cafe_sales_cleaned.csv      # output of the script
├── python/
│   └── cafe_cleaning.py            # cleaning script
├── Sql/
│   └── data_validation.sql         # checks in SQL Server
├── PowerBI/
│   └── Cafe_Sales_Analysis_Dashboard.pbix
├── dashboard/
│   └── dashboard_preview.png       # dashboard screenshot
└── README.md
```

## How to run

1. Install the libraries: `pip install pandas numpy`
2. Run the script:
   ```
   cd python
   python cafe_cleaning.py
   ```
   It prints the checks and saves `data/cafe_sales_cleaned.csv`.
3. In SQL Server, import `data/cafe_sales_cleaned.csv` as the table `cafe_sales_cleaned` in the database `Cafe_Sales_Analytics`. Keep Price and Total as decimal, not int. Then run `Sql/data_validation.sql`.
4. Open `PowerBI/Cafe_Sales_Analysis_Dashboard.pbix` in Power BI Desktop. If the data path is different on your computer, change it in Transform data → Data source settings.

## Tools

Python, pandas, NumPy, SQL Server, Power BI