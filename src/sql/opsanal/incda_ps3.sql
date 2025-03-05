SELECT 
CAST('19' || ps3.YEAR || '-' || lpad(ps3.MONTH,2,'0') || '-' || lpad(ps3.DAY,2,'0') AS DATE) AS REPORT_DATE,
INSEQ,
PCN,
PSSQ3,
VSZ3,
OSEQ,
ORIG,
'19' || left(ps3.ODTG,2) || '-' || substring(ps3.ODTG,3,2) || '-' || substring(ps3.ODTG,5,2) || ' ' || substring(ps3.ODTG,7,2) || ':' || right(ps3.ODTG,2) AS ODTG,
m.value AS MTYPE,
remove_nan_decimals(MSER) AS MSER
FROM opsanal.main.incda_ps3_nara ps3
LEFT JOIN opsanal.main.incda_mtab m
	ON remove_nan_decimals(ps3.MTYPE) = m.code