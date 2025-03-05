SELECT 
CAST('19' || ps2.YEAR || '-' || lpad(ps2.MONTH,2,'0') || '-' || lpad(ps2.DAY,2,'0') AS DATE) AS REPORT_DATE,
INSEQ,
PCN,
PSSQ2,
VSZ2,
QTYRCD,
remove_nan_decimals(FORID) AS FORID,
remove_nan_decimals(SUPID) AS SUPID,
a.value AS TYPRCD
FROM opsanal.main.incda_ps2_nara ps2 
LEFT JOIN opsanal.main.incda_amtab a
	ON remove_nan_decimals(TYPRCD) = a.code