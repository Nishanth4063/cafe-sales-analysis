import pandas as pd
import numpy as np

# 1. Load Data
df = pd.read_excel('cafe_sales_10k_cleaned.xlsx')

# 2. Standardize garbage/placeholder values to Nulls (NaN)
invalid_values = ['UNKNOWN', 'unknown', 'ERROR', 'Not Specified', '']
df['Item'] = df['Item'].replace(invalid_values, np.nan)
df['Payment Method'] = df['Payment Method'].replace(invalid_values, np.nan)
df['Location'] = df['Location'].replace(invalid_values, np.nan)

# 3. Clean Numerical Columns (Safely coerces strings like 'ERROR' to NaN)
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
df['Price Per Unit'] = pd.to_numeric(df['Price Per Unit'], errors='coerce')
total_spent_num = pd.to_numeric(df['Corrected Total Spent'], errors='coerce')

# 4. REVERSE IMPUTATION (Price -> Item)
known_items = df.dropna(subset=['Item', 'Price Per Unit'])
price_to_item_map = known_items.groupby('Price Per Unit')['Item'].apply(lambda x: x.mode()[0]).to_dict()

missing_item_mask = df['Item'].isna() & df['Price Per Unit'].notna()
df.loc[missing_item_mask, 'Item'] = df.loc[missing_item_mask, 'Price Per Unit'].map(price_to_item_map)

# 5. FORWARD IMPUTATION (Item -> Price)
item_prices = df.groupby('Item')['Price Per Unit'].median()
df['Price Per Unit'] = df['Price Per Unit'].fillna(df['Item'].map(item_prices))

# 6. Fallbacks for completely unmappable rows
df['Price Per Unit'] = df['Price Per Unit'].fillna(df['Price Per Unit'].median())
df['Item'] = df['Item'].fillna('Others')

# 7. Mode Imputation for Categorical Data
df['Payment Method'] = df['Payment Method'].fillna(df['Payment Method'].mode()[0])
df['Location'] = df['Location'].fillna(df['Location'].mode()[0])

# 8. Mathematically Impute Missing Quantities
missing_qty_mask = df['Quantity'].isna()
df.loc[missing_qty_mask, 'Quantity'] = (total_spent_num[missing_qty_mask] / df.loc[missing_qty_mask, 'Price Per Unit']).round()
df['Quantity'] = df['Quantity'].fillna(df['Quantity'].median()).round().astype(int)

# 9. Recalculate Corrected Total Spent reliably
df['Corrected Total Spent'] = (df['Quantity'] * df['Price Per Unit']).round(2)

# 10. Format Transaction Dates
df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], errors='coerce')
df['Transaction Date'] = df['Transaction Date'].ffill()

# 11. Export Clean Data
df.to_excel('cafe_sales_10k_final.xlsx', index=False)
print("Pipeline Execution Complete. Clean Data Saved to cafe_sales_10k_final.xlsx.")