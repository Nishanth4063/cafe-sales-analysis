use Cafe_Sales_Analytics
go
select count(*) from cafe_sales_10k_cleaned

select * from cafe_sales_10k_cleaned


SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'cafe_sales_10k_cleaned';

SELECT Transaction_ID, COUNT(*) AS Duplicate_Count
FROM cafe_sales_10k_cleaned
GROUP BY Transaction_ID
HAVING COUNT(*) > 1;

SELECT *
FROM cafe_sales_10k_cleaned
WHERE Transaction_ID IS NULL 
   OR Corrected_Total_Spent IS NULL;

SELECT 
    MIN([Transaction_Date]) AS First_Transaction_Date, 
    MAX([Transaction_Date]) AS Last_Transaction_Date, 
    SUM([Corrected_Total_Spent]) AS Overall_Revenue
FROM cafe_sales_10k_cleaned;
