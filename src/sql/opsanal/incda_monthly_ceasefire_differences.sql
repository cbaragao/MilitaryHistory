CREATE VIEW incda_monthly_ceasfire_differences AS 
WITH base AS (
SELECT 
    YEAR(report_date) AS _YEAR,
    MONTH(report_date) AS _MONTH,
    COUNT(1) AS TotalViolations
FROM opsanal.main.incda_tx
GROUP BY YEAR(report_date), MONTH(report_date) 
ORDER BY YEAR(report_date) ASC,  MONTH(report_date)  ASC
),
counts AS (
SELECT 
b._YEAR,
b._MONTH,
b.TotalViolations,
LAG(b.TotalViolations,1,NULL) OVER (ORDER BY b._YEAR, b._MONTH) AS PrevMonthViolations,
FROM base b
ORDER BY b._YEAR, b._MONTH
)
SELECT
	CAST(c._YEAR AS CHAR(4)) AS "YEAR",
	c._MONTH AS "MONTH",
	c.TotalViolations,
	c.PrevMonthViolations,
	CASE WHEN c.PrevMonthViolations IS NULL THEN NULL ELSE ROUND((c.TotalViolations/c.PrevMonthViolations) * 100.0,2) END AS PercentChange
FROM counts c