select * from customer
select * from exchange
select * from product
select * from sales
select * from stores;


/* QUESTION 1: 1. Which stores consistently achieve the highest sales volume, and how does this
vary by year and quarter?
○ Analyze store performance over time to identify trends in sales volume across
different periods */


WITH aggregated_sales AS (
    SELECT
        sales."StoreKey",
        EXTRACT(YEAR FROM sales."Order Date") AS year,
        EXTRACT(QUARTER FROM sales."Order Date") AS quarter,
        SUM(product."Unit Price USD" * sales."Quantity") AS total_sales
    FROM public.sales 
    JOIN public.product
        ON sales."ProductKey" = product."ProductKey"
    GROUP BY sales."StoreKey", year, quarter
)
SELECT
    "StoreKey",
    year,
    quarter,
    total_sales,
    RANK() OVER (
        PARTITION BY year, quarter 
        ORDER BY total_sales DESC
    ) AS sales_rank
FROM aggregated_sales
ORDER BY year, quarter, sales_rank;




/* QUESTION 2: What are the most profitable products in each region, and how do exchange rate
fluctuations impact profitability?
○ Evaluate product profitability by region, taking into account the effects of currency
exchange rates. */


WITH Profit_Calculation AS (
SELECT
    product."ProductKey" AS Product_ID,
    stores."Country" AS Region,
    SUM(product."Unit Price USD" * sales."Quantity" * exchange."Exchange" - product."Unit Cost USD" * sales."Quantity") AS profit
FROM
    public.product 
JOIN
    public.sales ON product."ProductKey" = sales."ProductKey"
JOIN 
    public.stores ON sales."StoreKey" = stores."StoreKey"
JOIN 
	public.exchange ON sales."Currency Code" = exchange."Currency"
WHERE
	exchange."Date"=sales."Order Date"
GROUP BY 
    product."ProductKey",
    stores."Country"
)
Select 
	Product_ID,
	Region,
	profit,
 	RANK() OVER ( ORDER BY profit DESC) AS Rank_Profit
From
	Profit_Calculation



	

/*Question 3: Which customer segments exhibit the highest repeat purchase behavior, and what
are the key factors driving loyalty?
○ Determine which customer demographics are most loyal and analyze the factors
contributing to repeat purchases.*/

WITH Repeat_Customers AS (
    SELECT 
        "CustomerKey",
        COUNT("Order Number") AS Purchase_Count
    FROM 
        public.sales
    GROUP BY 
        "CustomerKey"
    HAVING COUNT("Order Number") > 1  -- Identify customers with more than one purchase--
)
SELECT 
    customer."Gender",
    customer."Age",
    customer."Country",
    customer."Continent",
    Repeat_Customers.Purchase_Count,
    AVG(sales."Quantity") AS Avg_Purchase_Quantity,
    AVG(sales."Quantity" * product."Unit Price USD") AS Avg_Spending
FROM 
    Repeat_Customers
JOIN 
    public.customer ON Repeat_Customers."CustomerKey" = customer."CustomerKey"
JOIN 
    public.sales ON Repeat_Customers."CustomerKey" = sales."CustomerKey"
JOIN 
    public.product  ON sales."ProductKey" = product."ProductKey"
GROUP BY 
    customer."Gender", customer."Age", customer."Country", customer."Continent", Repeat_Customers.Purchase_Count
ORDER BY 
    Repeat_Customers.Purchase_Count DESC, Avg_Spending DESC;





/*Question 4:How do delivery delays impact sales performance, and what are the most common
causes of delays across different stores and regions?
○ Investigate the relationship between delivery delays and sales, identifying
patterns and causes of delays.*/


-- Analyze Impact of Delays on Sales and when there is no delay--
WITH Delivery_Delay AS (
    SELECT 
        sales."Order Number",
        sales."StoreKey",
        sales."CustomerKey",
        sales."ProductKey",
        stores."State" AS Region,         -- Assuming State is the region
        sales."Order Duration" AS Delay_Days, 
        sales."Quantity",
        sales."Currency Code",
        sales."Quantity" * product."Unit Price USD" AS Sale_Amount
    FROM 
        public.sales 
    JOIN 
        stores ON sales."StoreKey" = stores."StoreKey"   
    JOIN 
        Product  ON sales."ProductKey" = product."ProductKey" 
)
SELECT 
    AVG(CASE WHEN Delivery_Delay.Delay_Days > 0 THEN Delivery_Delay.Sale_Amount ELSE NULL END) AS Avg_Delayed_Sales,
    AVG(CASE WHEN Delivery_Delay.Delay_Days < 1 THEN Delivery_Delay.Sale_Amount ELSE NULL END) AS Avg_On_Time_Sales,
    COUNT(CASE WHEN Delivery_Delay.Delay_Days > 0 THEN Delivery_Delay."Order Number" ELSE NULL END) AS Delayed_Orders,
    COUNT(CASE WHEN Delivery_Delay.Delay_Days < 1 THEN Delivery_Delay."Order Number" ELSE NULL END) AS On_Time_Orders
FROM 
    Delivery_Delay;



--Identify Common Causes of Delays BY FOCUSING ON THE PRODUCTKEY, STOREKEY, REGION--
WITH Delivery_Delay AS (
    SELECT 
        sales."Order Number",
        sales."StoreKey",
        sales."CustomerKey",
        sales."ProductKey",
        stores."State" AS Region,         -- Assuming State is the region
        sales."Order Duration" AS Delay_Days, 
        sales."Quantity",
        sales."Currency Code",
        sales."Quantity" * product."Unit Price USD" AS Sale_Amount
    FROM 
        public.sales 
    JOIN 
        stores ON sales."StoreKey" = stores."StoreKey"   
    JOIN 
        Product  ON sales."ProductKey" = product."ProductKey" 
	WHERE 
	sales."Order Duration" > 0
)
SELECT 
	Delivery_Delay."ProductKey",
    Delivery_Delay."StoreKey",
    Delivery_Delay.Region,
    COUNT(Delivery_Delay."Order Number") AS Total_Delayed_Orders,
    AVG(Delivery_Delay.Delay_Days) AS Avg_Delay_Days,
    SUM(Delivery_Delay.Sale_Amount) AS Total_Delayed_Sales
FROM 
    Delivery_Delay 	
GROUP BY 
    Delivery_Delay."ProductKey", Delivery_Delay."StoreKey", Delivery_Delay.Region
ORDER BY 
    Total_Delayed_Orders DESC, Avg_Delay_Days DESC;








/*Question 5: What is the relationship between store size (in square meters) and revenue
generation? Are larger stores more effective in driving sales, or is there a
diminishing return as store size increases?
○ Explore the correlation between store size and revenue to determine the most
effective store size for sales performance.*/


WITH Store_Revenue AS (
    SELECT 
        sales."StoreKey",
        SUM(sales."Quantity" * product."Unit Price USD") AS Total_Revenue
    FROM 
        sales 
    JOIN 
        Product ON sales."ProductKey" = product."ProductKey" 
    GROUP BY 
        sales."StoreKey"  
)
SELECT 
    sr."StoreKey",
    st."Square Meters",
    sr.Total_Revenue,
    (sr.Total_Revenue / st."Square Meters") AS Revenue_Per_Square_Meter,
	 CORR(st."Square Meters", sr.Total_Revenue) OVER() AS Correlation_StoreSize_Revenue
FROM 
    Store_Revenue sr
JOIN 
    stores st ON sr."StoreKey" = st."StoreKey" 
ORDER BY 
    Revenue_Per_Square_Meter DESC;

