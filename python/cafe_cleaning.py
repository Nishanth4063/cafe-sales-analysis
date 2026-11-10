from pathlib import Path

import numpy as np
import pandas as pd

# 0. Find the raw file (next to this script, or in ../data/, or ./data/)
HERE = Path(__file__).resolve().parent
candidates = [
    HERE / "dirty_cafe_sales.csv",
    HERE.parent / "data" / "dirty_cafe_sales.csv",
    HERE / "data" / "dirty_cafe_sales.csv",
]
RAW = next((p for p in candidates if p.exists()), None)
if RAW is None:
    raise FileNotFoundError("dirty_cafe_sales.csv not found. Put it in the data/ folder.")
OUT = RAW.parent / "cafe_sales_cleaned.csv"

# 1. Load and turn placeholder text into real blanks (NaN)
df = pd.read_csv(RAW)
rows_start = len(df)
df = df.replace(["ERROR", "UNKNOWN", "Unknown", "unknown", ""], np.nan)

# 2. Make the number columns real numbers
for col in ["Quantity", "Price Per Unit", "Total Spent"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

original_total = df["Total Spent"].copy()

# Quantity can only be a whole number from 1 to 5
bad_qty = df["Quantity"].notna() & ~(
    (df["Quantity"] % 1 == 0) & df["Quantity"].between(1, 5)
)
df.loc[bad_qty, "Quantity"] = np.nan

# 3. Lookup tables from rows where Item and Price are both known
known = df.dropna(subset=["Item", "Price Per Unit"])
item_to_price = known.groupby("Item")["Price Per Unit"].agg(lambda s: s.mode()[0])
items_per_price = known.groupby("Price Per Unit")["Item"].unique()
price_to_item = {p: items[0] for p, items in items_per_price.items() if len(items) == 1}
valid_prices = set(known["Price Per Unit"].unique())

# 4. Fill missing values, only when the row itself gives the answer
# 4a. Price from Item
m = df["Price Per Unit"].isna() & df["Item"].notna()
df.loc[m, "Price Per Unit"] = df.loc[m, "Item"].map(item_to_price)

# 4b. Price from Total / Quantity (only if it is a real menu price)
m = df["Price Per Unit"].isna() & df["Total Spent"].notna() & df["Quantity"].notna()
price_guess = df.loc[m, "Total Spent"] / df.loc[m, "Quantity"]
df.loc[m, "Price Per Unit"] = price_guess.where(price_guess.isin(valid_prices))

# 4c. Item from Price (only when that price belongs to exactly one item)
m = df["Item"].isna() & df["Price Per Unit"].notna()
df.loc[m, "Item"] = df.loc[m, "Price Per Unit"].map(price_to_item)

# 4d. Quantity from Total / Price (only if whole number from 1 to 5)
m = df["Quantity"].isna() & df["Total Spent"].notna() & df["Price Per Unit"].notna()
qty_guess = df.loc[m, "Total Spent"] / df.loc[m, "Price Per Unit"]
valid_qty = (qty_guess % 1 == 0) & qty_guess.between(1, 5)
df.loc[m, "Quantity"] = qty_guess.where(valid_qty)

# 4e. Total from Quantity x Price
m = df["Total Spent"].isna() & df["Quantity"].notna() & df["Price Per Unit"].notna()
df.loc[m, "Total Spent"] = df.loc[m, "Quantity"] * df.loc[m, "Price Per Unit"]

# 5. Text columns still blank become "Unknown" (no mode filling)
for col in ["Item", "Payment Method", "Location"]:
    df[col] = df[col].fillna("Unknown")

# 6. Drop rows that cannot be recovered
before = len(df)
df = df.dropna(subset=["Quantity", "Price Per Unit", "Total Spent"]).copy()
rows_dropped = before - len(df)
df["Quantity"] = df["Quantity"].astype(int)

# 7. Dates: keep blank dates blank
df["Transaction Date"] = pd.to_datetime(df["Transaction Date"], errors="coerce")

# 8. Same column name your SQL and Power BI use
df = df.rename(columns={"Total Spent": "Corrected Total Spent"})

# 9. Validation (these checks can really fail)
orig = original_total.loc[df.index]
has_orig = orig.notna()
math_wrong = (~np.isclose(
    df["Quantity"] * df["Price Per Unit"], df["Corrected Total Spent"]
)).sum()
changed_known_total = (~np.isclose(
    df.loc[has_orig, "Corrected Total Spent"], orig[has_orig]
)).sum()

print("Raw rows              :", rows_start)
print("Rows dropped          :", rows_dropped)
print("Final rows            :", len(df))
print("Duplicate IDs         :", df["Transaction ID"].duplicated().sum())
print("Blank dates (kept)    :", df["Transaction Date"].isna().sum())
print("Quantity min / max    :", df["Quantity"].min(), "/", df["Quantity"].max())
print("Qty x Price != Total  :", math_wrong, "(want 0)")
print("Original Total changed:", changed_known_total, "(want 0)")
print("Total revenue         :", round(df["Corrected Total Spent"].sum(), 2))
print()
print(df["Payment Method"].value_counts())
print()
print(df["Location"].value_counts())
print()
print(df["Item"].value_counts())

# 10. Save
df.to_csv(OUT, index=False)
print("\nSaved:", OUT)