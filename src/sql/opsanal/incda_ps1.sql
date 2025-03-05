SELECT
CAST('19' || ps1.YEAR || '-' || lpad(ps1.MONTH,2,'0') || '-' || lpad(ps1.DAY,2,'0') AS DATE) AS REPORT_DATE,
	ps1.INSEQ,
	ps1.PCN,
	ps1.PSSQ1,
	ps1.VSZ1,
	ps1.NODES,
	ps1.NODAM,
	ps1.NOCAP,
	ps1.LSEQ,
	n.value AS LNAT,
	l.value AS LOSCD
FROM
	opsanal.main.incda_ps1_nara ps1
LEFT JOIN opsanal.main.incda_natab n
	ON remove_nan_decimals(ps1.LNAT) = n.code
LEFT JOIN opsanal.main.incda_lctab l
	ON remove_nan_decimals(ps1.LOSCD) = l.code