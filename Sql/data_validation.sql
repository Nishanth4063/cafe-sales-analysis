USE Cafe_Sales_Analytics;
GO

-- 1. Row count (expect 9974)
SELECT COUNT(*) AS Total_Rows FROM cafe_sales_cleaned;

-- 2. Column types
SELECT COLUMN_NAME, DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'cafe_sales_cleaned';

-- 3. Duplicate transaction IDs (expect 0 rows)
SELECT Transaction_ID, COUNT(*) AS Duplicate_Count
FROM cafe_sales_cleaned
GROUP BY Transaction_ID
HAVING COUNT(*) > 1;

-- 4. Missing IDs or totals (expect 0 rows)
SELECT *
FROM cafe_sales_cleaned
WHERE Transaction_ID IS NULL OR Corrected_Total_Spent IS NULL;

-- 5. Quantity x Price must equal Total (expect 0)
SELECT COUNT(*) AS Wrong_Rows
FROM cafe_sales_cleaned
WHERE Quantity * Price_Per_Unit <> Corrected_Total_Spent;

-- 6. Date range and revenue (expect 2023-01-01, 2023-12-31, 89042.00)
SELECT MIN(Transaction_Date) AS First_Date,
       MAX(Transaction_Date) AS Last_Date,
       SUM(Corrected_Total_Spent) AS Overall_Revenue
FROM cafe_sales_cleaned;