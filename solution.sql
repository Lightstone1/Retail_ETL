
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




select * from exchange
select * from product
select * from sales;

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
 	RANK() OVER (PARTITION BY Region ORDER BY profit DESC) AS Rank_Profit
From
	Profit_Calculation
